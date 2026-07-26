from __future__ import annotations
from ....Definitions.Raw import TokenRawWord, TokenRawSymbol, TokenRawLiteral
from ....Definitions.Tokens import *
from ....Definitions.Enums import *
from ....Definitions.Base import *
from ....Definitions.Exceptions import OurSyntaxError
from dataclasses import dataclass


@dataclass(slots=True)
class RawOperator:
    symbol: str
    origin: TokenOrigin

    def __repr__(self):
        return self.symbol


@dataclass(slots=True)
class RawOperand:
    thing: TokenRawWord | TokenRawLiteral
    origin: TokenOrigin

    def __repr__(self):
        if isinstance(self.thing, TokenRawWord):
            return self.thing.word
        else:
            return self.thing.literal


@dataclass(slots=True)
class Dummy:
    origin: TokenOrigin


class BracketOpen(Dummy):
    def __repr__(self):
        return '('


class BracketClose(Dummy):
    def __repr__(self):
        return ')'


class SquareBracketOpen(Dummy):
    def __repr__(self):
        return '['


class SquareBracketClose(Dummy):
    def __repr__(self):
        return ']'


class Separator(Dummy):
    def __repr__(self):
        return ','


class Delimiter(Dummy):
    def __repr__(self):
        return ':'


class TreeOperatorABC(ABC):
    origin: TokenOrigin

    @property
    @abstractmethod
    def associativity(self) -> Associativity:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @abstractmethod
    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        pass

    @staticmethod
    def rvalueize(operand: TokenOperatorABC) -> TokenOperatorRvalueABC:
        if not isinstance(operand, TokenOperatorRvalueABC):
            raise OurSyntaxError('Ожидалось rvalue', operand.origin)
        return operand

    @staticmethod
    def wvalueize(operand: TokenOperatorABC) -> TokenOperatorWvalueABC:
        if not isinstance(operand, TokenOperatorWvalueABC):
            raise OurSyntaxError('Ожидалось wvalue', operand.origin)
        return operand

    @staticmethod
    def rwvalueize(operand: TokenOperatorABC) -> TokenOperatorWvalueABC | TokenOperatorRvalueABC:
        if not isinstance(operand, (TokenOperatorWvalueABC, TokenOperatorRvalueABC)):
            raise OurSyntaxError('Ожидалось rvalue|wvalue', operand.origin)
        return operand

@dataclass(slots=True)
class TreeOperatorBinary(TreeOperatorABC):
    type: TokenOperatorBinaryTypes
    origin: TokenOrigin

    def __repr__(self):
        return f'{self.type.value.symbol}'

    @property
    def associativity(self) -> Associativity:
        return self.type.value.associativity

    @property
    def priority(self) -> int:
        return self.type.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 2:
            raise OurSyntaxError('У бинарного оператора нету достаточного количества операндов', self.origin)
        if self.type == TokenOperatorBinaryTypes.AsgmUsial:
            right = self.rvalueize(operands.pop())
            left = self.wvalueize(operands.pop())
            operands.append(
                TokenOperatorAssignment(left, right, self.origin)
            )

        elif self.type in (TokenOperatorBinaryTypes.FieldAccess, TokenOperatorBinaryTypes.FieldAccessPointer):
            right = operands.pop()
            if not isinstance(right, TokenVariableAccess):
                raise OurSyntaxError('Имя в доступе к полю должно быть словом', right.origin)
            left = self.rvalueize(operands.pop())
            if self.type == TokenOperatorBinaryTypes.FieldAccess:
                operands.append(TokenOperatorFieldAccess(
                    left, right.name, self.origin
                ))
            else:
                operands.append(TokenOperatorFieldAccessPointer(
                    left, right.name, self.origin
                ))

        else:
            right = self.rvalueize(operands.pop())
            left = self.rvalueize(operands.pop())
            operands.append(
                TokenOperatorBinary(self.type, left, right, self.origin)
            )


@dataclass(slots=True)
class TreeOperatorPrefix(TreeOperatorABC):
    type: TokenOperatorPrefixTypes
    origin: TokenOrigin

    def __repr__(self):
        return f'{self.type.value.symbol}'

    @property
    def associativity(self) -> Associativity:
        return self.type.value.associativity

    @property
    def priority(self) -> int:
        return self.type.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У префиксного оператора нету достаточного количества операндов', self.origin)
        if self.type == TokenOperatorPrefixTypes.Lenof:
            operands.append(TokenOperatorLenof(
                self.rvalueize(operands.pop()), self.origin
            ))
        elif self.type == TokenOperatorPrefixTypes.DeInitializer:
            operands.append(TokenOperatorDeInitializer(
                self.rvalueize(operands.pop()), self.origin
            ))
        else:
            operands.append(
                TokenOperatorPrefix(self.type, self.rvalueize(operands.pop()), self.origin)
            )

@dataclass(slots=True)
class TreeOperatorPostfix(TreeOperatorABC):
    type: TokenOperatorPostfixTypes
    origin: TokenOrigin

    def __repr__(self):
        return f'{self.type.value.symbol}'

    @property
    def associativity(self) -> Associativity:
        return self.type.value.associativity

    @property
    def priority(self) -> int:
        return self.type.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У постфиксного оператора нету достаточного количества операндов', self.origin)
        if self.type == TokenOperatorPostfixTypes.Referencing:
            operands.append(
                TokenOperatorReferencing(self.wvalueize(operands.pop()), self.origin)
            )
        elif self.type == TokenOperatorPostfixTypes.Dereferencing:
            operands.append(
                TokenOperatorDereferencing(self.rvalueize(operands.pop()), self.origin)
            )
        else:
            raise ValueError('что-то пошло не так')


