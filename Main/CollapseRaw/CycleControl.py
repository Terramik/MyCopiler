from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_cycle_control(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and (
            first.word == KeyWords.CycleControlBreak.value or
            first.word == KeyWords.CycleControlContinue.value
    ):
        return True
    return False


def collapse_cycle_control(data: list[TokenRawABC]) -> ControlRawCycleControl:
    if len(data) != 1:
        raise OurSyntaxError('Количество слов в управляющей конструкции цикла - исключительно одно',
                             data[0].origin + data[-1].origin)
    match data[0].word:
        case KeyWords.CycleControlBreak.value: _type = CycleControlTypes.break_
        case KeyWords.CycleControlContinue.value: _type = CycleControlTypes.continue_
        case _: raise ValueError('что-то пошло не так')
    return ControlRawCycleControl(
        _type, data[0].origin
    )

