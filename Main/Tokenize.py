from ..Definitions.Raw import *
from ..Definitions.Exceptions import ReadError
import re
from typing import TextIO

PATTERN_COMMENT = re.compile(r'^\s*#')

TOKENS = [
    TokenRawLiteral,
    TokenRawSymbol,
    TokenRawWord
]


def tokenize_file(file: TextIO, path: Path) -> list[TokenRawABC]:
    """
    Токенизирует содержимое файла на 3 типа примитивных токенов(слово, символ, литерал) и
    выдаёт в виде плоского списка. Игнорирует все символы после '#' до конца строки. При
    невозможности прочитать что-то выкидывает ReadError.
    """
    tokens = []
    line_i = 0
    for line in file:
        col_i = 0
        while line.strip():
            if PATTERN_COMMENT.match(line) is not None:
                break
            for cls in TOKENS:
                match = re.match(cls.PATTERN, line)
                if match is not None:
                    d_col, tok = cls.make(line_i, col_i, path, match)
                    tokens.append(tok)
                    line = line[d_col:]
                    col_i += d_col
                    break
            else:
                raise ReadError('', TextPosition(line_i, col_i))
        line_i += 1
    return tokens
