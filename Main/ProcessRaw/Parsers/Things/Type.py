from .. import Definitions
from ..Definitions import *
from .....Definitions.Exceptions import OurSyntaxError
from .....Definitions.Tokens import *

# Должен парсить тип


__all__ = ('_parse_type',)


def parse_types_list(data: list[PreprocessResults], start: int, end: int) -> tuple[int, list[Type]]:
    """Обходит конструкцию вида "(<тип>, <тип>, ...)" и выдаёт все найденные типы"""
    assert isinstance(data[start], BracketOpen)
    results = []
    i = start + 1

    while True:
        i, type = Definitions.parse_type(data, i, end)
        results.append(type)
        i += 1
        match data[i]:
            case BracketClose():
                break
            case Separator():
                i += 1
            case _:
                raise OurSyntaxError('Неожиданный токен в ряде типов, ожидалось ")" или ","', data[i].origin)

    return i, results


def _parse_type(data: list[PreprocessResults], start: int, end: int) -> tuple[int, Type]:
    # нет открывающей скобки, это простой тип
    i = start
    depth = 0
    simple_type_found = False
    simple: Type.SimpleTypeABC

    modifiers = []
    if not data:
        raise OurSyntaxError('Типа нет, да и вообще, кто учил тебя писать буквы?', zero_origin)

    # для начала найдём простой тип
    cur = data[i]
    # учтём "("
    while isinstance(cur, BracketOpen):
        i += 1
        depth += 1
        cur = data[i]

    if isinstance(cur, RawOperand) and isinstance(cur.thing, TokenRawWord):
        word = cur.thing.word
        # это тип-функция
        if word == KeyWords.FunctionTypeDeclarator.value:
            # найдём типы-аргументы
            args = []
            ii = i + 1
            if ii >= end or not isinstance(data[ii], BracketOpen):
                raise OurSyntaxError('После func(тип-функция) ожидается "("', cur.origin)

            i_end, arguments = parse_types_list(data, ii, end)
            # теперь больше проверок
            assert isinstance(data[i_end], BracketClose)
            ii = i_end + 1
            if ii >= end or not isinstance(data[ii], RawOperator) or data[ii].symbol != '->':
                raise OurSyntaxError('После первого блока типов(агрументов) ожидается "->"',
                                     data[i_end].origin)
            ii += 1
            if ii >= end or not isinstance(data[ii], BracketOpen):
                raise OurSyntaxError('После первого блока типов(агрументов) и "->" ожидается "("',
                                     data[i_end].origin)
            # и типы-результаты
            i_end, results = parse_types_list(data, ii, end)
            # всё
            simple = Type.SimpleTypeFunc(arguments, results)
            i = i_end
        # простой тип
        else:
            # получаем всякие вложенные имена
            indexes = []
            while i + 2 < end and isinstance(data[i + 1], RawOperator) and data[i + 1].symbol == '.' and \
                    isinstance(data[i + 2], RawOperand) and isinstance(data[i + 2].thing, TokenRawWord):
                indexes.append(data[i + 2].thing.word)
                i += 2
            # сам тип
            simple = Type.SimpleTypeRaw(word, indexes)

    else:
        raise OurSyntaxError('Неожиданный токен, ожидался простой тип типа', cur.origin)
    i += 1

    # теперь модификаторы
    while True:
        #
        if i >= end:
            break
        cur = data[i]

        match cur:
            case BracketOpen():
                depth += 1
            case BracketClose():
                if depth == 0:
                    break
                else:
                    depth -= 1
            case SquareBracketClose():
                break
            # это модификатор массива или среза
            case SquareBracketOpen():
                # гарантируем, что _next есть
                if i + 1 >= end:
                    break # может, оно для чего-то более важного
                _next = data[i + 1]

                # это массив
                if isinstance(_next, RawOperand):
                    if isinstance(_next.thing, TokenRawLiteral):
                        lenght = TokenLiteral.from_raw(_next.thing)
                        if lenght.type != TokenLiteralTypes.Int:
                            break
                        modifiers.append(Type.ModifierArray(int(lenght.value)))
                        i += 2
                    else:
                        break

                # это срез
                elif isinstance(_next, (Separator, SquareBracketClose)):
                    dims = 1
                    i += 1
                    break_true = False
                    while i < end:
                        match data[i]:
                            case Separator():
                                dims += 1
                            case SquareBracketClose():
                                break
                            case _:
                                break_true = True
                                break
                        i += 1
                    if break_true:
                        break
                    modifiers.append(Type.ModifierSlise(dims))

                else:
                    break

            # это должен быть модификатор указателя
            case RawOperator():
                if cur.symbol != '*':
                    break
                modifiers.append(Type.ModifierPointer())
            case _:
                break
        i += 1
    # если обработка завершилась неожиданно
    i -= 1
    if depth != 0:
        raise OurSyntaxError('Неожиданный токен, ожидались модификаторы типа', cur.origin)

    return i, Type(simple, modifiers, data[start].origin + data[i].origin)


