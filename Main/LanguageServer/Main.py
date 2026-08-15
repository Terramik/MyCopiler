from pygls.lsp.server import LanguageServer
from pathlib import Path
from ...Definitions.Modules import Module
from ...Definitions.Exceptions import OurSyntaxError, SemanticError
from ...Definitions.Tokens import *
from ..Modules import analyze_module
from .PositionToNode import position_to_node, position_to_node_with_scope
from lsprotocol import types
from urllib.parse import urlparse, unquote, quote
import sys
from .SemanticPainter import *

p = Path(__file__).parent / 'logs.txt'


class OurLanguageServer(LanguageServer):
    def __init__(self, *args, **kwargs):
        with open(p, 'w') as f:
            f.write('START\n')
        self.processed_modules: dict[Path, Module] = {}
        self.texts: dict[Path, list[str]] = {}

        super().__init__(*args, **kwargs)
        with open(p, 'a') as f:
            f.write('START ENDED\n')

    @staticmethod
    def uri_to_path(uri: str) -> Path:
        parsed = urlparse(uri)
        if sys.platform == "win32":
            parsed = parsed.path.lstrip("/")
        path_str = unquote(parsed)
        return Path(path_str)

    @staticmethod
    def token_origin_to_pygls_range(origin: TokenOrigin) -> types.Range:
        return types.Range(
            types.Position(origin.start.line, origin.start.column),
            types.Position(origin.end.line, origin.end.column),
        )

    @staticmethod
    def token_origin_to_pygls_location(origin: TokenOrigin) -> types.Location:
        return types.Location(
            origin.file.resolve().as_uri(),
            OurLanguageServer.token_origin_to_pygls_range(origin)
        )

    @staticmethod
    def pygls_position_to_our_position(position: types.Position) -> TextPosition:
        return TextPosition(position.line, position.character)

    def analyze_module(self, path: Path, update_text: bool):
        module = analyze_module(path, self.processed_modules)

        self.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                path.as_uri(), [
                    types.Diagnostic(
                        range=self.token_origin_to_pygls_range(err.position),
                        message=err.args[0],
                        severity=types.DiagnosticSeverity.Error
                    )
                    for err in module.errors
                ]
            )
        )

        if update_text:
            with open(path, 'r') as f:
                self.texts[path] = f.read().split('\n')


server = OurLanguageServer('MyLangLS', 'v0.1')


@server.feature(types.INITIALIZE)
def initialize(ls, params):
    return types.InitializeResult(
        capabilities=types.ServerCapabilities(
            text_document_sync=types.TextDocumentSyncOptions(
                open_close=True,
                change=types.TextDocumentSyncKind.Full,
                will_save=False,
                will_save_wait_until=False,
                save=True,
            ),
            definition_provider=True,
            hover_provider=True,
            semantic_tokens_provider=types.SemanticTokensOptions(
                legend=types.SemanticTokensLegend(
                    token_types=LEGEND_TOKEN_TYPES,
                    token_modifiers=LEGEND_MODIFIERS
                ),
                full=True,
                range=False
            ),
            completion_provider=types.CompletionOptions(
                trigger_characters=['.', '->']
            )
        )
    )


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: OurLanguageServer, params: types.DidOpenTextDocumentParams):
    path = ls.uri_to_path(params.text_document.uri)
    ls.analyze_module(path, False)
    ls.texts[path] = params.text_document.text.split('\n')


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: OurLanguageServer, params: types.DidChangeTextDocumentParams):
    ls.analyze_module(ls.uri_to_path(params.text_document.uri), True)


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def goto_definition(ls: OurLanguageServer, params: types.DefinitionParams):
    path = ls.uri_to_path(params.text_document.uri)

    assert path in ls.processed_modules

    mod = ls.processed_modules.get(path)

    tok = position_to_node(
        mod,
        ls.pygls_position_to_our_position(params.position)
    )

    if isinstance(tok, TokenVariableAccess):
        tok = tok.var_def

        while True:
            # если переменная импортирована
            for imp in mod.import_:
                if imp.thing is tok:
                    if imp.from_.is_std:  # костыль, т.к. будет сложно сдвинуть их к объявлению в си файле
                        return None

                    exp = imp.from_.find_export(imp.name)
                    if isinstance(exp.thing, TokenOperatorVariableDefinition):
                        tok = imp.thing
                        continue
                    else:
                        return None
            else:
                break

        return ls.token_origin_to_pygls_location(tok.origin)
    elif isinstance(tok, Type):
        if tok.is_simple_typedef:
            return ls.token_origin_to_pygls_location(tok.simple.link.type.origin)
    return None


