from __future__ import annotations
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ..Enums import *
from ..Raw import TokenRawLiteral, TokenRawWord
from .Type import *
from ..Base import *


TypeExpressionParent = Union[
    'TokenOperatorRvalueABC',
    'TokenOperatorWvalueABC',
    'ControlABC',
]


class TokenOperatorABC(ABC):
    res_type: Type
    origin: TokenOrigin

    @abstractmethod
    def __repr__(self):
        pass


class TokenOperatorRvalueABC(TokenOperatorABC):
    @abstractmethod
    def __repr__(self):
        pass


class TokenOperatorWvalueABC(TokenOperatorABC):
    @abstractmethod
    def __repr__(self):
        pass


@dataclass(slots=True)
class TokenOperatorVariableDefinition(TokenOperatorWvalueABC):
    name: str
    type: Type
    origin: TokenOrigin

    def __repr__(self):
        return self.type.with_name(self.name)

    @property
    def res_type(self) -> Type:
        return self.type

    @res_type.setter
    def res_type(self, type: Type):
        self.type = type

    @res_type.setter
    def res_type(self, new: Type):
        self.type = new


@dataclass(slots=True)
class TokenVariableAccess(TokenOperatorRvalueABC, TokenOperatorWvalueABC):
    name: str
    origin: TokenOrigin
    is_nonlocal: bool = False
    var_def: TokenOperatorVariableDefinition | None = None

    def __repr__(self):
        if self.var_def is None:
            return self.name
        else:
            return self.var_def.name

    @property
    def res_type(self) -> Type:
        if self.var_def:
            return self.var_def.type
        else:
            return None

    @res_type.setter
    def res_type(self, type: Type):
        self.var_def.type = type


@dataclass(slots=True)
class TokenLiteral(TokenOperatorRvalueABC):
    type: 'TokenLiteral.Types'
    value: str
    origin: TokenOrigin
    res_type: Type | None = None

    Types = TokenLiteralTypes

    @classmethod
    def from_raw(cls, raw: TokenRawLiteral) -> 'TokenLiteral':
        if re.fullmatch(r'"([^"\\]|\\.)*"', raw.literal):
            return TokenLiteral(
                cls.Types.Str, raw.literal[1:-1], raw.origin, # обрежем ""
                Type(Type.SimpleTypeBase(BaseTypes.uint8), [Type.ModifierSlise(1)])
            )
        elif re.fullmatch(r'\'([^"\\]|\\.)\'', raw.literal):
            return TokenLiteral(
                cls.Types.Char, raw.literal, raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.uint8), [])
            )
        elif re.fullmatch(f'(true|false)', raw.literal):
            return TokenLiteral(
                cls.Types.Bool, raw.literal, raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.bool), [])
            )
        elif re.fullmatch(r'\d+', raw.literal):
            return TokenLiteral(
                cls.Types.Int, raw.literal, raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.int64), [])
            )
        elif re.fullmatch(r'0x[0-9a-f]+|', raw.literal):
            return TokenLiteral(
                cls.Types.Int, str(int(raw.literal, 16)), raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.int64), [])
            )
        elif re.fullmatch(r'0b[0-1]+|', raw.literal):
            return TokenLiteral(
                cls.Types.Int, str(int(raw.literal, 2)), raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.int64), [])
            )
        else:
            return TokenLiteral(
                cls.Types.Float, raw.literal, raw.origin,
                Type(Type.SimpleTypeBase(BaseTypes.float64), [])
            )

    def __repr__(self):
        return self.value


@dataclass(slots=True)
class TokenOperatorAssignment(TokenOperatorRvalueABC):
    left: TokenOperatorWvalueABC
    right: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'({self.left}) = ({self.right})'


@dataclass(slots=True)
class TokenOperatorFunctionCall(TokenOperatorRvalueABC):
    func: TokenOperatorRvalueABC
    arguments: list[TokenOperatorRvalueABC]
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'({self.func})({', '.join(map(repr, self.arguments))})'


