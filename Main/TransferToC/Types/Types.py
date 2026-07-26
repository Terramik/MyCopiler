import types
from functools import lru_cache
from .Simple import *
from .Pointer import transfer_pointer
from .Array import transfer_array, transfer_array_index
from .Slice import transfer_slice, transfer_slice_index
from .Function import transfer_func
from .Classes import transfer_class_itself, transfer_class_instance
from .Enums import transfer_enum


__all__ = ('transfer_all_types',)


"""
Эти функция нужны для собрания всех сложных типов и 
генерации структур и обслуживающих функций для них
"""


@lru_cache()
def count(_type: Type) -> int:
    """
    Считаем "сложность" типа - насколько сложные типы нужны для создания этого типа.
    """
    # основной тип
    res = 0
    match _type.simple:
        case Type.SimpleTypeBase():
            res += 0

        case Type.SimpleTypeFunc():
            assert isinstance(_type.simple, Type.SimpleTypeFunc)
            res += max(
                max((
                    count(arg) for arg in _type.simple.arguments
                )) if _type.simple.arguments else 0,
                max((
                    count(res) for res in _type.simple.results
                )) if _type.simple.results else 0
            ) + 1

        case Type.SimpleTypeClassInstance():
            cls = _type.cls
            res += (max((  # поля экзепляра
                    count(v.type) for v in cls.instance_field
            )) if cls.instance_field else 0) + 1

        case Type.SimpleTypeClass():
            cls = _type.cls
            # экзепляр и поля класса
            res += max(
                count(
                    Type(Type.SimpleTypeClassInstance(cls), [])
                ),
                max((
                    count(v.type) for v in cls.class_field
                ))
            ) + 1

        case Type.SimpleTypeEnum() | Type.SimpleTypeEnumInstance():
            res = 1 # так как они - просто числа
        case _:
            raise ValueError('')

    # модификаторы
    for m in _type.modifiers:
        if isinstance(m, Type.ModifierSlise):
            res += m.dimensions
        else:
            res += 1

    return res


def transfer_all_types(file: TextIO, types: set[types], data: DataContainer):
    """
    Генерирует си-структуры для типов. Также функции для их индексации(если это массив или срез), и
    структуры для получения множественных аргументов из функций.
    """

    # получаем сложность
    types = ((t, count(t)) for t in types)
    # пропускаем типы с нулевой сложностью
    types = filter(lambda x: x[1] != 0, types)
    # сортируем
    types = sorted(types, key=lambda x: x[1])
    # и берём только сам тип
    types = (t[0] for t in types)

    for t in types:
        assert isinstance(t, Type)
        if t.is_mod_pointer:
            transfer_pointer(file, data, t)
        elif t.is_mod_array:
            transfer_array(file, data, t)
            transfer_array_index(file, data, t)
        elif t.is_mod_slize:
            transfer_slice(file, data, t)
            transfer_slice_index(file, data, t)
        elif t.is_mod_usual:
            if t.is_simple_class_instance:
                transfer_class_instance(file, data, t)
            elif t.is_simple_class:
                transfer_class_itself(file, data, t)
            elif t.is_simple_func:
                transfer_func(file, data, t)
            elif t.is_simple_enum:
                transfer_enum(file, data, t)
            elif t.is_simple_enum_instance:
                pass # чтобы не кидать ошибку, а так оно обработано в transfer_enum
            else:
                raise ValueError('')
        else:
            raise ValueError('Что-то пошло не так')




