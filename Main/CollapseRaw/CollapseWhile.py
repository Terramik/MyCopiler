from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_while(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.CycleWhile.value:
        return True
    return False


def collapse_while(data: list[TokenRawABC], block: ControlRawCodeBlock,
                   errors: list[OurSyntaxError], results: list[ControlRawABC]):
    if len(data) < 2:
        errors.append(OurSyntaxError('Отсутствие условия в цикле while', data[0].origin))
    results.append(ControlRawWhile(
        data[1:], block, data[0].origin + data[-1].origin
    ))

