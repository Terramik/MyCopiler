from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_typedef(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Typedef.value:
        return True
    return False


def collapse_typedef(data: list[TokenRawABC],
                     errors: list[OurSyntaxError], results: list[ControlRawABC]):
    if len(data) < 3:
        errors.append(OurSyntaxError('Недостаточное количество токенов в псевдониме', data[0].origin + data[-1].origin))
        return
    name = data[1]
    if not isinstance(name, TokenRawWord):
        errors.append(OurSyntaxError('Ожидалось слово(имя псевдонима)', name.origin))
        return
    results.append(ControlRawTypedef(
        name.word, data[1:], data[0].origin + data[-1].origin
    ))