def type_to_hover_hint(type: Type) -> str:
    if isinstance(type, ErrorType):
        return '**error type**'
    elif type.is_simple_func:
        return f'func ({
        ', '.join(map(type_to_hover_hint, type.simple.arguments))
        }) -> ({
        ', '.join(map(type_to_hover_hint, type.simple.results))
        })'
    elif type.is_simple_typedef:
        return f'**{type}** aka **{type.full_type}**'
    return f'**{type}**'


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: OurLanguageServer, params: types.HoverParams):
    # ищём штуку
    path = ls.uri_to_path(params.text_document.uri)

    assert path in ls.processed_modules

    mod = ls.processed_modules.get(path)

    tok = position_to_node(
        mod,
        ls.pygls_position_to_our_position(params.position)
    )

    # и выводим сам тип
    type: Type | None = None
    if isinstance(tok, ControlFunctionDefinition):
        type = tok.var.type
    elif isinstance(tok, (TokenOperatorRvalueABC, TokenOperatorWvalueABC)):
        type = tok.res_type
    elif isinstance(tok, Type):
        type = tok  # зачем тип типу? хз.

    if type is not None:
        return types.Hover(
            types.MarkupContent(
                types.MarkupKind.Markdown,
                type_to_hover_hint(type)
            ),
            ls.token_origin_to_pygls_range(tok.origin)
        )
    return None


