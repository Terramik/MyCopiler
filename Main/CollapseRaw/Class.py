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


def collapse_class(data: list[TokenRawABC], block: ControlRawCodeBlock) -> ControlRawClass:
    if len(data) != 2:
        raise OurSyntaxError('Неожиданное количество токенов, ожидалось class <имя>',
                             data[0].origin + data[-1].origin)
    name = data[1]
    if not isinstance(name, TokenRawWord):
        raise OurSyntaxError('Ожидалось слово(название класса)', name.origin)
    name = name.word

    if len(block.block_parts) < 1:
        raise OurSyntaxError('Не указан блок полей экземпляра', block.origin)
    instance_field = block.block_parts[0]
    if not isinstance(instance_field, ControlRawCodeBlock):
        raise OurSyntaxError('Это не блок полей экзепляра', instance_field.origin)
    for field in instance_field.block_parts:
        if not isinstance(field, ControlRawExpression):
            raise OurSyntaxError('Неожиданная конструкция', field.origin)

    block.block_parts = block.block_parts[1:]
    for ect in block.block_parts:
        if not isinstance(ect, (
                ControlRawFunctionDefinition, ControlRawExpression,
                ControlRawTypedef, ControlRawClass, ControlRawEnum
        )):
            raise OurSyntaxError('В классе разрешены только объявления функций, классов, '
                                 'переменных, перечисления и псевдонимы', ect.origin)

    return ControlRawClass(
        name, instance_field, block,
        data[0].origin + data[-1].origin
    )
