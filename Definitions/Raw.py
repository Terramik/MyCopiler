from __future__ import annotations
from .Base import *
from .Enums import KeyWords, ConditionalPartTypes, CycleControlTypes
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import Union


'''
Это объявления для двух штук - сырых токенов и сырых управляющих конструкций.
сырые токены - это очень простые токены трёх видов - слово, символ, и литерал.
Сырые управляющие конструкции - это наборы токенов, подчинявшихся одному правилу,
они служат структурированию кода программы
'''


class TokenRawABC(ABC):
    origin: TokenOrigin

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def repr_full(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def make(cls, *args):
        pass


class TokenRawWord(TokenRawABC):
    """
    Некое слово, будь то ключевое, имя переменной, функции, класса или ещё чего-то.
    """
    __slots__ = ('word', 'origin')
    PATTERN = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)')

    def __init__(self, word: str, origin: TokenOrigin):
        self.word = word
        self.origin = origin

    def __repr__(self):
        return f'{self.word}'

    def repr_full(self) -> str:
        return f'({self.word}->{self.origin})'

    @classmethod
    def make(cls, line_i: int, col_i: int, path: Path, match: re.Match) -> tuple[int, 'TokenRawWord']:
        new_col = col_i + match.span()[1]
        word = match.group(1)
        return match.span()[1], TokenRawWord(
            word,
            TokenOrigin(
                TextPosition(line_i, new_col - len(word)),
                TextPosition(line_i, new_col),
                path
            ))


class TokenRawSymbol(TokenRawABC):
    """
    Некий особый символ, оператор, часть блока кода или управляющая конструкция
    """
    __slots__ = ('symbol', 'origin')
    PATTERN = re.compile(
        r'^\s*(sizeof(?=\s|$)|'
        r'lenof(?=\s|$)|'
        r'and(?=\s|$)|'
        r'or(?=\s|$)|'
        r'as(?=\s|$)|'
        r'var(?=\s|$)|'
        r'not(?=\s|$)|'
        r'del(?=\s|$)|'
        r'->|>>|<<|>=|<=|==|!=|=|\+|-|\*|/|%|&|\^|\||~|<|>|\(|\)|\{|}|;|,|\[|]|:|\.)'
    )

    def __init__(self, symbol: str, origin: TokenOrigin):
        self.symbol = symbol
        self.origin = origin

    def __repr__(self):
        return f'{self.symbol}'

    def repr_full(self) -> str:
        return f'({self.symbol}->{self.origin})'

    @classmethod
    def make(cls, line_i: int, col_i: int, path: Path, match: re.Match) -> tuple[int, 'TokenRawSymbol']:
        new_col = col_i + match.span()[1]
        word = match.group(1)
        return match.span()[1], TokenRawSymbol(
            word,
            TokenOrigin(
                TextPosition(line_i, new_col - len(word)),
                TextPosition(line_i, new_col),
                path
            ))


class TokenRawLiteral(TokenRawABC):
    """
    Литерал (строка или числа)
    """
    __slots__ = ('literal', 'origin')
    PATTERN = re.compile(
        r'^\s*('
            r'0x[0-9a-f]+|'
            r'0b[0-1]+|'
            r'\d+(?:\.\d+)?(?:e[+-]?\d+)?|'
            r"'(?:[^\"\\]|\\.)'|"
            r'true|'
            r'false|'
            r'"([^"\\]|\\.)*"'
        r')',
        re.DOTALL)

    def __init__(self, literal: str, origin: TokenOrigin):
        self.literal = literal
        self.origin = origin

    def __repr__(self):
        return f'{self.literal}'

    def repr_full(self) -> str:
        return f'({self.literal}->{self.origin})'

    @classmethod
    def make(cls, line_i: int, col_i: int, path: Path, match: re.Match) -> tuple[int, 'TokenRawLiteral']:
        new_col = col_i + match.span()[1]
        word = match.group(1)
        return match.span()[1], TokenRawLiteral(
            word,
            TokenOrigin(
                TextPosition(line_i, new_col - len(word)),
                TextPosition(line_i, new_col),
                path
            ))


# ===== Controls =====


class ControlRawABC(ABC):
    origin: TokenOrigin

    @abstractmethod
    def __repr__(self):
        pass


