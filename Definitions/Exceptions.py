from __future__ import annotations
from .Base import *
from typing import Union


class CompilerError(Exception):
    pass


class ReadError(CompilerError):
    def __init__(self, message: str, position: TextPosition):
        super().__init__(message)
        self.position = position

    def __str__(self):
        return f'Ошибка чтение с {self.position}'


class OurSyntaxError(CompilerError):
    def __init__(self, message: str, position: TokenOrigin):
        super().__init__(message)
        self.position = position

    def __str__(self):
        return f'{self.args[0]} на {self.position}'


class SemanticError(CompilerError):
    def __init__(self, message: str, position: TokenOrigin):
        super().__init__(message)
        self.position = position

    def __str__(self):
        return f'{self.args[0]} на {self.position}'
