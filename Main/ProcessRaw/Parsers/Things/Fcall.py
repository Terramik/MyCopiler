from .. import Definitions
from ..Definitions import *
from .....Definitions.Exceptions import OurSyntaxError
from .....Definitions.Tokens import *

# должен обрабатывать вызов функции


__all__ = ('_parse_fcall',)


def _parse_fcall(data: list[PreprocessResults], operands: OperandsStack,
      operators: OperatorsStack, start: int, end: int) -> tuple[int, TreeOperatorFunctionCall]:
    assert isinstance(data[start], BracketOpen)
    i = start + 1
    depth = 0 # для отслеживания вложенности из-за скобок, чтобы мы работали только с нашей.
    last_separator = start
    arguments = []
    while i < end:
        cur = data[i]
        match cur:
            case BracketOpen() | SquareBracketOpen():
                depth += 1
            case SquareBracketClose():
                if depth == 0:
                    raise OurSyntaxError('Неоткрытая скобка', cur.origin)
                depth -= 1
            case BracketClose():
                if depth == 0:
                    # мы нашли конец вызова функции
                    break
                depth -= 1
            case Separator():
                if depth == 0:
                    # ещё один аргумент
                    if last_separator + 1 == i:
                        raise OurSyntaxError('Пустой аргумент вызова функции', cur.origin)
                    _, arg = Definitions.parse_general(data, [], [], last_separator + 1, i)
                    if not isinstance(arg, TokenOperatorRvalueABC):
                        raise OurSyntaxError('Аргумент вызова функции должен быть rvalue', arg.origin)
                    arguments.append(arg)
                    last_separator = i
        i += 1
    else:
        raise OurSyntaxError('Незакрытая скобка', data[start].origin)

    # теперь последний аргумент, между последней запятой и скобкой
    if start + 1 != i: # аргументы есть вообще, так что между последней запятой и скобкой тоже должен быть
        if i == last_separator + 1:
            raise OurSyntaxError('Пустой аргумент вызова функции', data[i].origin)
        _, arg = Definitions.parse_general(data, [], [], last_separator + 1, i)
        if not isinstance(arg, TokenOperatorRvalueABC):
            raise OurSyntaxError('Аргумент вызова функции должен быть rvalue', arg.origin)
        arguments.append(arg)
    # и теперь сам вызов
    return i, TreeOperatorFunctionCall(
        arguments,
        data[start].origin + data[i].origin
    )

