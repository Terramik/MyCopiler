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

    def __contains__(self, item):
        if not isinstance(item, TextPosition):
            return False
        return self.is_in(item)

    def is_before(self, pos: TextPosition):
        if (
            self.start.line > pos.line
        ) or (
            self.start.line == pos.line and
            self.start.column > pos.column
        ):
            return True
        return False

    def is_in(self, pos: TextPosition):
        if (
            # если штука в строках внутри
            self.start.line < pos.line < self.end.line
        ) or (
            # если штуки в начальной строки
            self.start.line == pos.line < self.end.line and
            self.start.column <= pos.column
        ) or (
            # если штуки в последней строке
            self.start.line < pos.line == self.end.line and
            pos.column <= self.end.column
        ) or (
            # если на одной строке
            self.start.line == pos.line == self.end.line and
            self.start.column <= pos.column <= self.end.column
        ):
            return True
        return False

    def is_after(self, pos: TextPosition):
        if (
            pos.line > self.end.line
        ) or (
            pos.line == self.end.line and
            pos.column > self.start.column
        ):
            return True
        return False


zero_origin = TokenOrigin(TextPosition(0, 0), TextPosition(0, 0), Path(''))

