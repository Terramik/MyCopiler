from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_class(data: list[TokenRawABC]) -> bool:
    if len(data) < 1:
        return False
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Class_Definition.value:
        return True
    return False


def collapse_class(data: list[TokenRawABC], block: ControlRawCodeBlock,
                   errors: list[OurSyntaxError], results: list[ControlRawABC]):
    if len(data) != 2:
        errors.append(OurSyntaxError('Неожиданное количество токенов, ожидалось class <имя>',
                                     data[0].origin + data[-1].origin))
        return

    name = data[1]
    if not isinstance(name, TokenRawWord):
        errors.append(OurSyntaxError('Ожидалось слово(имя класса)', name.origin))
        return
    name = name.word

    if len(block.block_parts) < 1:
        errors.append(OurSyntaxError('Отсутствует блок полей экземпляра', block.origin))
        return

    instance_field = block.block_parts[0]
    if not isinstance(instance_field, ControlRawCodeBlock):
        errors.append(OurSyntaxError('Это не блок полей экзепляра', instance_field.origin))
        return
    i = 0
    while i < len(instance_field.block_parts):
        field = instance_field.block_parts[i]
        if not isinstance(field, ControlRawExpression):
            errors.append(OurSyntaxError('Неожиданная конструкция', field.origin))
            del instance_field.block_parts[i]
        else:
            i += 1

    block.block_parts = block.block_parts[1:]
    i = 0
    while i < len(block.block_parts):
        tok = block.block_parts[i]
        if not isinstance(tok, (
                ControlRawFunctionDefinition, ControlRawExpression,
                ControlRawTypedef, ControlRawClass, ControlRawEnum
        )):
            errors.append(OurSyntaxError('В классе разрешены только объявления функций, классов, '
                                         'переменных, перечисления и псевдонимы', tok.origin))
            del block.block_parts[i]
        else:
            i += 1

    results.append(ControlRawClass(
        name, instance_field, block,
        data[0].origin + data[-1].origin
    ))