class ControlRawFunctionDefinition(ControlRawABC):
    """
    Необработанная управляющая конструкция объявления функции
    """
    __slots__ = ('name', 'parameters', 'results', 'code_block', 'origin')

    def __init__(self, name: str, parameters: list[list[TokenRawWord | TokenRawSymbol]],
                 results: list[list[TokenRawWord | TokenRawSymbol]], code_block: 'ControlRawCodeBlock', origin: TokenOrigin):
        self.name = name
        self.parameters = parameters
        self.results = results
        self.code_block = code_block
        self.origin = origin

    def __repr__(self):
        return f'{KeyWords.Function.value} {self.name} ({', '.join(map(repr, self.parameters))}) -> ({
                ', '.join(map(repr, self.results))})\n {self.code_block}'


@dataclass(slots=True)
class ControlRawExpression(ControlRawABC):
    """
    Необработанная основная конструкция в блоке кода, она либо присваивает что-то чему-то, либо вызывает что-то.
    """
    tokens: list[TokenRawABC]
    origin: TokenOrigin

    def __repr__(self):
        return f' {' '.join(map(repr, self.tokens))}; '


class ControlRawReturn(ControlRawABC):
    """
    Необработанная конструкция return
    """
    __slots__ = ('tokens', 'origin')

    def __init__(self, tokens: list[list[TokenRawABC]], origin: TokenOrigin):
        self.tokens = tokens
        self.origin = origin

    def __repr__(self):
        return f' {' '.join(map(repr, self.tokens))}; '


class ControlRawMassAssignment(ControlRawABC):
    """
    Необработанная конструкция массового присвоения
    """
    __slots__ = ('left', 'right', 'origin')

    def __init__(self, left: list[list[TokenRawABC]], right: list[list[TokenRawABC]], origin: TokenOrigin):
        self.left = left
        self.right = right
        self.origin = origin

    def __repr__(self):
        return f'{', '.join(map(repr, self.left))} = {', '.join(map(repr, self.right))}; '


class ControlRawCodeBlock(ControlRawABC):
    """
    Необработанный блок кода, такие стоят после управляющий констукций (функции, циклы, условия) и
    хранят в себе вложенные управляющие конструкции и выражения.
    """
    __slots__ = ('block_parts', 'origin')

    def __init__(self, block_parts: list[ControlRawABC], origin: TokenOrigin):
        self.block_parts = block_parts
        self.origin = origin

    def __repr__(self):
        return f'{{{' '.join(map(repr, self.block_parts))}}}'


# ControlRawConditional
@dataclass(slots=True)
class ControlRawIf(ControlRawABC):
    condition: list[TokenRawABC]
    block_if: ControlRawCodeBlock
    block_else: ControlRawCodeBlock | None
    type: ConditionalPartTypes
    origin: TokenOrigin

    def __repr__(self):
        return (
            f'{KeyWords.ConditionalStart.value} ({''.join(map(repr, self.condition))}) \n{self.block_if}'
            f'{KeyWords.ConditionalEnd.value} {self.block_else}\n'
        )


@dataclass(slots=True)
class ControlRawWhile(ControlRawABC):
    condition: list[TokenRawABC]
    code_block: ControlRawCodeBlock
    origin: TokenOrigin

    def __repr__(self):
        return f'while {self.condition} \n {self.code_block}'


@dataclass(slots=True)
class ControlRawCycleControl(ControlRawABC):
    type: CycleControlTypes
    origin: TokenOrigin

    def __repr__(self):
        return self.type.value


@dataclass(slots=True)
class ControlRawTypedef(ControlRawABC):
    name: str
    type: list[TokenRawABC]
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Typedef.value} {''.join(map(repr, self.tokens))}'


@dataclass(slots=True)
class ControlRawImport(ControlRawABC):
    tokens_file: list[TokenRawABC]
    tokens_names: list[list[TokenRawABC]]
    origin: TokenOrigin

    def __repr__(self):
        return (f'{KeyWords.Import_Part1} {''.join(map(repr, self.tokens_file))} '
                f'{KeyWords.Import_Part2} {''.join(map(repr, self.tokens_names))};')


@dataclass(slots=True)
class ControlRawExport(ControlRawABC):
    tokens_names: list[list[TokenRawABC]]
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Export} {''.join(map(repr, self.tokens_names))};'


@dataclass(slots=True)
class ControlRawClass(ControlRawABC):
    name: str
    instance_field: ControlRawCodeBlock
    rest: ControlRawCodeBlock
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Class_Definition.value} {self.name} \n{{ {{{''.join(repr(inst) for inst in self.instance_field.block_parts)}}} {''.join(repr(rest) for rest in self.rest.block_parts)} }}'


@dataclass(slots=True)
class ControlRawEnum(ControlRawABC):
    name: str
    states: list[str]
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Enum_Definition.value} {self.name} {{{''.join(f'{s};' for s in self.states)}}}'

