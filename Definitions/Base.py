from __future__ import annotations
from pathlib import Path
# from .Enums import *
# from abc import ABC, abstractmethod
# from typing import Union


class TextPosition:
    __slots__ = ('line', 'column')

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.line}:{self.column}'


class TokenOrigin:
    __slots__ = ('start', 'end', 'file')

    def __init__(self, start: TextPosition, end: TextPosition, file: Path):
        self.start = start
        self.end = end
        self.file = file

    def __add__(self, other: TokenOrigin):
        return TokenOrigin(
            self.start, other.end, self.file
        )

    def __repr__(self):
        return f'{self.start}-{self.end}'


zero_origin = TokenOrigin(TextPosition(0, 0), TextPosition(0, 0), Path(''))

