from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_function(data: list[TokenRawABC]) -> bool:
    if len(data) == 0:
        return False
    if isinstance(data[0], TokenRawWord) and data[0].word == KeyWords.Function.value:
        return True
    return False


def collapse_function(data: list[TokenRawABC | ControlRawCodeBlock],
                      block: ControlRawCodeBlock) -> ControlRawFunctionDefinition:
    """
    Сворачивает функцию. Не меняет массив data, только достаёт из него информацию.
    В случае несоответствия токенов паттерну функции, может выдать кучу разных OurSyntaxError.
    """
    # проверем штуки
    if len(data) < 4:
        raise OurSyntaxError('обьявление слишком короткое', data[0].origin)

    f_name = data[1]
    if not isinstance(f_name, TokenRawWord):
        raise OurSyntaxError('за объявление функции не следует её имя', f_name.origin)
    tok = data[2]
    if not isinstance(tok, TokenRawSymbol) or tok.symbol != '(':
        raise OurSyntaxError('за именем функции не следует \'(\' ', tok.origin)

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
        raise OurSyntaxError('Блок параметров функции не был закрыт', data[2].origin + data[-2].origin)
    params = split_by_comma(data[start:end], 'Пустой параметр')

    # выделим результаты, если есть
    results = []
    if end != last_tok - 1:
        tok = data[end + 1]
        if isinstance(tok, TokenRawSymbol) and tok.symbol == '->':
            # у функции есть результаты
            tok = data[end + 2]
            if not isinstance(tok, TokenRawSymbol) or tok.symbol != '(':
                raise OurSyntaxError('за -> функции не следует \'(\' ', tok.origin)

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
                raise OurSyntaxError('Блок результатов функции не был закрыт',
                                     data[2].origin + data[-2].origin)
            results = split_by_comma(data[start:end], 'Пустой параметр')

    return ControlRawFunctionDefinition(
        f_name.word, params, results, block,
        data[0].origin + block.origin
    )

