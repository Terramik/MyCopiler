from __future__ import annotations
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def split_by_comma(arr: list[TokenRawABC | ControlRawCodeBlock], err_s: str, errors: list[OurSyntaxError]) -> \
        list[list[TokenRawABC | ControlRawCodeBlock]]:
    """
    Разделяет массив на подмассивы по запятым, не лежачим в скобках
    """
    if len(arr) == 0:
        return []
    res = []
    unclosed_bracket = 0
    last_comma = 0
    for i, tok in enumerate(arr):
        if isinstance(tok, TokenRawSymbol):
            match tok.symbol:
                case '(' | '[':
                    unclosed_bracket += 1
                case ')' | ']':
                    unclosed_bracket -= 1
                case ',':
                    if unclosed_bracket == 0:
                        if last_comma == i:
                            errors.append(OurSyntaxError(err_s, arr[last_comma].origin + tok.origin))
                        else:
                            res.append(arr[last_comma:i])
                            last_comma = i + 1

    if last_comma == len(arr):
        errors.append(OurSyntaxError(err_s, arr[-1].origin))
    else:
        res.append(arr[last_comma:])

    return res
