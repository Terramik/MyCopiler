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


p = Path(__file__).parent / 'logs.txt'


class OurLanguageServer(LanguageServer):
    def __init__(self, *args, **kwargs):
        with open(p, 'w') as f:
            f.write('START\n')
        self.processed_modules: dict[Path, Module] = {}
        self.is_mod_good: dict[Path, bool] = {}
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


    def analyze_module(self, path: Path):
        is_bad, err = analyze_module(path, self.processed_modules)
        if is_bad:
            self.text_document_publish_diagnostics(
                types.PublishDiagnosticsParams(
                    path.as_posix(), [types.Diagnostic(
                        range=self.token_origin_to_pygls_range(err.position),
                        message=err.args[0],
                        severity=types.DiagnosticSeverity.Error
                    )]
                )
            )
            self.is_mod_good[path] = False
        else:
            self.text_document_publish_diagnostics(
                types.PublishDiagnosticsParams(
                    path.as_posix(), []
                )
            )
            self.is_mod_good[path] = True


server = OurLanguageServer('mylang', 'v0.1')


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
        )
    )


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: OurLanguageServer, params: types.DidOpenTextDocumentParams):
    ls.analyze_module(ls.uri_to_path(params.text_document.uri))


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: OurLanguageServer, params: types.DidChangeTextDocumentParams):
    ls.analyze_module(ls.uri_to_path(params.text_document.uri))


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def goto_definition(ls: OurLanguageServer, params: types.DefinitionParams):
    with (open(p, 'a') as f):
        path = ls.uri_to_path(params.text_document.uri)

        if not (path in ls.is_mod_good and ls.is_mod_good.get(path)):
            return None
        mod = ls.processed_modules.get(path)

        assert mod is not None
        assert mod.code is not None

        tok = position_to_node(
            mod,
            ls.pygls_position_to_our_position(params.position)
        )

        print(f'TOK {tok}', file=f)
        if isinstance(tok, TokenVariableAccess):
            tok = tok.var_def

            while True:
                # если переменная импортирована
                for imp in mod.import_:
                    if imp.thing is tok:
                        if imp.from_.is_std: # костыль, т.к. будет сложно сдвинуть их к объявлению в си файле
                            return None

                        exp = imp.from_.find_export(imp.name)
                        if isinstance(exp.thing, TokenOperatorVariableDefinition):
                            tok = imp.thing
                            continue
                        else:
                            return None
                else:
                    break

            print(f'GOTODEF SUCCESS: {tok}', file=f)

            return ls.token_origin_to_pygls_location(tok.origin)
        elif isinstance(tok, Type):
            print(f'TYPE {tok}', file=f)
            if tok.is_simple_typedef:
                return ls.token_origin_to_pygls_location(tok.simple.link.type.origin)
    return None

server.start_io()