@server.feature(types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
def semantic_tokens_full(ls: OurLanguageServer, params: types.SemanticTokensParams):
    with open(Path(__file__).parent / 'logs.txt', 'a') as f:
        print('SEMANTIC', file=f)

    # я понятия не имею, почему эта фигня не запрашивает раскраску.
    # вообще.
    assert False

    # путь и модуль
    path = ls.uri_to_path(params.text_document.uri)

    assert path in ls.processed_modules

    mod = ls.processed_modules.get(path)

    data = sematic_print(mod)

    return types.SemanticTokens(data)


def completion_type_to_king(type: Type) -> types.CompletionItemKind:
    if type == t_error:
        return types.CompletionItemKind.Variable

    if type.is_simple_typedef:
        type = type.full_type

    if type.is_simple_class:
        return types.CompletionItemKind.Class
    elif type.is_simple_class_instance:
        return types.CompletionItemKind.Class
    elif type.is_simple_enum:
        return types.CompletionItemKind.Enum
    elif type.is_simple_enum_instance:
        return types.CompletionItemKind.EnumMember
    elif type.is_simple_func:
        return types.CompletionItemKind.Function
    elif type.is_simple_base:
        return types.CompletionItemKind.Value


def completion_type_to_detail(type: Type) -> str:
    return type_to_hover_hint(type).replace('**', '')  # костыли


completion_base_types = [
    types.CompletionItem(
        label=t.value, kind=types.CompletionItemKind.Value, detail=t.value
    ) for t in BaseTypes
]

completion_key_words = [
    types.CompletionItem(
        label='def', kind=types.CompletionItemKind.Keyword,
        insert_text='def ${1:name} (${2:args}) -> (${3:res}) {\n\t${4:code} \n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='return', kind=types.CompletionItemKind.Keyword,
        insert_text='return ${1:values};',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='if', kind=types.CompletionItemKind.Keyword,
        insert_text='if ${1:condition} {\n\t${2:code} \n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='elif', kind=types.CompletionItemKind.Keyword,
        insert_text='elif ${1:condition} {\n\t${2:code} \n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='else', kind=types.CompletionItemKind.Keyword,
        insert_text='else {\n\t${1:code} \n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='while', kind=types.CompletionItemKind.Keyword,
        insert_text='while ${1:condition} {\n\t${2:code} \n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='break', kind=types.CompletionItemKind.Keyword,
        insert_text='break;',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='continue', kind=types.CompletionItemKind.Keyword,
        insert_text='continue;',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='func', kind=types.CompletionItemKind.Keyword,
        insert_text='func (${1:args}) -> (${2:res})',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='alias', kind=types.CompletionItemKind.Keyword,
        insert_text='alias ${1:name} ${2:type};',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='from', kind=types.CompletionItemKind.Keyword,
        insert_text='from ${1:file} import ${2:names};',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='export', kind=types.CompletionItemKind.Keyword,
        insert_text='export ${1:names};',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='class', kind=types.CompletionItemKind.Keyword,
        insert_text='class ${1:name} {\n\t${2:code}\n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
    types.CompletionItem(
        label='enum', kind=types.CompletionItemKind.Keyword,
        insert_text='enum ${1:name} {\n\t${2:states}\n}',
        insert_text_format=types.InsertTextFormat.Snippet
    ),
] + [
    types.CompletionItem(
        label=k, kind=types.CompletionItemKind.Keyword
    ) for k in (
        'var', 'import', 'all'
    )
]

completion_operators = [
    types.CompletionItem(
        label=op, kind=types.CompletionItemKind.Operator
    ) for op in (
        'as', 'and', 'or', 'sizeof', 'lenof', 'not', 'del'
    )
]

completion_all = completion_operators + completion_key_words + completion_base_types

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completion(ls: OurLanguageServer, params: types.CompletionParams):
    # где мы
    path = ls.uri_to_path(params.text_document.uri)
    assert path in ls.processed_modules
    mod = ls.processed_modules.get(path)
    pos = ls.pygls_position_to_our_position(params.position)

    res = []

    # это случай с . и ->
    if params.context.trigger_kind == 2:
        # сдвинем, чтобы попасть в то, откуда мы должны взять поля
        if params.context.trigger_character == '.':
            pos = TextPosition(pos.line, pos.column - 1)
        else:
            pos = TextPosition(pos.line, pos.column - 2)

        tok = position_to_node(mod, pos)
        if isinstance(tok, TokenOperatorRvalueABC):
            type = tok.res_type
            if type.is_simple_class or type.is_simple_class_instance:
                cls: ControlClass = type.cls
                for cls_field in cls.class_field:
                    res.append(types.CompletionItem(
                        label=cls_field.name, kind=types.CompletionItemKind.Property,
                        detail=completion_type_to_detail(cls_field.type)
                    ))
                if type.is_simple_class_instance:
                    for instance_field in cls.class_field:
                        res.append(types.CompletionItem(
                            label=instance_field.name, kind=types.CompletionItemKind.Property,
                            detail=completion_type_to_detail(instance_field.type)
                        ))

            elif type.is_simple_enum:
                enum: ControlEnum = type.enum
                for state in enum.states:
                    res.append(types.CompletionItem(
                        label=state, kind=types.CompletionItemKind.EnumMember
                    ))
    else:
        tok, scope = position_to_node_with_scope(
            mod, pos
        )

        if isinstance(tok, (TokenOperatorFieldAccess, TokenOperatorFieldAccessPointer)):
            op_type = tok.operand.res_type
            if op_type != t_error:
                if op_type.is_simple_class or op_type.is_simple_class_instance:
                    cls: ControlClass = op_type.cls
                    if not cls.is_bad:
                        if tok.operand.res_type.is_simple_class_instance:
                            for cls_field in cls.instance_field:
                                res.append(types.CompletionItem(
                                    label=cls_field.name, kind=types.CompletionItemKind.Property,
                                    detail=completion_type_to_detail(cls_field.type)
                                ))
                        for instance_field in cls.class_field:
                            res.append(types.CompletionItem(
                                label=f.name, kind=types.CompletionItemKind.Property,
                                detail=completion_type_to_detail(instance_field.type)
                            ))
                elif op_type.is_simple_enum:
                    enum: ControlEnum = op_type.enum
                    if not enum.is_bad:
                        for f in enum.states:
                            res.append(types.CompletionItem(
                                label=f, kind=types.CompletionItemKind.EnumMember
                            ))
        else:
            res = completion_all[:]

            while True:
                for var in scope.variables:
                    res.append(types.CompletionItem(
                        label=var.name, kind=completion_type_to_king(var.type),
                        detail=completion_type_to_detail(var.type)
                    ))
                for typedef in scope.typedefs:
                    res.append(types.CompletionItem(
                        label=typedef.typedef.name, kind=completion_type_to_king(typedef.typedef.type),
                        detail=completion_type_to_detail(typedef.typedef.type)
                    ))
                if scope.is_global:
                    break
                scope = scope.parent

    return types.CompletionList(is_incomplete=False, items=res)

server.start_io()
