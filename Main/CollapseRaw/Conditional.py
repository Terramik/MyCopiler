from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_conditional(data: list[TokenRawABC]) -> bool:
    if len(data) == 0:
        return False
    if isinstance(data[0], TokenRawWord) and data[0].word in (
            KeyWords.ConditionalStart.value,
            KeyWords.ConditionalMiddle.value,
            KeyWords.ConditionalEnd.value
    ):
        return True
    return False


def collapse_conditional(data: list[TokenRawABC | ControlRawCodeBlock],
                      block: ControlRawCodeBlock) -> ControlRawIf:
    match data[0].word:
        case KeyWords.ConditionalStart.value: _type = ConditionalPartTypes.start
        case KeyWords.ConditionalMiddle.value: _type = ConditionalPartTypes.middle
        case KeyWords.ConditionalEnd.value: _type = ConditionalPartTypes.end
        case _: raise ValueError('что-то пошло не так')

    if _type == ConditionalPartTypes.end and len(data) > 1:
        raise OurSyntaxError('В else не может быть условия', data[1].origin + data[-1].origin)
    elif _type != ConditionalPartTypes.end and len(data) < 2:
        raise OurSyntaxError('В if/elif должно быть условие', data[1].origin)

    return ControlRawIf(
        data[1:], block,
        ControlRawCodeBlock([], data[0].origin + data[-1].origin),
        _type, data[0].origin + data[-1].origin
    )


def clue_conditional(data: list[ControlRawABC]):
    last_if = None
    i = 0
    while i < len(data):
        control = data[i]
        if isinstance(control, ControlRawIf):
            if last_if is None:
                if control.type is not ConditionalPartTypes.start:
                    raise OurSyntaxError(f'Началом условной конструкции должен служить {KeyWords.ConditionalStart}',
                                         control.origin)
                last_if = control
            else:
                # во всех случаях кроме начала конструкции мы удаляем конструкцию, т.к. она уже часть большей
                match control.type:
                    # новый if - новый блок
                    case ConditionalPartTypes.start:
                        last_if = control
                    # elif - добавляем к старым
                    case ConditionalPartTypes.middle:
                        # добавляем его всего в else прошлого блока
                        last_if.block_else = ControlRawCodeBlock(
                            [
                                control
                            ], control.origin
                        )
                        last_if = control # чтобы внедриться дальше по дереву
                        del data[i]
                        i -= 1
                    # else - заканчиваем
                    case ConditionalPartTypes.end:
                        # вставляем на else наш код
                        last_if.block_else = control.block_if
                        last_if = None
                        del data[i]
                        i -= 1
        else:
            # если условный блок прерывается, то он заканчивается.
            if last_if is not None:
                last_if = None
        i += 1

