from .. import Definitions
from ..Definitions import *
from .....Definitions.Exceptions import OurSyntaxError
from .....Definitions.Tokens import *


__all__ = (
    '_parse_vardef',
    '_parse_cast',
    '_parse_sizeof',
    '_parse_array',
    '_parse_index_or_slice',
)


def _parse_vardef(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorVariableDefinition]:
    """Парсит объявление переменной, var <name> <тип>"""
    var = data[start]
    assert isinstance(var, RawOperator) and var.symbol == KeyWords.Variable.value
    if start + 1 >= end or not isinstance(name := data[start + 1], RawOperand) or not isinstance(name.thing, TokenRawWord):
        raise OurSyntaxError('После ключевого слова объявления переменной("var") должно следовать её имя', var.origin)
    name = name.thing.word
    i, _type = Definitions.parse_type(data, start + 2, end)
    return i, TokenOperatorVariableDefinition(name, _type,
                                              data[start].origin + data[i].origin)


def _parse_cast(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TreeOperatorCast]:
    _as = data[start]
    assert isinstance(_as, RawOperator) and _as.symbol == KeyWords.Cast.value
    i, _type = Definitions.parse_type(data, start + 1, end)
    return i, TreeOperatorCast(_type, _as.origin)


def _parse_sizeof(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorSizeof]:
    sizeof = data[start]
    assert isinstance(sizeof, RawOperator) and sizeof.symbol == KeyWords.Sizeof.value
    i, _type = Definitions.parse_type(data, start + 1, end)
    return i, TokenOperatorSizeof(_type, sizeof.origin + data[i].origin)


def _parse_array(data: list[PreprocessResults], operands: OperandsStack,
                operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorArrayCreation]:
    assert isinstance(data[start], SquareBracketOpen)
    last_separator = start
    i = start + 1
    depth = 0
    elements = []

    while i < end:
        cur = data[i]
        match cur:
            case BracketOpen() | SquareBracketOpen():
                depth += 1
            case BracketClose():
                if depth == 0:
                    raise OurSyntaxError('Неоткрытая скобка', cur.origin)
                depth -= 1
            case SquareBracketClose():
                if depth == 0:
                    break
                depth -= 1
            case Separator():
                if depth == 0:
                    if last_separator + 1 == i:
                        raise OurSyntaxError('Пустой элемент массива', cur.origin)
                    i_end, elem = Definitions.parse_general(data, [], [], last_separator + 1, i)
                    if not isinstance(elem, TokenOperatorRvalueABC):
                        raise OurSyntaxError('Элементы в массиве должны быть rvalue', elem.origin)
                    last_separator = i
                    elements.append(elem)
        i += 1
    else:
        raise OurSyntaxError('Незакрытая скобка', data[start].origin)

    if last_separator + 1 == i:
        raise OurSyntaxError('Пустой элемент массива', cur.origin)
    i_end, elem = Definitions.parse_general(data, [], [], last_separator + 1, i)
    if not isinstance(elem, TokenOperatorRvalueABC):
        raise OurSyntaxError('Элементы в массиве должны быть rvalue', elem.origin)
    elements.append(elem)

    return i, TokenOperatorArrayCreation(elements, data[start].origin + data[i].origin)


def _parse_index_or_slice(data: list[PreprocessResults], operands: OperandsStack,
                         operators: OperatorsStack, start: int, end: int) -> \
        tuple[int, TreeOperatorIndex | TreeOperatorSlice]:
    assert isinstance(data[start], SquareBracketOpen)
    last_separator = start
    delimiter: int
    i = start + 1
    depth = 0
    elements1 = []
    delimiter_found = False
    elements2 = []

    while i < end:
        cur = data[i]
        match cur:
            case BracketOpen() | SquareBracketOpen():
                depth += 1
            case BracketClose():
                if depth == 0:
                    raise OurSyntaxError('Неоткрытая скобка', cur.origin)
                depth -= 1
            case SquareBracketClose():
                if depth == 0:
                    break
                depth -= 1

            case Delimiter():
                if depth == 0:
                    if not delimiter_found:
                        # эта штука вида [:... без индексов
                        if start + 1 == i:
                            delimiter_found = True
                            last_separator = i
                            delimiter = i
                        else:
                            if last_separator + 1 == i:
                                raise OurSyntaxError('Пустой элемент среза|массива', cur.origin)
                            i_end, elem = Definitions.parse_general(data, [], [], last_separator + 1, i)
                            if not isinstance(elem, TokenOperatorRvalueABC):
                                raise OurSyntaxError('Индексы в индексации|срезе должны быть rvalue', elem.origin)
                            elements1.append(elem)
                            delimiter_found = True
                            last_separator = i
                            delimiter = i
                    else:
                        raise OurSyntaxError('":" в срезе может быть только одно', cur.origin)

            case Separator():
                if depth == 0:
                    if last_separator + 1 == i:
                        raise OurSyntaxError('Пустой элемент среза|массива', cur.origin)
                    i_end, elem = Definitions.parse_general(data, [], [], last_separator + 1, i)
                    if not isinstance(elem, TokenOperatorRvalueABC):
                        raise OurSyntaxError('Индексы в индексации|срезе должны быть rvalue', elem.origin)
                    last_separator = i
                    if delimiter_found:
                        elements2.append(elem)
                    else:
                        elements1.append(elem)
        i += 1
    else:
        raise OurSyntaxError('Незакрытая скобка', data[start].origin)

    # если эта штука вида [...:](без индексов, то мы пропустим последнее сворачивание
    if not (delimiter_found and delimiter + 1 == i):

        if last_separator + 1 == i:
            raise OurSyntaxError('Пустой элемент среза|массива', cur.origin)
        i_end, elem = Definitions.parse_general(data, [], [], last_separator + 1, i)
        if not isinstance(elem, TokenOperatorRvalueABC):
            raise OurSyntaxError('Индексы в индексации|срезе должны быть rvalue', elem.origin)
        if delimiter_found:
            elements2.append(elem)
        else:
            elements1.append(elem)

    if delimiter_found:
        return i, TreeOperatorSlice(elements1, elements2, data[start].origin + data[i].origin)
    else:
        return i, TreeOperatorIndex(elements1)



