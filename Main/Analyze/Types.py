from ...Definitions.Tokens import *
from ...Definitions import TypesShortener as types


"""
Этот модуль нужен для трёх штук - первое, находить общий тип для бинарный операндов, второе - проверять, возможно ли
какая-то операция с каким-то типом, и третье - возможно ли преобразование какого-то типа в какому-то
"""

__all__ = (
    'get_common_type_binary',
    'get_common_type_prefix',
    'get_common_type_postfix',
    'get_result_type_binary',
    'get_result_type_prefix',
    'get_result_type_postfix',
    'turn_into_int',
    'get_common_type_array_creation',
    'get_magic_thing_binary',
    'get_magic_thing_prefix',
    'get_magic_thing_postfix',
)


def is_any_float(t1: Type, t2: Type) -> bool:
    assert t1.is_simple_base and t1.is_simple_base
    return t1.simple.type in BaseTypesTypes.Floating or t2.simple.type in BaseTypesTypes.Floating


def lead_to_float(t1: Type, t2: Type) -> Type:
    assert t1.is_simple_base and t1.is_simple_base
    i1 = BaseTypesTypes.Floating.index(t1.simple.type) if t1.simple.type in BaseTypesTypes.Floating else -1
    i2 = BaseTypesTypes.Floating.index(t2.simple.type) if t2.simple.type in BaseTypesTypes.Floating else -1
    return Type(Type.SimpleTypeBase(BaseTypesTypes.Floating[max(i1, i2)]), [])


def lead_to_int(t1: Type, t2: Type) -> Type:
    assert t1.is_simple_base and t1.is_simple_base
    t1t = t1.simple.type
    t2t = t2.simple.type
    cond1 = t1t in BaseTypesTypes.Unsigned
    cond2 = t2t in BaseTypesTypes.Unsigned
    # если есть беззнаковое
    if cond1 or cond2:
        # оба числа беззнаковыe, результат - тоже
        if cond1 and cond2:
            i1 = BaseTypesTypes.Unsigned.index(t1t)
            i2 = BaseTypesTypes.Unsigned.index(t2t)
            return Type(Type.SimpleTypeBase(BaseTypesTypes.Unsigned[max(i1, i2)]), [])
        # рассмотрим что у нас за беззаковое
        uns = t1t if cond1 else t2t
        match uns:
            case BaseTypes.bool:
                res = BaseTypes.int8
            case BaseTypes.uint8:
                res = BaseTypes.int16
            case BaseTypes.uint16:
                res = BaseTypes.int32
            case BaseTypes.uint32:
                res = BaseTypes.int64
            case BaseTypes.uint64:
                # особое правило - вместе с uint64 всё будет uint64 кроме флоатов
                return Type(Type.SimpleTypeBase(BaseTypes.uint64), [])
            case _:
                raise ValueError('Что-то пошло не так')
        # приводим к более общему знаковому типу
        if cond1:
            t1t = res
        else:
            t2t = res
        # теперь оба типа - знаковые
    # берём знаковое
    i1 = BaseTypesTypes.Signed.index(t1t)
    i2 = BaseTypesTypes.Signed.index(t2t)
    return Type(Type.SimpleTypeBase(BaseTypesTypes.Signed[max(i1, i2)]), [])


