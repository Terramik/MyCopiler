from __future__ import annotations
from ...Definitions.Raw import *
from ...Definitions.Tokens import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Definitions.TreeInterface import IteratorExpression
from .Parsers import *


def process_expression(expr: ControlRawExpression, errors: list[OurSyntaxError]) -> ControlExpression:
    # можем r\w значениями, так что просто
    return ControlExpression(
        process_any_value(expr.tokens),
        expr.origin)


def process_return(expr: ControlRawReturn, errors: list[OurSyntaxError]) -> ControlReturn:
    return ControlReturn(
        [process_rvalue(tokens, errors) for tokens in expr.tokens],
        expr.origin
    )


def process_mass_assignment(expr: ControlRawMassAssignment, errors: list[OurSyntaxError]) -> ControlMassAssignment:
    return ControlMassAssignment(
        [process_wvalue(tokens, errors) for tokens in expr.left],
        [process_rvalue(tokens, errors) for tokens in expr.right],
        expr.origin
    )


def process_cycle_control(cont: ControlRawCycleControl, errors: list[OurSyntaxError]) -> ControlCycleControl:
    return ControlCycleControl(
        cont.type, cont.origin
    )


def process_typedef(typedef: ControlRawTypedef, errors: list[OurSyntaxError]) -> ControlTypedef:
    return ControlTypedef(
        Type.Typedef(process_type(typedef.type, errors), typedef.name), typedef.origin
    )


def process_enum(enum: ControlRawEnum, errors: list[OurSyntaxError]) -> ControlEnum:
    # просто скопируем
    return ControlEnum(
        enum.name, enum.states, enum.origin
    )


def import_export_check_names(tokens_names: list[list[TokenRawABC]], errors: list[OurSyntaxError]) -> tuple[bool, list[tuple[str, str]]]:
    # проверяем имена
    all_ = False
    names = []
    i = 0
    while i < len(tokens_names):
        name = tokens_names[i]

        if len(name) == 1:
            name = name[0]
            if not isinstance(name, TokenRawWord):
                errors.append(OurSyntaxError('Неожиданный токен, ожидалось слово', name.origin))
                del tokens_names[i]
                i -= 1
            else:
                name = name.word
                if name == KeyWords.Import_Export_All.value:
                    all_ = True
                else:
                    names.append((name, name))

        elif len(name) == 3:
            alias = name[2]
            as_ = name[1]
            name = name[0]

            is_name = isinstance(name, TokenRawWord)
            is_as = isinstance(as_, TokenRawSymbol) and as_.symbol != KeyWords.Import_Export_Alias.value
            is_alias = isinstance(alias, TokenRawWord)

            if not (is_name and is_as and is_alias):
                if not is_name:
                    errors.append(OurSyntaxError('Неожиданный токен, ожидалось слово', name.origin))
                if not is_as:
                    errors.append(OurSyntaxError(f'Неожиданный токен, ожидалось "{KeyWords.Import_Export_Alias.value}"', as_.origin))
                if not is_alias:
                    errors.append(OurSyntaxError('Неожиданный токен, ожидалось слово', alias.origin))
                del tokens_names[i]
                i -= 1
            else:
                names.append((name.word, alias.word))
        else:
            errors.append(OurSyntaxError('Неожиданное количество токенов',
                                         name[0].origin + name[-1].origin))
        i += 1

    return all_, names


def process_import(import_: ControlRawImport, errors: list[OurSyntaxError]) -> ControlImport:
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
    all_, names = import_export_check_names(import_.tokens_names, errors)

    return ControlImport(
        path, all_, names, import_.origin
    )

        
def process_export(export: ControlRawExport, errors: list[OurSyntaxError]) -> ControlExport:
    all_, names = import_export_check_names(export.tokens_names, errors)

    return ControlExport(
        all_, names, export.origin
    )


def process_code_block(block: ControlRawCodeBlock, errors: list[OurSyntaxError]) -> ControlCodeBlock:
    raise NotImplemented('')


def process_if(cond: ControlRawIf, errors: list[OurSyntaxError]) -> ControlIf:
    return ControlIf(
        process_rvalue(cond.condition, errors),
        process_code_block(cond.block_if, errors),
        process_code_block(cond.block_else, errors),
        cond.origin
    )


def process_while(_while: ControlRawWhile, errors: list[OurSyntaxError]) -> ControlWhile:
    return ControlWhile(
        process_rvalue(_while.condition, errors),
        process_code_block(_while.code_block, errors),
        _while.origin
    )


def process_function(func: ControlRawFunctionDefinition, errors: list[OurSyntaxError]) -> ControlFunctionDefinition:
    return ControlFunctionDefinition(
        func.name,
        [process_define(d, errors) for d in func.parameters],
        [process_type(d, errors) for d in func.results],
        process_code_block(func.code_block, errors),
        func.origin
    )


class ItExpr(IteratorExpression):
    """Нужен для поиска объявлений функций"""
    def __init__(self, all_vars: list[TokenOperatorVariableDefinition]):
        self.all_vars = all_vars

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        self.all_vars.append(node)


def process_class(class_: ControlRawClass, errors: list[OurSyntaxError]) -> ControlClass:
    instance_field = []
    for field_ in class_.instance_field.block_parts:
        assert isinstance(field_, ControlRawExpression)
        instance_field.append(process_define(field_.tokens, errors))
    rest = process_code_block(class_.rest, errors)

    return ControlClass(
        class_.name, instance_field, rest,
        class_.origin
    )


def process_code_block(block: ControlRawCodeBlock) -> tuple[ControlCodeBlock, list[OurSyntaxError]]:
    errors = []

    def inner(data: ControlRawCodeBlock, errors: list[OurSyntaxError]) -> ControlCodeBlock:
        res = []
        for control in data.block_parts:
            match control:
                case ControlRawExpression():
                    res.append(process_expression(control, errors))
                case ControlRawCodeBlock():
                    res.append(inner(control, errors))
                case ControlRawReturn():
                    res.append(process_return(control, errors))
                case ControlRawMassAssignment():
                    res.append(process_mass_assignment(control, errors))
                case ControlRawFunctionDefinition():
                    res.append(process_function(control, errors))
                case ControlRawIf():
                    res.append(process_if(control, errors))
                case ControlRawCycleControl():
                    res.append(process_cycle_control(control, errors))
                case ControlRawWhile():
                    res.append(process_while(control, errors))
                case ControlRawTypedef():
                    res.append(process_typedef(control, errors))
                case ControlRawImport():
                    res.append(process_import(control, errors))
                case ControlRawExport():
                    res.append(process_export(control, errors))
                case ControlRawClass():
                    res.append(process_class(control, errors))
                case ControlRawEnum():
                    res.append(process_enum(control, errors))

        return ControlCodeBlock(res, data.origin)

    return inner(block, errors), errors


def process_raw(block: ControlRawCodeBlock) -> ControlCodeBlock:
    return process_code_block(block)





