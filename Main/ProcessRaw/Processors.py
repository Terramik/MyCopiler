from __future__ import annotations
from ...Definitions.Raw import *
from ...Definitions.Tokens import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Definitions.TreeInterface import IteratorExpression
from .Parsers import *


def process_expression(expr: ControlRawExpression) -> ControlExpression:
    # можем r\w значениями, так что просто
    return ControlExpression(
        process_any_value(expr.tokens),
        expr.origin)


def process_return(expr: ControlRawReturn) -> ControlReturn:
    return ControlReturn(
        [process_rvalue(tokens) for tokens in expr.tokens],
        expr.origin
    )


def process_mass_assignment(expr: ControlRawMassAssignment) -> ControlMassAssignment:
    return ControlMassAssignment(
        [process_wvalue(tokens) for tokens in expr.left],
        [process_rvalue(tokens) for tokens in expr.right],
        expr.origin
    )


def process_cycle_control(cont: ControlRawCycleControl) -> ControlCycleControl:
    return ControlCycleControl(
        cont.type, cont.origin
    )


def process_typedef(typedef: ControlRawTypedef) -> ControlTypedef:
    return ControlTypedef(
        Type.Typedef(process_type(typedef.type), typedef.name), typedef.origin
    )

def process_enum(enum: ControlRawEnum) -> ControlEnum:
    # просто скопируем
    return ControlEnum(
        enum.name, enum.states, enum.origin
    )


def import_export_check_names(tokens_names: list[list[TokenRawABC]]) -> tuple[bool, list[tuple[str, str]]]:
    # проверяем имена
    all_ = False
    names = []
    for name in tokens_names:
        if len(name) == 1:
            name = name[0]
            if not isinstance(name, TokenRawWord):
                raise OurSyntaxError('Неожиданный токен, ожидалось слово', name.origin)
            name = name.word
            if name == KeyWords.Import_Export_All.value:
                all_ = True
            else:
                names.append((name, name))
        elif len(name) == 3:
            alias = name[2]
            as_ = name[1]
            name = name[0]
            if not isinstance(name, TokenRawWord):
                raise OurSyntaxError('Неожиданный токен, ожидалось слово', name.origin)
            if not isinstance(as_, TokenRawSymbol) or as_.symbol != KeyWords.Import_Export_Alias.value:
                raise OurSyntaxError(f'Неожиданный токен, ожидалось "{KeyWords.Import_Export_Alias.value}"', as_.origin)
            if not isinstance(alias, TokenRawWord):
                raise OurSyntaxError('Неожиданный токен, ожидалось слово', alias.origin)
            names.append((name.word, alias.word))
        else:
            raise OurSyntaxError('Неожиданное количество токенов',
                                 name[0].origin + name[-1].origin)

    return all_, names


def process_import(import_: ControlRawImport) -> ControlImport:
    # склеиваем путь обратно
    path = []
    for tok in import_.tokens_file:
        match tok:
            case TokenRawWord():
                path.append(tok.word)
            case TokenRawSymbol():
                path.append(tok.symbol)
            case TokenLiteral():
                path.append(tok.value)
            case _:
                raise ValueError('')
    path = ''.join(path)
    # имена
    all_, names = import_export_check_names(import_.tokens_names)

    return ControlImport(
        path, all_, names, import_.origin
    )

        
def process_export(export: ControlRawExport) -> ControlExport:
    all_, names = import_export_check_names(export.tokens_names)

    return ControlExport(
        all_, names, export.origin
    )


def process_code_block(block: ControlRawCodeBlock) -> ControlCodeBlock:
    raise NotImplemented('')


def process_if(cond: ControlRawIf) -> ControlIf:
    return ControlIf(
        process_rvalue(cond.condition),
        process_code_block(cond.block_if),
        process_code_block(cond.block_else),
        cond.origin
    )


def process_while(_while: ControlRawWhile) -> ControlWhile:
    return ControlWhile(
        process_rvalue(_while.condition),
        process_code_block(_while.code_block),
        _while.origin
    )


def process_function(func: ControlRawFunctionDefinition) -> ControlFunctionDefinition:
    return ControlFunctionDefinition(
        func.name,
        [process_define(d) for d in func.parameters],
        [process_type(d) for d in func.results],
        process_code_block(func.code_block),
        func.origin
    )


class ItExpr(IteratorExpression):
    """Нужен для поиска объявлений функций"""
    def __init__(self, all_vars: list[TokenOperatorVariableDefinition]):
        self.all_vars = all_vars

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        self.all_vars.append(node)


def process_class(class_: ControlRawClass) -> ControlClass:
    instance_field = []
    for field_ in class_.instance_field.block_parts:
        assert isinstance(field_, ControlRawExpression)
        instance_field.append(process_define(field_.tokens))
    rest = process_code_block(class_.rest)

    return ControlClass(
        class_.name, instance_field, rest,
        class_.origin
    )


def process_code_block(block: ControlRawCodeBlock) -> ControlCodeBlock:
    def inner(data: ControlRawCodeBlock) -> ControlCodeBlock:
        res = []
        for control in data.block_parts:
            match control:
                case ControlRawExpression():
                    res.append(process_expression(control))
                case ControlRawCodeBlock():
                    res.append(inner(control))
                case ControlRawReturn():
                    res.append(process_return(control))
                case ControlRawMassAssignment():
                    res.append(process_mass_assignment(control))
                case ControlRawFunctionDefinition():
                    res.append(process_function(control))
                case ControlRawIf():
                    res.append(process_if(control))
                case ControlRawCycleControl():
                    res.append(process_cycle_control(control))
                case ControlRawWhile():
                    res.append(process_while(control))
                case ControlRawTypedef():
                    res.append(process_typedef(control))
                case ControlRawImport():
                    res.append(process_import(control))
                case ControlRawExport():
                    res.append(process_export(control))
                case ControlRawClass():
                    res.append(process_class(control))
                case ControlRawEnum():
                    res.append(process_enum(control))

        return ControlCodeBlock(res, data.origin)

    return inner(block)


def process_raw(block: ControlRawCodeBlock) -> ControlCodeBlock:
    return process_code_block(block)