def is_classes_operation_allowed(
        type: Type,
        operation: TokenOperatorBinaryTypes | TokenOperatorPrefixTypes | TokenOperatorPostfixTypes) -> bool:
    assert isinstance(type.simple, Type.SimpleTypeClassInstance)
    class_ = type.cls
    assert isinstance(class_, ControlClass)

    if operation in TokenOperatorPrefixTypes:
        if operation == TokenOperatorPrefixTypes.ArfmUnMin:
            if '__neg__' in class_.magic_methods:
                return True
        elif operation in TokenOperatorsTypes.Logical:
            if '__bool__' in class_.magic_methods:
                return True

    if operation in TokenOperatorBinaryTypes:
        if (
                (operation == TokenOperatorBinaryTypes.ArfmAdd and '__add__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ArfmSub and '__sub__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ArfmMul and '__mul__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ArfmDiv and '__div__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ArfmMod and '__mod__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprEq and '__eq__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprNEq and '__ne__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprLess and '__lt__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprLessOrEq and '__le__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprMore and '__gt__' in class_.magic_methods) or
                (operation == TokenOperatorBinaryTypes.ComprMoreOrEq and '__ge__' in class_.magic_methods) or
                (operation in TokenOperatorsTypes.Logical and '__bool__' in class_.magic_methods)
        ):
            return True
    return False


# ========== Бинарные ==========
def get_common_type_binary(
        oper_type: TokenOperatorBinaryTypes,
        type1: Type, type2: Type,
        origin: TokenOrigin) -> tuple[Type, Type]:
    """
    Ищет тип(если есть) к которому нужно привести оба операнда для проведения операции, также проверяет, возможно ли это.
    """
    _type1, _type2 = type1.full_type, type2.full_type


    # особая ветка логики - указатели
    if _type1.is_mod_pointer or _type2.is_mod_pointer:
        if _type1.is_mod_pointer and _type2.is_mod_pointer:
            if oper_type in (TokenOperatorBinaryTypes.ComprEq, TokenOperatorBinaryTypes.ComprNEq):
                if _type1 == _type2:
                    return type1, type2
                else:
                    raise SemanticError(f'Сравнивать можно только указатели одинаковых типов: {type1}, {type2}', origin)
            else:
                raise SemanticError('Два указателя можно только сравнить: {type1}, {type2}', origin)

        if _type1.is_mod_pointer:
            pointer, integer = type1, type2
            _integer = type2
        else:
            pointer, integer = type2, type1
            _integer = type1

        if not (
                _integer.is_mod_usual and
                _integer.is_simple_base and
                _integer.simple.type in BaseTypesTypes.Integer
        ):
            raise SemanticError(f'Указатель {pointer} можно двигать только на '
                                f'целочисленный тип, был дан {integer}', origin)

        if oper_type not in (TokenOperatorBinaryTypes.ArfmAdd, TokenOperatorBinaryTypes.ArfmSub):
            raise SemanticError(f'Неправильная операция: {oper_type.value.symbol}. '
                                f'Указатель можно только двигать(суммируя или вычитая)', origin)

        if _type1.is_mod_pointer:
            return type1, type2
        else:
            return type2, type1

    # базовые классы и их магические методы
    if _type1.is_mod_usual and _type1.is_simple_class_instance and _type2.is_mod_usual and _type2.is_simple_class_instance and _type1 == _type2:
        if is_classes_operation_allowed(_type1, oper_type):
            return type1, type2

    # сравнения перечислений, можно сравнивать 2 перечисления одинакового типа
    if _type1.is_mod_usual and _type1.is_simple_enum_instance and _type2.is_mod_usual and _type2.is_simple_enum_instance and _type1 == _type2:
        if oper_type in (TokenOperatorBinaryTypes.ComprEq, TokenOperatorBinaryTypes.ComprNEq):
            return type1, type2

    # теперь - только базовые типы без модификаторов
    if not (type1.is_mod_usual and type2.is_mod_usual and type1.is_simple_base and type2.is_simple_base):
        raise SemanticError(f'Операция {oper_type.value.symbol} не работает с типами {type1} и {type2}', origin)

    # особый случай - % только с целыми числами
    if oper_type == TokenOperatorBinaryTypes.ArfmMod:
        if is_any_float(type1, type2):
            raise SemanticError(f'Операция {oper_type.value.symbol}  работает только '
                                f'с целочисленными типами, были даны {type1} и {type2}', origin)
        need = lead_to_int(type1, type2)

    # просто арифметика, если один из них флоат - то это флоат, в другом случае это целое число
    elif oper_type in TokenOperatorsTypes.Arithmetic or oper_type in TokenOperatorsTypes.Comparison:
        if is_any_float(type1, type2):
            need = lead_to_float(type1, type2)
        else:
            need = lead_to_int(type1, type2)

    # битовые операции, только целочисленное
    elif oper_type in TokenOperatorsTypes.BitwiseShifts or oper_type in TokenOperatorsTypes.Bitwise:
        if is_any_float(type1, type2):
            raise SemanticError(f'Битовые операции работают только с целочисленными '
                                f'типами, были даны {type1} и {type2}', origin)
        need = lead_to_int(type1, type2)

    # логические, только булев
    elif oper_type in TokenOperatorsTypes.Logical:
        need = t_bool

    else:
        raise ValueError('что-то пошло не так')

    return type1 if _type1 == need else need, _type2 if _type2 == need else need


def get_result_type_binary(oper_type: TokenOperatorBinaryTypes, type1: Type, type2: Type) -> Type:
    """
    Нужно, чтобы понять, какой тип будет у операции вида oper_type с операндами типа type1 и type2
    """
    # это указатель в сдвиге указателей, вернём его
    if type1.full_type != type2.full_type:
        if type1.full_type.is_mod_pointer:
            return type1
        else:
            return type2

    # типы равны, и это обычные операции
    if oper_type in TokenOperatorsTypes.Arithmetic or \
            oper_type in TokenOperatorsTypes.BitwiseShifts or \
            oper_type in TokenOperatorsTypes.Bitwise:
        return type1
    elif oper_type in TokenOperatorsTypes.Comparison or \
            oper_type in TokenOperatorsTypes.Logical:
        return t_bool


def get_magic_thing_binary(oper_type: TokenOperatorBinaryTypes, type1: Type, type2: Type) -> tuple[str, Type, Type]:
    assert type1 == type2
    assert type1.is_mod_usual
    assert type1.is_simple_class_instance
    match oper_type:
        case TokenOperatorBinaryTypes.ArfmAdd: return '__add__', types.func([type1, type1], [type1]), type1
        case TokenOperatorBinaryTypes.ArfmSub: return '__sub__', types.func([type1, type1], [type1]), type1
        case TokenOperatorBinaryTypes.ArfmMul: return '__mul__', types.func([type1, type1], [type1]), type1
        case TokenOperatorBinaryTypes.ArfmDiv: return '__div__', types.func([type1, type1], [type1]), type1
        case TokenOperatorBinaryTypes.ArfmMod: return '__mod__', types.func([type1, type1], [type1]), type1
        case TokenOperatorBinaryTypes.ComprEq: return '__eq__', types.func([type1, type1], [types.bool]), types.bool
        case TokenOperatorBinaryTypes.ComprNEq: return '__ne__', types.func([type1, type1], [types.bool]), types.bool
        case TokenOperatorBinaryTypes.ComprLess: return '__lt__', types.func([type1, type1], [types.bool]), types.bool
        case TokenOperatorBinaryTypes.ComprLessOrEq: return '__le__', types.func([type1, type1], [types.bool]), types.bool
        case TokenOperatorBinaryTypes.ComprMore: return '__gt__', types.func([type1, type1], [types.bool]), types.bool
        case TokenOperatorBinaryTypes.ComprMoreOrEq: return '__ge__', types.func([type1, type1], [types.bool]), types.bool
        case _:
            raise ValueError('')


# ========== Префиксные ==========
def get_common_type_prefix(oper_type: TokenOperatorPrefixTypes, type1: Type, origin: TokenOrigin) -> Type:
    _type1 = type1.full_type

    if _type1.is_mod_usual and _type1.is_simple_class_instance:
        if is_classes_operation_allowed(_type1, oper_type):
            return type1

    if not (_type1.is_mod_usual and _type1.is_simple_base):
        raise SemanticError(f'Операция {oper_type.value.symbol} работает '
                            f'только с базовыми типами без модификаторов', origin)

    t1t = _type1.simple.type

    if oper_type in TokenOperatorsTypes.Arithmetic:
        return type1

    elif oper_type in TokenOperatorsTypes.Bitwise:
        if t1t in BaseTypesTypes.Floating:
            raise SemanticError(f'Битовые операции работают только с целочисленными '
                                f'типами, был дан {type1}', origin)
        return type1

    elif oper_type in TokenOperatorsTypes.Logical:
        return t_bool

    else:
        raise ValueError('что-то пошло не так')


def get_result_type_prefix(oper_type: TokenOperatorPrefixTypes, type_n: Type) -> Type:
    if type_n.full_type.is_simple_class_instance:
        return type_n

    if oper_type in TokenOperatorsTypes.Arithmetic or \
            oper_type in TokenOperatorsTypes.Bitwise:
        return type_n
    elif oper_type in TokenOperatorsTypes.Logical:
        return t_bool


def get_magic_thing_prefix(oper_type: TokenOperatorPrefixTypes, type1: Type) -> tuple[str, Type, Type]:
    assert type1.is_mod_usual
    assert type1.is_simple_class_instance
    match oper_type:
        case TokenOperatorBinaryTypes.ArfmAdd: return '__neg__', types.func([type1], [type1]), type1
        case _:
            raise ValueError('')


# ========== Постфиксные ==========
def get_common_type_postfix(oper_type: TokenOperatorPostfixTypes, type1: Type, origin: TokenOrigin) -> Type:
    _type1 = type1.full_type

    # может, на будущее
    if _type1.is_mod_usual and type1.is_simple_class_instance:
        if is_classes_operation_allowed(_type1, oper_type):
            return type1

    # одинокое разыменование
    if oper_type == TokenOperatorPostfixTypes.Dereferencing:
        if _type1.is_mod_pointer:
            return type1
    raise SemanticError(f'Разыменование работает только с указателем, был дан {type1}', origin)


def get_result_type_postfix(oper_type: TokenOperatorPostfixTypes, type_n: Type) -> Type:
    if type_n.full_type.is_simple_class_instance:
        return type_n

    if oper_type == TokenOperatorPostfixTypes.Dereferencing:
        if type_n.is_mod_pointer:
            return type_n.without_one_modifier()
    return type_n


def get_magic_thing_postfix(oper_type: TokenOperatorPrefixTypes, type1: Type) -> tuple[str, Type, Type]:
    assert type1.is_mod_usual
    assert type1.is_simple_class_instance
    match oper_type:
        case _:
            raise ValueError('')


# ========== Общий тип массива ==========
def turn_into_int(type1: Type, origin: TokenOrigin, signed_allowed: bool = False) -> Type:
    """
    Делает из типа int__ если нужно, и проверяет возможно ли это вообще. Нужен для индексов
    """
    _type = type1.full_type
    if not (_type.is_mod_usual and _type.is_simple_base and _type.simple.type in BaseTypesTypes.Integer):
        raise SemanticError(f'Индексом могут быть только численные типы, был дан {type1}', origin)

    if signed_allowed:
        return type1

    elif not signed_allowed:
        if _type.simple.type in BaseTypesTypes.Unsigned:
            return _type
        elif _type.simple.type in BaseTypesTypes.Integer:
            return Type(Type.SimpleTypeBase(BaseTypes.uint64), [])


def get_common_type_array_creation(type1: Type, type2: Type, origin: TokenOrigin) -> Type:
    _type1, _type2 = type1.full_type, type2.full_type

    if _type1 == _type2:
        return type1

    if _type1.is_mod_pointer or _type2.is_mod_pointer:
        raise SemanticError(f'Указатели не приводятся друг к другу неявно, так что в '
                            f'массиве их типы должны быть равны, были даны {type1}, {type2}', origin)

    elif _type1.is_mod_slize or _type2.is_mod_slize:
        raise SemanticError(f'Срезы не приводятся друг к другу неявно, так что в '
                            f'массиве их типы должны быть равны, были даны {type1}, {type2}', origin)

    elif _type1.is_mod_array or _type2.is_mod_array:
        if _type1.is_mod_array and _type2.is_mod_array and _type1.length == _type2.length:
            # убираем все измерения и берём тим элемента
            dims = []
            _type1 = type1
            _type2 = type2
            while _type1.is_mod_array and _type2.is_mod_array:
                dims.append(_type1.length)
                # тут мы пытаемся сохранить псевдоним
                if type1.modifiers:
                    _type1 = type1.without_one_modifier()
                else:
                    _type1 = _type1.without_one_modifier()
                if type1.modifiers:
                    _type2 = type2.without_one_modifier()
                else:
                    _type2 = _type2.without_one_modifier()

            # теперь, приводим типы элементов
            result = get_common_type_array_creation(_type1, _type2, origin)
            mods_append = [
                Type.ModifierArray(d) for d in dims
            ][::-1]
            return Type(
                result.simple, result.modifiers + mods_append, result.origin
            )
        else:
            raise SemanticError(f'В создании массива внутренние массивы для привидения должны иметь '
                                f'одинаковую длину и приводимый тип элемента, были даны {type1}, {type2}', origin)
    else:
        if _type1.is_simple_func and _type2.is_simple_func:
            raise SemanticError(f'Функции не приводятся друг к другу неявно, так что в '
                                f'массиве их типы должны быть равны, были даны {type1}, {type2}', origin)
        elif _type1.is_simple_base and _type2.is_simple_base:
            if is_any_float(type1, type2):
                return lead_to_float(type1, type2)
            return lead_to_int(type1, type2)
        else:
            raise SemanticError(f'Данные базовые типы не приводятся друг к другу неявно {type1}, {type2}', origin)

