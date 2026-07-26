from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_typedef(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Typedef.value:
        return True
    return False


def collapse_typedef(data: list[TokenRawABC]) -> ControlRawTypedef:
    return ControlRawTypedef(
        data[1:], data[0].origin + data[-1].origin
    )
