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
                    block: ControlRawCodeBlock) -> ControlRawEnum:
    if len(data) != 2:
        raise OurSyntaxError('Неожиданное выражение', data[0].origin + data[-1].origin)
    name = data[1]
    if not isinstance(name, TokenRawWord):
        raise OurSyntaxError('Ожидалось слово', name.origin)
    name = name.word
    states = []

    for exp in block.block_parts:
        if not (isinstance(exp, ControlRawExpression) and
                len(exp.tokens) == 1 and
                isinstance(exp.tokens[0], TokenRawWord)):
            raise OurSyntaxError('Неожиданная конструкция', exp.origin)
        states.append(exp.tokens[0].word)
    return ControlRawEnum(
        name, states, data[0].origin + block.origin
    )