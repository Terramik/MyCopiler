from enum import Enum
from .Tokens import Type
from . import TypesShortener as types
from dataclasses import dataclass


@dataclass
class MagicMethodData:
    needed_type: Type



magic_methods = {
    '__init__',
    '__del__',
    '__bool__',
    '__add__',
    '__sub__',
    '__mul__',
    '__div__',
    '__mod__',
    '__eq__',
    '__ne__',
    '__lt__',
    '__le__',
    '__gt__',
    '__ge__',
}