@dataclass(slots=True)
class TokenOperatorBinary(TokenOperatorRvalueABC):
    type: 'TokenOperatorBinary.Types'
    left: TokenOperatorRvalueABC
    right: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    Types = TokenOperatorBinaryTypes

    def __repr__(self):
        return f'({self.left}) {self.type.value.symbol} ({self.right})'


@dataclass(slots=True)
class TokenOperatorPrefix(TokenOperatorRvalueABC):
    type: 'TokenOperatorPrefix.Types'
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    Types = TokenOperatorPrefixTypes

    def __repr__(self):
        return f'{self.type.value.symbol} ({self.operand})'


@dataclass(slots=True)
class TokenOperatorPostfix(TokenOperatorRvalueABC):
    type: 'TokenOperatorPostfix.Types'
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    Types = TokenOperatorPostfixTypes

    def __repr__(self):
        return f'({self.operand}) {self.type.value.symbol}'


@dataclass(slots=True)
class TokenOperatorCast(TokenOperatorRvalueABC):
    cast_type: Type
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin

    @property
    def res_type(self) -> Type:
        return self.cast_type

    @res_type.setter
    def res_type(self, type: Type):
        self.cast_type = type

    @res_type.setter
    def res_type(self, new: Type):
        self.cast_type = new

    def __repr__(self):
        return f'({self.operand}) as ({self.cast_type})'


@dataclass(slots=True)
class TokenOperatorSizeof(TokenOperatorRvalueABC):
    type: Type
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'{KeyWords.Sizeof} ({self.type})'


@dataclass(slots=True)
class TokenOperatorLenof(TokenOperatorRvalueABC):
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'{KeyWords.Lenof} ({self.operand})'


@dataclass(slots=True)
class TokenOperatorSlize(TokenOperatorRvalueABC):
    operand: TokenOperatorRvalueABC
    position_start: list[TokenOperatorRvalueABC] | None
    result_dimensions: list[TokenOperatorRvalueABC] | None
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return (f'({self.operand})['
                f'{'' if self.position_start is None else ', '.join(map(repr, self.position_start))}:'
                f'{'' if self.result_dimensions is None else ', '.join(map(repr, self.result_dimensions))}]')


@dataclass(slots=True)
class TokenOperatorIndex(TokenOperatorRvalueABC, TokenOperatorWvalueABC):
    operand: TokenOperatorRvalueABC | TokenOperatorWvalueABC
    index: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'({self.operand})[{self.index}]'


@dataclass(slots=True)
class TokenOperatorArrayCreation(TokenOperatorRvalueABC):
    operands: list[TokenOperatorRvalueABC]
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'[{', '.join(map(repr, self.operands))}]'


@dataclass(slots=True)
class TokenOperatorReferencing(TokenOperatorRvalueABC):
    operand: TokenOperatorWvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'({self.operand})&'


@dataclass(slots=True)
class TokenOperatorDereferencing(TokenOperatorRvalueABC, TokenOperatorWvalueABC):
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'({self.operand})*'


@dataclass(slots=True)
class TokenOperatorFieldAccess(TokenOperatorRvalueABC, TokenOperatorWvalueABC):
    operand: TokenOperatorRvalueABC
    name: str
    origin: TokenOrigin
    res_type: Type | Type = None
    field: TokenOperatorVariableDefinition | None = None

    def __repr__(self):
        return f'({self.operand}).{self.name}'


@dataclass(slots=True)
class TokenOperatorFieldAccessPointer(TokenOperatorRvalueABC, TokenOperatorWvalueABC):
    operand: TokenOperatorRvalueABC
    name: str
    origin: TokenOrigin
    res_type: Type | None = None
    field: TokenOperatorVariableDefinition | None = None

    def __repr__(self):
        return f'({self.operand})->{self.name}'


@dataclass(slots=True)
class TokenOperatorDeInitializer(TokenOperatorRvalueABC):
    operand: TokenOperatorRvalueABC
    origin: TokenOrigin
    res_type: Type | None = None

    def __repr__(self):
        return f'{KeyWords.DeInitializer.value} ({self.operand})'


