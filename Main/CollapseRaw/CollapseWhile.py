from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_while(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.CycleWhile.value:
        return True
    return False


def collapse_while(data: list[TokenRawABC], block: ControlRawCodeBlock) -> ControlRawWhile:
    if len(data) < 2:
        raise OurSyntaxError('В условии цикла while должно что-то стоять,', data[0].origin)
    return ControlRawWhile(
        data[1:], block, data[0].origin + data[-1].origin
    )

