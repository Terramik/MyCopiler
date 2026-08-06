from __future__ import annotations
from .Function import collapse_function, is_function
from .Return import collapse_return, is_return
from .MassAssignment import collapse_mass_assignment, is_mass_assignment
from .Conditional import collapse_conditional, is_conditional, clue_conditional
from .CollapseWhile import collapse_while, is_while
from .CycleControl import collapse_cycle_control, is_cycle_control
from .Typedef import collapse_typedef, is_typedef
from .Modules import collapse_import, is_import, collapse_export, is_export
from .Class import collapse_class, is_class
from .Enums import collapse_enum, is_enum
from ...Definitions.Enums import KeyWords
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from typing import Union


NestedTokenRawList = list[Union[TokenRawABC, 'NestedRawTokenList']]


def split_to_expressions(data: NestedTokenRawList, errors: list[OurSyntaxError], origin: TokenOrigin) -> ControlRawCodeBlock:
    """
    Разбивает списки на сырые выражения и управляющие конструкции
    """
    last_semicolon = 0
    result = []
    i = 0
    while i < len(data):
        tok = data[i]
        if (isinstance(tok, TokenRawSymbol) and tok.symbol == ';') or \
                isinstance(tok, ControlRawCodeBlock):

            if isinstance(tok, ControlRawCodeBlock):
                # в блоках кода если за ... ; идёт { ... }, то он идёт сразу, и мы не хотим выбрасывать исключение.
                if last_semicolon == i:
                    result.append(data[i])
                    last_semicolon = i + 1
                    i += 1
                    continue

            if last_semicolon == i:
                errors.append(OurSyntaxError('Выражение без содержимого',
                                             data[last_semicolon].origin + data[i].origin))

            else:
                cut = data[last_semicolon:i]

                if isinstance(tok, ControlRawCodeBlock):
                    if is_function(cut):
                        collapse_function(cut, data[i], errors, result)
                    elif is_conditional(cut):
                        collapse_conditional(cut, data[i], errors, result)
                    elif is_while(cut):
                        collapse_while(cut, data[i], errors, result)
                    elif is_class(cut):
                        collapse_class(cut, data[i], errors, result)
                    elif is_enum(cut):
                        collapse_enum(cut, data[i], errors, result)

                else:
                    if is_return(cut):
                        collapse_return(cut, errors, result)
                    elif is_mass_assignment(cut):
                        collapse_mass_assignment(cut, errors, result)
                    elif is_cycle_control(cut):
                        collapse_cycle_control(cut, errors, result)
                    elif is_typedef(cut):
                        collapse_typedef(cut, errors, result)
                    elif is_import(cut):
                        collapse_import(cut, errors, result)
                    elif is_export(cut):
                        collapse_export(cut, errors, result)
                    else:
                        # просто выражение
                        result.append(ControlRawExpression(
                            cut, data[last_semicolon].origin + data[i].origin
                        ))

            last_semicolon = i + 1
        i += 1

    if last_semicolon != i:
        errors.append(OurSyntaxError('Обнаружены не обьеденённые в выражение токены',
                                     data[last_semicolon].origin + data[i - 1].origin))
    clue_conditional(result, errors)

    return ControlRawCodeBlock(result, origin)


def collapse_nest(data: list[TokenRawABC]) -> tuple[ControlRawCodeBlock, list[OurSyntaxError]]:
    """
    Сворачивает все блоки кода, управляющие конструкции и выражения в их сырые версии.
    """
    errors = []

    # свернём все {} во вложенные списки, так чтобы код в своих блоках представлялся просто как
    # некий абстрактный блок с кодом размером в 1 сущность, а также свернём все выражения и конструкции в блоках.
    brace_stack: list[int] = []
    brace_pos_stack: list[TokenOrigin] = []

    i = 0
    while i < len(data):
        tok = data[i]
        if isinstance(tok, TokenRawSymbol):
            if tok.symbol == '{':
                brace_stack.append(i)
                brace_pos_stack.append(tok.origin)
            elif tok.symbol == '}':
                if not brace_stack:
                    # допустим, тут ничего не было
                    errors.append(OurSyntaxError('Блок кода не был открыт', tok.origin))
                else:
                    last_i = brace_stack.pop()
                    brace_pos_stack.pop()
                    data[last_i] = split_to_expressions(data[last_i+1:i], errors,
                                                        data[last_i].origin + data[i].origin)
                    del data[last_i + 1: i + 1]
                    i = last_i
        i += 1

    # добавим все незакрытые в ошибки
    if brace_stack:
        for pos in brace_pos_stack:
            errors.append(OurSyntaxError('Блок кода не был закрыт', pos))

    # теперь свернём самый верхний блок кода

    origin = data[0].origin + data[-1].origin if data else zero_origin
    block = split_to_expressions(data, errors, origin)

    # проверим, что остались только объявления функций
    i = 0
    while i < len(block.block_parts):
        tok = block.block_parts[i]
        if not isinstance(tok, (
            ControlRawFunctionDefinition,
            ControlRawTypedef,
            ControlRawExpression,
            ControlRawClass,
            ControlRawImport,
            ControlRawExport,
            ControlRawEnum
        )):
            errors.append(
                OurSyntaxError('В глобальной области разрешены только объявления '
                               'функций, выражения, псевдонимы, классы, перечисления, экспорты и импорты', tok.origin)
            )
            del block.block_parts[i]
        else:
            i += 1

    return block, errors

