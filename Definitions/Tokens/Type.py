from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from typing import Union
from ..Base import *
from ..Enums import BaseTypes, BaseTypesTypes
from ..Exceptions import SemanticError


class Type:
    """
    Отображает тип (int|float|bool[10]) чего-то
    """
    __slots__ = ('_simple', '_modifiers', '_raw_name', 'origin')

    @dataclass(slots=True, frozen=True)
    class Typedef:
        """Должен служить обёрткой, заворачивающие 1 типы в другие"""
        type: Type
        name: str

        def conj(self, mods: list[Type.ModifierABS]) -> Type:
            """Склеивает тип typedef'а и новые модификаторы"""
            return Type(self.type.simple, self.type.modifiers + mods)

    # эти штуки должны отображать основную, базовую часть типа тип (то есть, int64 в int64[])
    class SimpleTypeABC(ABC):
        pass

    @dataclass(slots=True, frozen=True)
    class SimpleTypeRaw(SimpleTypeABC):
        raw_name: str
        indexes: list[str] = field(default_factory=list)

        def __repr__(self):
            return self.raw_name + ''.join(f'.{n}' for n in self.indexes)

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeRaw):
                return False
            return self.raw_name == other.raw_name and self.indexes == other.indexes

    @dataclass(slots=True, frozen=True)
    class SimpleTypeBase(SimpleTypeABC):
        type: BaseTypes

        def __repr__(self):
            return self.type.value

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeBase):
                return False
            return self.type == other.type

    @dataclass(slots=True, frozen=True)
    class SimpleTypeFunc(SimpleTypeABC):
        arguments: list[Type]
        results: list[Type]

        def __repr__(self):
            return f'func ({', '.join(map(repr, self.arguments))}) -> ({', '.join(map(repr, self.results))})'

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeFunc):
                return False
            return self.arguments == other.arguments and self.results == other.results

        def __hash__(self):
            return hash((tuple(self.results), tuple(self.arguments)))

    @dataclass(slots=True, frozen=True)
    class SimpleTypeTypedef(SimpleTypeABC):
        link: Type.Typedef
        full_type: Type

        def __repr__(self):
            return self.link.name

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeTypedef):
                return False
            return self.full_type == other.full_type

    @dataclass(slots=True, frozen=True)
    class SimpleTypeClassInstance(SimpleTypeABC):
        """Отображает тип экзепляра класса"""
        class_: 'ControlClass'

        def __repr__(self): return self.class_.name

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeClassInstance):
                return False
            return self.class_ == other.class_

        def __hash__(self): return hash(self.class_)

    @dataclass(slots=True, frozen=True)
    class SimpleTypeClass(SimpleTypeABC):
        """Отображает тип класса"""
        class_: 'ControlClass'

        def __repr__(self): return self.class_.name

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeClass):
                return False
            return self.class_ == other.class_

        def __hash__(self): return hash(self.class_)


    @dataclass(slots=True, frozen=True)
    class SimpleTypeEnum(SimpleTypeABC):
        """Отображает тип перечисление(контейнера состояний)"""
        enum: 'ControlEnum'

        def __repr__(self): return self.enum.name

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeEnum):
                return False
            return self.enum == other.enum

        def __hash__(self): return hash(self.enum)


    @dataclass(slots=True, frozen=True)
    class SimpleTypeEnumInstance(SimpleTypeABC):
        """Отображает тип перечисление(самого состояний)"""
        enum: 'ControlEnum'

        def __repr__(self): return self.enum.name

        def __eq__(self, other):
            if not isinstance(other, Type.SimpleTypeEnumInstance):
                return False
            return self.enum == other.enum

        def __hash__(self): return hash(self.enum)



    # эти штуки должны дополнительную, модифицированную часть типа (то есть, [] в int64[])
    class ModifierABS(ABC):
        pass

    @dataclass(slots=True, frozen=True)
    class ModifierPointer(ModifierABS):
        def __repr__(self):
            return '*'

        def __eq__(self, other):
            return isinstance(other, Type.ModifierPointer)

    @dataclass(slots=True, frozen=True)
    class ModifierArray(ModifierABS):
        length: int

        def __repr__(self):
            return f'[{self.length}]'

        def __eq__(self, other):
            if not isinstance(other, Type.ModifierArray):
                return False
            return self.length == other.length

    @dataclass(slots=True, frozen=True)
    class ModifierSlise(ModifierABS):
        dimensions: int

        def __repr__(self):
            return f'[{',' * (self.dimensions - 1)}]'

        def __eq__(self, other):
            if not isinstance(other, Type.ModifierSlise):
                return False
            return self.dimensions == other.dimensions

    def __init__(
            self,
            simple: SimpleTypeABC,
            modifiers: list[ModifierABS],
            origin: TokenOrigin = zero_origin
    ):
        self._simple = simple
        # модификаторы будут храниться в прямом порядке:
        # int64*[10] будет Type(BaseTypes.int64, [Type.ModifierPointer(), Type.ModifierArray(10)])
        self._modifiers = tuple(modifiers)
        self.origin = origin

    @classmethod
    def from_raw(cls, raw_name: str, modifiers: list[ModifierABS], origin: TokenOrigin) -> Type:
        return Type(Type.SimpleTypeRaw(raw_name), modifiers, origin)

    @classmethod
    def from_typedef(cls, typedef: Type.Typedef, modifiers: list[ModifierABS], origin: TokenOrigin) -> Type:
        return Type(Type.SimpleTypeTypedef(typedef, typedef.conj(modifiers)), modifiers, origin)

    @property
    def is_mod_pointer(self) -> bool:
        _self = self.full_type
        return isinstance(_self._modifiers[-1], _self.ModifierPointer) if _self._modifiers else False

    @property
    def is_mod_array(self) -> bool:
        _self = self.full_type
        return isinstance(_self._modifiers[-1], _self.ModifierArray) if _self._modifiers else False

    @property
    def is_mod_slize(self) -> bool:
        _self = self.full_type
        return isinstance(_self._modifiers[-1], _self.ModifierSlise) if _self._modifiers else False

    @property
    def is_mod_usual(self) -> bool:
        _self = self.full_type
        return not _self._modifiers

    @property
    def is_simple_raw(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeRaw)

    @property
    def is_simple_base(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeBase)

    @property
    def is_simple_func(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeFunc)

    @property
    def is_simple_typedef(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeTypedef)

    @property
    def is_simple_class_instance(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeClassInstance)

    @property
    def is_simple_class(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeClass)

    @property
    def is_simple_enum_instance(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeEnumInstance)

    @property
    def is_simple_enum(self) -> bool:
        return isinstance(self._simple, Type.SimpleTypeEnum)

    @property
    def full_type(self) -> Type:
        """Возвращает полный тип без всяких typedef'ов"""
        if isinstance(self._simple, Type.SimpleTypeTypedef):
            return self._simple.full_type
        elif isinstance(self._simple, Type.SimpleTypeFunc):
            return Type(Type.SimpleTypeFunc(
                [t.full_type for t in self._simple.arguments],
                [t.full_type for t in self._simple.results],
            ), list(self._modifiers))
        else:
            return self

    def __repr__(self):
        return f'{self._simple}{''.join(map(repr, self._modifiers))}'

    def with_name(self, name: str) -> str:
        return f'var {name} ({repr(self)})'

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        _self = self.full_type
        other = other.full_type
        return self._simple == other._simple and self._modifiers == other._modifiers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self._simple, self._modifiers))

    @property
    def modifiers(self) -> list[ModifierABS]:
        _self = self.full_type
        return list(_self._modifiers)

    @property
    def simple(self) -> Type.SimpleTypeABC:
        return self._simple

    @simple.setter
    def simple(self, new_simple: SimpleTypeABC):
        self._simple = new_simple

    @property
    def length(self) -> int:
        _self = self.full_type
        assert _self._modifiers
        last = _self._modifiers[-1]
        assert isinstance(last, Type.ModifierArray)
        return last.length

    @property
    def dimensions(self) -> int:
        _self = self.full_type
        assert _self._modifiers
        last = _self._modifiers[-1]
        assert isinstance(last, Type.ModifierSlise)
        return last.dimensions
    
    @property
    def cls(self) -> 'ControlClass':
        assert self.full_type.is_simple_class_instance or self.full_type.is_simple_class
        return self.full_type.simple.class_
    
    @property
    def enum(self) -> 'ControlEnum':
        assert self.full_type.is_simple_enum or self.full_type.is_simple_enum_instance
        return self.full_type.simple.enum
    
    def add_modifier(self, modifier: ModifierABS) -> Type:
        mod = self.modifiers
        mod.append(modifier)
        return Type(self._simple, mod, self.origin)

    def get_dims(self):
        if self.is_mod_array:
            n = -len(self._modifiers)
            i = -1
            while i >= n and isinstance(self._modifiers[i], Type.ModifierArray):
                i -= 1
            return -i - 1
        elif self.is_mod_slize:
            return self.dimensions
        else:
            return 0

    def without_one_dimension(self) -> Type:
        _self = self if self._modifiers else self.full_type
        assert _self.is_mod_array or _self.is_mod_slize
        mod = list(_self._modifiers[:])
        if _self.is_mod_array:
            mod = mod[:-1]
        else:
            dims = _self.dimensions
            if dims == 1:
                mod = mod[:-1]
            else:
                mod[-1] = Type.ModifierSlise(dims - 1)
        return Type(_self._simple, mod, _self.origin)

    def without_one_modifier(self) -> Type:
        _self = self if self._modifiers else self.full_type
        assert _self._modifiers
        return Type(_self._simple, _self.modifiers[:-1], _self.origin)

    def copy(self) -> Type:
        return Type(self._simple, self.modifiers, self.origin)

    def is_castable_implicitly(self, cast_to: Type) -> bool:
        """Проверяет, возможно ли преобразование типа cast_from в тип cast_to неявно"""
        _self = self.full_type
        cast_to = cast_to.full_type

        if _self == cast_to:
            return True

        if _self.is_mod_usual and cast_to.is_mod_usual:
            if _self.is_simple_base and cast_to.is_simple_base:
                if _self._simple.type in BaseTypesTypes.Numeric and cast_to.simple.type in BaseTypesTypes.Numeric:
                    return True
            # класс с __bool__ можно неявно преобразовать
            if _self.is_simple_class_instance and cast_to == t_bool and _self.cls.is_bool:
                return True

        return False

    def is_castable_explicitly(self, cast_to: Type) -> bool:
        """Проверяет, возможно ли преобразование типа cast_from в тип cast_to явно"""
        _self = self.full_type
        cast_to = cast_to.full_type
        # указатель в указатель
        if _self.is_mod_pointer and cast_to.is_mod_pointer:
            return True

        # указатель в число
        if _self.is_mod_pointer and \
                cast_to.is_mod_usual and cast_to.is_simple_base and cast_to.simple.type in BaseTypesTypes.Integer:
            return True

        # указатель на функцию в число
        if _self.is_mod_slize and _self.is_simple_func and \
                cast_to.is_mod_usual and cast_to.is_simple_base and cast_to.simple.type in BaseTypesTypes.Integer:
            return True

        # число в указатель
        if _self.is_mod_usual and _self.is_simple_base and _self.simple.type in BaseTypesTypes.Integer and \
                cast_to.is_mod_pointer:
            return True

        # число в указатель на функцию
        if _self.is_mod_usual and _self.is_simple_base and _self.simple.type in BaseTypesTypes.Integer and \
                cast_to.is_mod_usual and cast_to.is_simple_func:
            return True

        # срез в указатель
        if self.is_mod_slize and cast_to.is_mod_pointer:
            return True
        # указатель в срез делается через срез

        # массив в массив, если элементы приводимы
        if _self.is_mod_array and cast_to.is_mod_array:
            # совпадает ли длина
            if _self.length != cast_to.length:
                return False
            # можно ли привести сами элементы массива друг в друга
            return _self.without_one_modifier().is_castable_explicitly(cast_to.without_one_modifier())

        if _self.is_mod_usual and cast_to.is_mod_usual:
            # число в число
            if _self.is_simple_base and cast_to.is_simple_base:
                if _self._simple.type in BaseTypesTypes.Numeric and cast_to.simple.type in BaseTypesTypes.Numeric:
                    return True
            # класс с __bool__ можно и явно преобразовать
            if _self.is_simple_class_instance and cast_to == t_bool and _self.cls.is_bool:
                return True

        return False

    def turn_into_int(self, signed_allowed: bool = False) -> Type | None:
        """
        Делает из типа int__ если нужно, и проверяет возможно ли это вообще. Нужен для индекса
        """
        _self = self.full_type
        if _self.is_mod_usual and _self.is_simple_base:
            if signed_allowed:
                if _self.simple.type in BaseTypesTypes.Integer:
                    return self

            elif not signed_allowed:
                if _self.simple.type in BaseTypesTypes.Unsigned:
                    return self
                elif _self.simple.type in BaseTypesTypes.Integer:
                    return Type(Type.SimpleTypeBase(BaseTypes.uint64), [])


class ErrorType(Type):
    """
    Тип для узла с ошибкой, указывает что он не валиден и что лишних ошибок кидать не надо.
    """
    def __init__(self, origin: TokenOrigin | None):
        self.origin = origin


t_bool = Type(Type.SimpleTypeBase(BaseTypes.bool), [])
t_error = ErrorType(zero_origin)
