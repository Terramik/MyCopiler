from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_mass_assignment(data: list[TokenRawABC]) -> bool:
    # проверим, есть ли ',' и '=' вне скобок, и если есть - то это массовое присвоение
    unclosed_bracket = 0
    is_comma = False
    is_assignment = False
    for i, tok in enumerate(data):
        if isinstance(tok, TokenRawSymbol):
            match tok.symbol:
                case '(' | '[':
                    unclosed_bracket += 1
                case ')' | ']':
                    unclosed_bracket -= 1
                case ',':
                    if unclosed_bracket == 0:
                        is_comma = True
                case '=':
                    if unclosed_bracket == 0 and not is_assignment:
                        is_assignment = True
            if is_comma and is_assignment:
                return True
    return False


def collapse_mass_assignment(data: list[TokenRawABC]) -> ControlRawMassAssignment:
    # найдём '='
    eq_i: int
    unclosed_bracket = 0
    for i, tok in enumerate(data):
        if isinstance(tok, TokenRawSymbol):
            match tok.symbol:
                case '(' | '[':
                    unclosed_bracket += 1
                case ')' | ']':
                    unclosed_bracket -= 1
                case '=':
                    if unclosed_bracket == 0:
                        eq_i = i
                        break
    else:
        raise ValueError('Что-то пошло не так')

    # разделим на 2 половинки по la_bequille (индекс '=') и потом половинки разделим по запятым.
    left, right = data[:eq_i], data[eq_i + 1:]
    origin = data[0].origin + data[-1].origin

    if not left:
        raise OurSyntaxError('Левая часть массового присваивания должна быть', origin)
    if not right:
        raise OurSyntaxError('Правая часть массового присваивания должна быть', origin)

    return ControlRawMassAssignment(
        split_by_comma(left, 'Пустое wvalue у массового присваивания'),
        split_by_comma(right, 'Пустое rvalue у массового присваивания'),
        origin
    )
