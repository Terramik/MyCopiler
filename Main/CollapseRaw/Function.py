from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_function(data: list[TokenRawABC]) -> bool:
    if len(data) < 1:
        return False
    if isinstance(data[0], TokenRawWord) and data[0].word == KeyWords.Function.value:
        return True
    return False


def collapse_function(data: list[TokenRawABC | ControlRawCodeBlock],
                      block: ControlRawCodeBlock,
                      errors: list[OurSyntaxError], results: list[ControlRawABC]):
    """
    Сворачивает функцию. Не меняет массив data, только достаёт из него информацию.
    В случае несоответствия токенов паттерну функции, может выдать кучу разных OurSyntaxError.
    """
    # проверим штуки
    if len(data) < 4:
        errors.append(OurSyntaxError('Cлишком мало токенов для объявления функции', data[0].origin + data[-1].origin))
        return

    f_name = data[1]
    if not isinstance(f_name, TokenRawWord):
        errors.append(OurSyntaxError('За объявлением функции не следует её имя', f_name.origin))
        return
    tok = data[2]
    if not isinstance(tok, TokenRawSymbol) or tok.symbol != '(':
        errors.append(OurSyntaxError('За именем функции не следует "(" ', tok.origin))
        return

    # выделим аргументы
    last_tok = len(data)
    start = 3
    end = start
    closed = False

    # найдём конец параметров
    depth = 0
    while end < last_tok:
        tok = data[end]
        if isinstance(tok, TokenRawSymbol):
            if tok.symbol == '(':
                depth += 1
            elif tok.symbol == ')':
                if depth == 0:
                    closed = True
                    break
                else:
                    depth -= 1
        end += 1
    if not closed:
        errors.append(OurSyntaxError('Блок параметров функции не был закрыт', data[2].origin + data[-2].origin))
        return
    params = split_by_comma(data[start:end], 'Пустой параметр', errors)

    # выделим результаты, если есть
    results_types = []
    if end != last_tok - 1:
        tok = data[end + 1]
        if isinstance(tok, TokenRawSymbol) and tok.symbol == '->':
            # у функции есть результаты
            tok = data[end + 2]
            if not isinstance(tok, TokenRawSymbol) or tok.symbol != '(':
                errors.append(OurSyntaxError('За -> функции не следует "(" ', tok.origin))
                return

            # получаем результаты
            start = end + 3
            end = start
            closed = False

            # найдём конец результатов
            depth = 0
            while end < last_tok:
                tok = data[end]
                if isinstance(tok, TokenRawSymbol):
                    if tok.symbol == '(':
                        depth += 1
                    elif tok.symbol == ')':
                        if depth == 0:
                            closed = True
                            break
                        else:
                            depth -= 1
                end += 1
            if not closed:
                errors.append(OurSyntaxError('Блок результатов функции не был закрыт',
                                             data[2].origin + data[-2].origin))
            results_types = split_by_comma(data[start:end], 'Пустой результат', errors)

    results.append(ControlRawFunctionDefinition(
        f_name.word, params, results_types, block,
        data[0].origin + data[-1].origin
    ))

