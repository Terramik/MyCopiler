from __future__ import annotations
from enum import Enum
from typing import Union
from .Tokens import *
from uuid import uuid4

'''
Эти штуки будут служить обработчиками областей видимости, хранить функции и переменны
Типы областей видимости завият от того, чем оно было создано (функция, цикл, или просто { ... })
это нужно для того, чтобы можно было понять, к чему относяться ключевые слова вроде return или break
'''

__all__ = ('Scope',)
scope_creator = Union[
    ControlCodeBlock,
    ControlFunctionDefinition,
    tuple[ControlIf, ControlCodeBlock],
    ControlWhile,
    ControlClass,
]


class Scope:
    __slots__ = ('type', 'parent', 'creator', 'children', 'variables', 'functions', 'typedefs', 'classes', 'enums')

    class Types(Enum):
        Function = 'f'
        Usual = 'u'
        Global = 'g'
        Conditional = 'if'
        Cycle = 'c'
        Class = 'cls'

    def __init__(
            self,
            scope_type: Types,
            creator: scope_creator,
            parent: Scope | None):
        self.type = scope_type
        self.creator = creator
        self.parent = parent
        self.children: list[Scope] = []
        # возможно, вы спросите, почему бы не использовать словари для быстрого поиска по имени? Потому что я не
        # хочу хранить имя чего-то где-то кроме самого объекта, и придумывать всякие прикольные дескрипторы и прочее.
        self.variables: list[TokenOperatorVariableDefinition] = []
        self.functions: list[ControlFunctionDefinition] = []
        self.typedefs: list[ControlTypedef] = []
        self.classes: list[ControlClass] = []
        self.enums: list[ControlEnum] = []

    def add_child(self, child: 'Scope'):
        self.children.append(child)

    def add_variable(self, variable: TokenOperatorVariableDefinition):
        self.variables.append(variable)

    def add_function(self, function: ControlFunctionDefinition):
        self.functions.append(function)

    def add_typedef(self, typedef: ControlTypedef):
        self.typedefs.append(typedef)

    def add_class(self, class_: ControlClass):
        self.classes.append(class_)

    def add_enum(self, enum: ControlEnum):
        self.enums.append(enum)

    def find_variable_in_cur_scope(self, name: str) -> None | TokenOperatorVariableDefinition:
        for var in self.variables:
            if var.name == name:
                return var

    def find_variable(self, name: str, add_to_f: bool) -> None | tuple[TokenOperatorVariableDefinition, bool]:
        """
        Ищет объявление переменной по высшим областям видимости. если add_to_f установлен на true, то при выходе из
        первой области видимости, созданной функцией, добавит искомую переменную в outer_variables функции.
        Возвращаемые значения - это само объявление переменной и то, является ли переменная внешней(не объявленной
        в области видимости ближайшей функции)
        """
        fs = []
        cur_scope = self
        while cur_scope is not None:
            v = cur_scope.find_variable_in_cur_scope(name)

            if cur_scope.type == self.Types.Function:
                fs.append(cur_scope.creator)

            if v:
                is_nonlocal: bool
                if (
                        (cur_scope.type == Scope.Types.Global) or
                        (len(fs) == 1 and cur_scope.parent.find_function_in_cur_scope(fs[0].name) is not None) or
                        (len(fs) == 0)
                ):
                    is_nonlocal = False
                else:
                    is_nonlocal = True
                    if add_to_f:
                        if fs[-1].name in cur_scope.parent.functions:
                            fs.pop()
                        fs[0].outer_variables.append(v)
                        for f in fs[1:]:
                            f.outer_variables_inner.append(v)

                return v, is_nonlocal

            cur_scope = cur_scope.parent
        return None

    def find_function_in_cur_scope(self, name: str) -> None | ControlFunctionDefinition:
        for f in self.functions:
            if f.name == name:
                return f

    def find_function(self, name: str) -> None | ControlFunctionDefinition:
        cur_scope = self
        while cur_scope is not None:
            f = cur_scope.find_function_in_cur_scope(name)
            if f:
                return f
            cur_scope = cur_scope.parent
        return None

    def find_typedef_in_cur_scope(self, name: str) -> None | ControlTypedef:
        for t in self.typedefs:
            if t.typedef.name == name:
                return t

    def find_typedef(self, name: str) -> None | ControlTypedef:
        cur_scope = self
        while cur_scope is not None:
            t = cur_scope.find_typedef_in_cur_scope(name)
            if t:
                return t
            cur_scope = cur_scope.parent
        return None

    def find_class_in_cur_scope(self, name: str) -> None | ControlClass:
        for c in self.classes:
            if c.name == name:
                return c

    def find_class(self, name: str) -> None | ControlClass:
        cur_scope = self
        while cur_scope is not None:
            t = cur_scope.find_class_in_cur_scope(name)
            if t:
                return t
            cur_scope = cur_scope.parent
        return None

    def find_scope_type(self, scope_type: Types) -> 'Scope' | None:
        cur_scope = self
        while cur_scope is not None:
            if cur_scope.type == scope_type:
                return cur_scope
            cur_scope = cur_scope.parent
        return None

    def get_child_scope_from_creator(self, creator: scope_creator) -> Scope:
        if isinstance(creator, tuple):
            for child in self.children:
                if isinstance(child.creator, tuple):
                    if len(creator) == len(child.creator):
                        if all(
                            cr is ch for cr, ch in zip(creator, child.creator)
                        ):
                            return child
        else:
            for child in self.children:
                if child.creator is creator:
                    return child
        raise ValueError('Что-то пошло не так')

    def is_name_occupied(self, name: str, check_outer_scopes: bool = False) -> bool:
        if check_outer_scopes:
            return (
                    self.find_variable(name, False) is not None or
                    self.find_function(name) is not None or
                    self.find_typedef(name) is not None
            )
        else:
            return (
                    self.find_variable_in_cur_scope(name) is not None or
                    self.find_function_in_cur_scope(name) is not None or
                    self.find_typedef_in_cur_scope(name) is not None
            )

    def get_unique_name(self, name: str = '_', allow_override: bool = False) -> str:
        """Генерация уникального имени, c allow_override ищёт только в данной области видимости"""
        res = name
        if allow_override:
            while (
                    self.find_variable_in_cur_scope(res) is not None or
                    self.find_function_in_cur_scope(res) is not None or
                    self.find_typedef_in_cur_scope(res) is not None
            ):
                res = f'{name}_{uuid4().hex}'
        else:
            while (
                    self.find_variable(res, False) is not None or
                    self.find_function(res) is not None or
                    self.find_typedef(res) is not None
            ):
                res = f'{name}_{uuid4().hex}'
        return res

    @property
    def is_global(self) -> bool:
        return self.type == Scope.Types.Global
