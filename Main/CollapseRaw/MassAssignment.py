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


def collapse_mass_assignment(data: list[TokenRawABC],
                             errors: list[OurSyntaxError], results: list[ControlRawABC]):
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

    # разделим на 2 половинки по '=' и потом половинки разделим по запятым.
    left, right = data[:eq_i], data[eq_i + 1:]
    origin = data[0].origin + data[-1].origin

    if not left:
        errors.append(OurSyntaxError('Отсутствует левая часть массового присваивания.', origin))
        return
    if not right:
        errors.append(OurSyntaxError('Отсутствует правая часть массового присваивания.', origin))
        return

    results.append(ControlRawMassAssignment(
        split_by_comma(left, 'Пустое wvalue у массового присваивания', errors),
        split_by_comma(right, 'Пустое rvalue у массового присваивания', errors),
        origin
    ))