@dataclass(slots=True)
class TreeOperatorFunctionCall(TreeOperatorABC):
    args: list[TokenOperatorRvalueABC]
    origin: TokenOrigin

    @property
    def associativity(self) -> Associativity:
        return TokenOperatorPrefixTypes.Fcall.value.associativity

    @property
    def priority(self) -> int:
        return TokenOperatorPrefixTypes.Fcall.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У вызова функции нету достаточного количества операндов', self.origin)
        operands.append(
            TokenOperatorFunctionCall(
                self.rvalueize(operands.pop()), self.args, self.origin
            )
        )


@dataclass(slots=True)
class TreeOperatorCast(TreeOperatorABC):
    cast_to: Type
    origin: TokenOrigin

    @property
    def associativity(self) -> Associativity:
        return TokenOperatorBinaryTypes.Cast.value.associativity

    @property
    def priority(self) -> int:
        return TokenOperatorBinaryTypes.Cast.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У преобразования типа нету достаточного количества операндов', self.origin)
        operands.append(
            TokenOperatorCast(
                self.cast_to, self.rvalueize(operands.pop()), self.origin
            )
        )


@dataclass(slots=True)
class TreeOperatorIndex(TreeOperatorABC):
    indexes: list[TokenOperatorRvalueABC]

    @property
    def associativity(self) -> Associativity:
        return TokenOperatorBinaryTypes.Indexing.value.associativity

    @property
    def priority(self) -> int:
        return TokenOperatorBinaryTypes.Indexing.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У индексации типа нету достаточного количества операндов', self.origin)
        operand = self.rwvalueize(operands.pop())
        for index in self.indexes:
            operand = TokenOperatorIndex(operand, index, index.origin)
        operands.append(operand)


@dataclass(slots=True)
class TreeOperatorSlice(TreeOperatorABC):
    indexes: list[TokenOperatorRvalueABC]
    sizes: list[TokenOperatorRvalueABC]
    origin: TokenOrigin

    @property
    def associativity(self) -> Associativity:
        return TokenOperatorBinaryTypes.Slicing.value.associativity

    @property
    def priority(self) -> int:
        return TokenOperatorBinaryTypes.Slicing.value.priority

    def reduce(self, operands: OperandsStack, operators: OperatorsStack):
        if len(operands) < 1:
            raise OurSyntaxError('У индексации типа нету достаточного количества операндов', self.origin)
        operands.append(
            TokenOperatorSlize(
                self.rwvalueize(operands.pop()),
                self.indexes if self.indexes else None,
                self.sizes if self.sizes else None,
                self.origin
            )
        )


PreprocessResults = Union[
    RawOperator,
    RawOperand,
    BracketOpen,
    BracketClose,
    SquareBracketOpen,
    SquareBracketClose,
    Separator,
    Delimiter,
]

Operand = Union[
    TokenOperatorABC,
]


OperandsStack = list[Operand]


OperatorsStack = list[TreeOperatorABC]


class LastTokensTypes(Enum):
    """
    Нужен для того, чтобы отслеживать, каким был последний токен, и каким положено быть следующим
    """
    operand = 0
    prefix = 1
    binary = 2
    postfix = 3
    # он бинарный, потому-что это удовлетворяет условию того, что может стоять в "начале"(буквальное начало, после
    # открывающей скобки или запятой) строки - операнд или префиксный оператор
    none = binary


# функции для парсинга выражений
# первый результат(int) - это индекс последнего обработанного токена.


def parse_fcall(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TreeOperatorFunctionCall]:
    raise NotImplementedError('')


def parse_type(data: list[PreprocessResults], start: int, end: int) -> tuple[int, Type]:
    raise NotImplementedError('')


def parse_general(data: list[PreprocessResults], operands: OperandsStack,
                  operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorABC]:
    raise NotImplementedError('')


def parse_vardef(data: list[PreprocessResults], operands: OperandsStack,
                 operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorVariableDefinition]:
    raise NotImplementedError('')


def parse_cast(data: list[PreprocessResults], operands: OperandsStack,
               operators: OperatorsStack, start: int, end: int) -> tuple[int, TreeOperatorCast]:
    raise NotImplementedError('')


def parse_sizeof(data: list[PreprocessResults], operands: OperandsStack,
                 operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorSizeof]:
    raise NotImplementedError('')


def parse_array(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorArrayCreation]:
    raise NotImplementedError('')


def parse_index_or_slice(data: list[PreprocessResults], operands: OperandsStack,
                         operators: OperatorsStack, start: int, end: int) -> \
        tuple[int, TreeOperatorIndex | TreeOperatorSlice]:
    raise NotImplementedError('')


from .Things.Type import *
from .Things.Fcall import *
from .Things.Ect import *
from .Things.General import *


parse_type = _parse_type
parse_fcall = _parse_fcall
parse_vardef = _parse_vardef
parse_cast = _parse_cast
parse_sizeof = _parse_sizeof
parse_array = _parse_array
parse_index_or_slice = _parse_index_or_slice
parse_general = _parse_general
