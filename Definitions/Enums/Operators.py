from enum import Enum
from .Else import KeyWords


class Associativity(Enum):
    left = 1
    right = 2


class OperatorType:
    __slots__ = ('symbol', 'associativity', 'priority')

    def __init__(self, symbol: str, associativity: Associativity, priority: int):
        self.symbol = symbol
        self.associativity = associativity
        self.priority = priority

    def __eq__(self, other):
        if isinstance(other, OperatorType):
            return other is self
        elif isinstance(other, str):
            return self.symbol == other
        else:
            return False

    def __hash__(self):
        return hash(self.symbol)

    def __repr__(self):
        return f'OpType: {self.symbol}'


class TokenOperatorBinaryTypes(Enum):

    FieldAccess = OperatorType('.', Associativity.left, 1)
    FieldAccessPointer = OperatorType('->', Associativity.left, 1)

    Cast = OperatorType('as', Associativity.left, 10)

    Indexing = OperatorType('[]', Associativity.left, 15)
    Slicing = OperatorType('[:]', Associativity.left, 15)

    ArfmMul = OperatorType('*', Associativity.left, 21)
    ArfmDiv = OperatorType('/', Associativity.left, 21)
    ArfmMod = OperatorType('%', Associativity.left, 21)
    ArfmAdd = OperatorType('+', Associativity.left, 22)
    ArfmSub = OperatorType('-', Associativity.left, 22)

    BitShiftLeft = OperatorType('<<', Associativity.left, 30)
    BitShiftRight = OperatorType('>>', Associativity.left, 30)

    BitAnd = OperatorType('&', Associativity.left, 41)
    BitXor = OperatorType('^', Associativity.left, 42)
    BitOr = OperatorType('|', Associativity.left, 43)

    ComprEq = OperatorType('==', Associativity.left, 50)
    ComprNEq = OperatorType('!=', Associativity.left, 50)
    ComprLess = OperatorType('<', Associativity.left, 50)
    ComprLessOrEq = OperatorType('<=', Associativity.left, 50)
    ComprMore = OperatorType('>', Associativity.left, 50)
    ComprMoreOrEq = OperatorType('>=', Associativity.left, 50)

    LogAnd = OperatorType('and', Associativity.left, 61)
    LogOr = OperatorType('or', Associativity.left, 62)

    AsgmUsial = OperatorType('=', Associativity.right, 70)


class TokenOperatorPrefixTypes(Enum):
    # ну очень особый оператор
    VarDef = OperatorType(KeyWords.Variable.value, Associativity.left, 1) # омега приоритет
    Fcall = OperatorType('call', Associativity.left, 1) # тут Associativity.left не очень подходит, и это как-бы костыль
    Sizeof = OperatorType('sizeof', Associativity.left, 5)
    Lenof = OperatorType('lenof', Associativity.left, 12)

    ArfmUnMin = OperatorType('-', Associativity.right, 20)
    BitNot = OperatorType('~', Associativity.right, 40)
    LogNot = OperatorType('not', Associativity.right, 60)

    DeInitializer = OperatorType('del', Associativity.right, 6)


class TokenOperatorPostfixTypes(Enum):
    # Костылизация продолжается, но мне просто нужны операторы, чтобы понять, что я
    # должен делать, так что может... это не костыль?
    # Также, они лежат тут, а не в бинарных операторах... потому что... ах, мне лень объяснять, и тут
    # слишком много костылей
    ArrayCreation = OperatorType('array', Associativity.left, 1)
    SlizeOrIndexing = OperatorType('SlizeOrIndexing', Associativity.left, 15)

    Dereferencing = OperatorType('*', Associativity.left, 15)
    Referencing = OperatorType('&', Associativity.left, 15)


class TokenOperatorsTypes:
    Arithmetic = (
        TokenOperatorBinaryTypes.ArfmAdd,
        TokenOperatorBinaryTypes.ArfmSub,
        TokenOperatorBinaryTypes.ArfmMul,
        TokenOperatorBinaryTypes.ArfmDiv,
        TokenOperatorBinaryTypes.ArfmMod,
        TokenOperatorPrefixTypes.ArfmUnMin,
    )
    BitwiseShifts = (
        TokenOperatorBinaryTypes.BitShiftLeft,
        TokenOperatorBinaryTypes.BitShiftRight,
    )
    Bitwise = (
        TokenOperatorPrefixTypes.BitNot,
        TokenOperatorBinaryTypes.BitAnd,
        TokenOperatorBinaryTypes.BitXor,
        TokenOperatorBinaryTypes.BitOr,
    )
    Comparison = (
        TokenOperatorBinaryTypes.ComprEq,
        TokenOperatorBinaryTypes.ComprNEq,
        TokenOperatorBinaryTypes.ComprLess,
        TokenOperatorBinaryTypes.ComprLessOrEq,
        TokenOperatorBinaryTypes.ComprMore,
        TokenOperatorBinaryTypes.ComprMoreOrEq,
    )
    Logical = (
        TokenOperatorPrefixTypes.LogNot,
        TokenOperatorBinaryTypes.LogOr,
        TokenOperatorBinaryTypes.LogAnd,
    )
    Assignment = (
        TokenOperatorBinaryTypes.AsgmUsial,
    )

