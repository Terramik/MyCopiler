from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_enum(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Enum_Definition.value:
        return True
    return False


def collapse_enum(data: list[TokenRawABC],
                  block: ControlRawCodeBlock,
                  errors: list[OurSyntaxError], results: list[ControlRawABC]):
    if len(data) != 2:
        errors.append(OurSyntaxError('Неожиданное количество токенов', data[0].origin + data[-1].origin))
        return
    name = data[1]
    if not isinstance(name, TokenRawWord):
        errors.append(OurSyntaxError('Ожидалось слово(имя перечисления)', name.origin))
        return
    name = name.word
    states = []

    for exp in block.block_parts:
        if not (isinstance(exp, ControlRawExpression) and
                len(exp.tokens) == 1 and
                isinstance(exp.tokens[0], TokenRawWord)):
            errors.append(OurSyntaxError('Неожиданная конструкция, ожидалось имя состояния перечисления', exp.origin))
        else:
            states.append(exp.tokens[0].word)

    results.append(ControlRawEnum(
        name, states, data[0].origin + block.origin
    ))