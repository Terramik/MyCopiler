from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_return(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Return.value:
        return True
    return False


def collapse_return(data: list[TokenRawABC],
                    errors: list[OurSyntaxError], results: list[ControlRawABC]):
    """
    Сворачивает выражение, первое слово которого - return в специальную конструкцию
    """
    results.append(ControlRawReturn(
        split_by_comma(data[1:], 'Возвращаемое rvalue пусто', errors),
        data[0].origin + data[-1].origin
    ))
