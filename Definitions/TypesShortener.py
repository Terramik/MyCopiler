from .Tokens import Type
from .Enums import BaseTypes

"""
Цель модуля - дать удобные имена для типов, и вообще сделать это дело удобнее.
"""

bool = Type(Type.SimpleTypeBase(BaseTypes.bool), [])
int64 = Type(Type.SimpleTypeBase(BaseTypes.int64), [])
int32 = Type(Type.SimpleTypeBase(BaseTypes.int32), [])
int16 = Type(Type.SimpleTypeBase(BaseTypes.int16), [])
int8 = Type(Type.SimpleTypeBase(BaseTypes.int8), [])
uint64 = Type(Type.SimpleTypeBase(BaseTypes.uint64), [])
uint32 = Type(Type.SimpleTypeBase(BaseTypes.uint32), [])
uint16 = Type(Type.SimpleTypeBase(BaseTypes.uint16), [])
uint8 = Type(Type.SimpleTypeBase(BaseTypes.uint8), [])
float64 = Type(Type.SimpleTypeBase(BaseTypes.float64), [])
float32 = Type(Type.SimpleTypeBase(BaseTypes.float32), [])

char = uint8
cher_ptr = Type(Type.SimpleTypeBase(BaseTypes.uint8), [Type.ModifierPointer()])
int8p = Type(Type.SimpleTypeBase(BaseTypes.int8), [Type.ModifierPointer()])
str = Type(Type.SimpleTypeBase(BaseTypes.uint8), [Type.ModifierSlise(1)])


def mod_pointer() -> Type.ModifierPointer:
    return Type.ModifierPointer()


def mod_array(size: int) -> Type.ModifierArray:
    return Type.ModifierArray(size)


def mod_slice(dims: int) -> Type.ModifierSlise:
    return Type.ModifierSlise(dims)


def add_modifiers(type: Type, mods: [Type.ModifierABS]) -> Type:
    return Type(type.simple, type.modifiers + mods)


def func(args: list[Type], res: list[Type]) -> Type:
    return Type(Type.SimpleTypeFunc(args, res), [])


def class_instance(class_: 'ControlClass'):
    return Type(Type.SimpleTypeClassInstance(class_), [])


def class_type(class_: 'ControlClass'):
    return Type(Type.SimpleTypeClass(class_), [])

