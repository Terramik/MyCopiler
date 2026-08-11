from __future__ import annotations
from typing import Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ...Definitions.Tokens import *
from ...Definitions.Scopes import *
from ...Definitions.Enums import BaseTypes, TokenOperatorBinaryTypes, TokenOperatorPrefixTypes, TokenOperatorPostfixTypes, CycleControlTypes

from ...Main.ProcessRaw import process_raw
from ...Main.CollapseRaw import collapse_raw
from ...Main.Tokenize import tokenize_file
from ...Main.Analyze import analyze
from io import StringIO


def parse_and_analyze(code: str):
    """Утилита: токенизирует, сворачивает, обрабатывает и анализирует код."""
    raw, err = collapse_raw(tokenize_file(StringIO(code), zero_origin.file))
    block, err2 = process_raw(raw)
    scope, err3 = analyze(block)
    assert not err
    assert not err2
    assert not err3
    return block, scope


def check_list(need: list[CheckNode], have: list[Any]):
    """Проверяет, что списки имеют одинаковую длину и каждый элемент совпадает."""
    assert len(need) == len(have)
    for n, h in zip(need, have):
        n.is_match(h)


def check_depth_two(need: list[list[CheckNode]], have: list[list[Any]]):
    """Проверяет двухуровневый список (например, параметры функции)."""
    assert len(need) == len(have)
    for n_level, h_level in zip(need, have):
        assert len(n_level) == len(h_level)
        for n, h in zip(n_level, h_level):
            n.is_match(h)


# ---------------------- Абстрактные базовые классы для проверок ----------------------

class CheckNode(ABC):
    @abstractmethod
    def is_match(self, node: Any):
        pass


class CheckValueABC(CheckNode):
    """Базовый класс для всех проверяемых значений (rvalue и wvalue)."""
    pass


class CheckRvalueABC(CheckValueABC):
    """Для проверяемых rvalue."""
    pass


class CheckWvalueABC(CheckValueABC):
    """Для проверяемых wvalue."""
    pass


class CheckControlABC(CheckNode):
    """Для проверяемых управляющих конструкций."""
    pass


# ---------------------- Проверка типа ----------------------

class CheckType(CheckNode, ABC):
    pass


@dataclass(slots=True)
class CheckTypeSimple(CheckType):
    type: Type

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert self.type == node


@dataclass(slots=True)
class CheckTypeFunc(CheckType):
    arg_types: list[CheckType]
    res_types: list[CheckType]
    modifiers: list[Type.ModifierABS] = field(default_factory=list)

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert isinstance(node.simple, Type.SimpleTypeFunc)
        check_list(self.arg_types, node.simple.arguments)
        check_list(self.res_types, node.simple.results)
        assert self.modifiers == node.modifiers


class ClassDescriptor:
    """Нужен для независимости от всяких круговых зависимостей"""
    def __init__(self, class_: CheckControlClass):
        self._class_: CheckControlClass = class_

    @property
    def class_(self) -> CheckControlClass:
        assert self._class_ is not None
        return self._class_

    @class_.setter
    def class_(self, class_: CheckControlClass):
        self._class_ = class_


class ClassDescriptorManager:
    def __init__(self):
        self.classes: dict[int, ClassDescriptor] = {}

    def assign(self, id_: int, class_: CheckControlClass) -> CheckControlClass:
        if id_ in self.classes:
            self.classes[id_].class_ = class_
        else:
            self.classes[id_] = ClassDescriptor(class_)
        return class_

    def elem(self, id_: int) -> ClassDescriptor:
        if not id_ in self.classes:
            self.classes[id_] = ClassDescriptor(None)
        return self.classes[id_]


@dataclass(slots=True)
class CheckTypeClassItself(CheckType):
    """Проверка типа 'сам класс' (используется как контейнер статических членов)."""
    class_: ClassDescriptor   # объект, возвращённый CheckControlClass
    modifiers: list[Type.ModifierABS] = field(default_factory=list)

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert isinstance(node.simple, Type.SimpleTypeClass)
        self.class_.class_.is_match_poor(node.cls)
        assert self.modifiers == node.modifiers


@dataclass(slots=True)
class CheckTypeClassInstance(CheckType):
    """Проверка типа 'экземпляр класса'."""
    class_: ClassDescriptor
    modifiers: list[Type.ModifierABS] = field(default_factory=list)

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert isinstance(node.full_type.simple, Type.SimpleTypeClassInstance)
        self.class_.class_.is_match_poor(node.full_type.cls)
        assert self.modifiers == node.modifiers


@dataclass(slots=True)
class CheckTypeEnumInstance(CheckType):
    """Проверка типа 'экземпляр класса'."""
    enum: CheckControlEnum
    modifiers: list[Type.ModifierABS] = field(default_factory=list)

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert isinstance(node.full_type.simple, Type.SimpleTypeEnumInstance)
        self.enum.is_match(node.enum)
        assert self.modifiers == node.modifiers


@dataclass(slots=True)
class CheckTypeEnum(CheckType):
    """Проверка типа 'экземпляр класса'."""
    enum: CheckControlEnum
    modifiers: list[Type.ModifierABS] = field(default_factory=list)

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert isinstance(node.full_type.simple, Type.SimpleTypeEnum)
        self.enum.is_match(node.enum)
        assert self.modifiers == node.modifiers

# ---------------------- Проверки токенов (rvalue / wvalue) ----------------------

@dataclass(slots=True)
class CheckTokenLiteral(CheckRvalueABC):
    value: str
    type: CheckType

    def is_match(self, node: TokenLiteral):
        assert isinstance(node, TokenLiteral)
        assert node.value == self.value
        self.type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenVariableAccess(CheckRvalueABC, CheckWvalueABC):
    name: str
    res_type: CheckType | None

    def is_match(self, node: TokenVariableAccess):
        assert isinstance(node, TokenVariableAccess)
        assert node.name == self.name
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorBinary(CheckRvalueABC):
    op: TokenOperatorBinaryTypes
    left: CheckRvalueABC
    right: CheckRvalueABC
    res_type: CheckType | None

    def is_match(self, node: TokenOperatorBinary):
        assert isinstance(node, TokenOperatorBinary)
        assert node.type == self.op
        self.left.is_match(node.left)
        self.right.is_match(node.right)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorPrefix(CheckRvalueABC):
    op: TokenOperatorPrefixTypes
    operand: CheckRvalueABC
    res_type: CheckType | None

    def is_match(self, node: TokenOperatorPrefix):
        assert isinstance(node, TokenOperatorPrefix)
        assert node.type == self.op
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorPostfix(CheckRvalueABC):
    op: TokenOperatorPostfixTypes
    operand: CheckRvalueABC
    res_type: CheckType | None

    def is_match(self, node: TokenOperatorPostfix):
        assert isinstance(node, TokenOperatorPostfix)
        assert node.type == self.op
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorCast(CheckRvalueABC):
    cast_type: CheckType
    operand: CheckRvalueABC

    def is_match(self, node: TokenOperatorCast):
        assert isinstance(node, TokenOperatorCast)
        self.cast_type.is_match(node.cast_type)
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorFunctionCall(CheckRvalueABC):
    func: CheckRvalueABC
    arguments: list[CheckRvalueABC]
    res_type: CheckType | None

    def is_match(self, node: TokenOperatorFunctionCall):
        assert isinstance(node, TokenOperatorFunctionCall)
        self.func.is_match(node.func)
        check_list(self.arguments, node.arguments)
        if self.res_type is not None:
            print(node, node.res_type)
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorAssignment(CheckRvalueABC):
    left: CheckWvalueABC
    right: CheckRvalueABC
    res_type: CheckType | None

    def is_match(self, node: TokenOperatorAssignment):
        assert isinstance(node, TokenOperatorAssignment)
        self.left.is_match(node.left)
        self.right.is_match(node.right)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorVariableDefinition(CheckWvalueABC):
    name: str
    type: CheckType

    def is_match(self, node: TokenOperatorVariableDefinition):
        assert isinstance(node, TokenOperatorVariableDefinition)
        assert node.name == self.name
        self.type.is_match(node.type)


@dataclass(slots=True)
class CheckTokenOperatorSizeof(CheckRvalueABC):
    type: CheckType
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorSizeof):
        assert isinstance(node, TokenOperatorSizeof)
        self.type.is_match(node.type)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorLenof(CheckRvalueABC):
    operand: CheckRvalueABC
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorLenof):
        assert isinstance(node, TokenOperatorLenof)
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            print(node)
            print(node.operand)
            print(node.res_type)
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorSlize(CheckRvalueABC):
    operand: CheckRvalueABC
    position_start: list[CheckRvalueABC] | None
    result_dimensions: list[CheckRvalueABC] | None
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorSlize):
        assert isinstance(node, TokenOperatorSlize)
        self.operand.is_match(node.operand)
        if self.position_start is None:
            assert node.position_start is None
        else:
            check_list(self.position_start, node.position_start)
        if self.result_dimensions is None:
            assert node.result_dimensions is None
        else:
            check_list(self.result_dimensions, node.result_dimensions)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorIndex(CheckRvalueABC, CheckWvalueABC):
    operand: CheckValueABC   # может быть и rvalue, и wvalue
    index: CheckRvalueABC
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorIndex):
        assert isinstance(node, TokenOperatorIndex)
        self.operand.is_match(node.operand)
        self.index.is_match(node.index)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorArrayCreation(CheckRvalueABC):
    operands: list[CheckRvalueABC]
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorArrayCreation):
        assert isinstance(node, TokenOperatorArrayCreation)
        check_list(self.operands, node.operands)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorReferencing(CheckRvalueABC):
    operand: CheckWvalueABC
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorReferencing):
        assert isinstance(node, TokenOperatorReferencing)
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorDereferencing(CheckRvalueABC, CheckWvalueABC):
    operand: CheckRvalueABC
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorDereferencing):
        assert isinstance(node, TokenOperatorDereferencing)
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorFieldAccess(CheckRvalueABC, CheckWvalueABC):
    operand: CheckRvalueABC
    name: str
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorFieldAccess):
        assert isinstance(node, TokenOperatorFieldAccess)
        self.operand.is_match(node.operand)
        assert node.name == self.name
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorFieldAccessPointer(CheckRvalueABC, CheckWvalueABC):
    operand: CheckRvalueABC
    name: str
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorFieldAccessPointer):
        assert isinstance(node, TokenOperatorFieldAccessPointer)
        self.operand.is_match(node.operand)
        assert node.name == self.name
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorDeInitializer(CheckRvalueABC):
    operand: CheckRvalueABC
    res_type: CheckType | None = None

    def is_match(self, node: TokenOperatorDeInitializer):
        assert isinstance(node, TokenOperatorDeInitializer)
        self.operand.is_match(node.operand)
        if self.res_type is not None:
            self.res_type.is_match(node.res_type)


# ---------------------- Проверки управляющих конструкций ----------------------

@dataclass(slots=True)
class CheckControlExpression(CheckControlABC):
    first: CheckValueABC   # может быть rvalue или определение переменной

    def is_match(self, node: ControlExpression):
        assert isinstance(node, ControlExpression)
        self.first.is_match(node.first)


@dataclass(slots=True)
class CheckControlReturn(CheckControlABC):
    results: list[CheckRvalueABC]

    def is_match(self, node: ControlReturn):
        assert isinstance(node, ControlReturn)
        check_list(self.results, node.results)


@dataclass(slots=True)
class CheckControlMassAssignmentInner(CheckNode):
    rvalue: CheckRvalueABC
    wvalues: list[CheckWvalueABC]
    t_need: list[CheckType | None]

    def is_match(self, node: ControlMassAssignment.Inner, mass: ControlMassAssignment | None = None):
        assert mass is not None
        assert isinstance(node, ControlMassAssignment.Inner)
        self.rvalue.is_match(node.rvalue)
        check_list(self.wvalues, [mass.left[i] for i in node.wvalues])
        assert len(self.t_need) == len(node.t_need)
        for tn, hn in zip(self.t_need, node.t_need):
            if tn is None:
                assert hn is None
            else:
                tn.is_match(hn)


@dataclass(slots=True)
class CheckControlMassAssignment(CheckControlABC):
    left: list[CheckWvalueABC]
    right: list[CheckRvalueABC]
    processed: list[CheckControlMassAssignmentInner]


    def is_match(self, node: ControlMassAssignment):
        assert isinstance(node, ControlMassAssignment)
        check_list(self.left, node.left)
        check_list(self.right, node.right)
        assert len(self.processed) == len(node.processed)
        for need, have in zip(self.processed, node.processed):
            need.is_match(have, node)


@dataclass(slots=True)
class CheckControlFunctionDefinition(CheckControlABC):
    name: str
    parameters: list[CheckTokenOperatorVariableDefinition]
    results: list[CheckType]
    outer_variables: list[CheckTokenOperatorVariableDefinition] | None
    code_block: CheckControlCodeBlock

    def is_match(self, node: ControlFunctionDefinition) -> None:
        assert isinstance(node, ControlFunctionDefinition)
        assert node.name == self.name
        check_list(self.parameters, node.parameters)
        check_list(self.results, node.results)
        self.code_block.is_match(node.code_block)
        if self.outer_variables is not None:
            check_list(self.outer_variables, node.outer_variables)


@dataclass(slots=True)
class CheckControlCodeBlock(CheckControlABC):
    block_parts: list[CheckControlABC]

    def is_match(self, node: ControlCodeBlock):
        assert isinstance(node, ControlCodeBlock)
        check_list(self.block_parts, node.block_parts)


@dataclass(slots=True)
class CheckControlWhile(CheckControlABC):
    condition: CheckRvalueABC
    code_block: CheckControlCodeBlock

    def is_match(self, node: ControlWhile):
        assert isinstance(node, ControlWhile)
        self.condition.is_match(node.condition)
        self.code_block.is_match(node.code_block)


@dataclass(slots=True)
class CheckControlIf(CheckControlABC):
    condition: CheckRvalueABC
    block_if: CheckControlCodeBlock
    block_else: CheckControlCodeBlock

    def is_match(self, node: ControlIf):
        assert isinstance(node, ControlIf)
        self.condition.is_match(node.condition)
        self.block_if.is_match(node.block_if)
        self.block_else.is_match(node.block_else)


@dataclass(slots=True)
class CheckControlCycleControl(CheckControlABC):
    type: CycleControlTypes

    def is_match(self, node: ControlCycleControl):
        assert isinstance(node, ControlCycleControl)
        assert node.type == self.type


@dataclass(slots=True)
class CheckControlTypedef(CheckControlABC):
    name: str
    type: CheckType

    def is_match(self, node: ControlTypedef):
        assert isinstance(node, ControlTypedef)
        assert node.typedef.name == self.name
        self.type.is_match(node.typedef.type)


@dataclass(slots=True)
class CheckControlImport(CheckControlABC):
    path: str
    names: list[tuple[str, str]]
    all: bool = False

    def is_match(self, node: ControlImport):
        assert isinstance(node, ControlImport)
        assert self.names == node.names
        assert self.all == node.all


@dataclass(slots=True)
class CheckControlExport(CheckControlABC):
    names: list[tuple[str, str]]
    all: bool = False

    def is_match(self, node: ControlExport):
        assert isinstance(node, ControlExport)
        assert self.names == node.names
        assert self.all == node.all


@dataclass(slots=True)
class CheckControlClass(CheckControlABC):
    name: str
    instance_field: list[CheckTokenOperatorVariableDefinition]
    rest: CheckControlCodeBlock
    # Поля class_var, class_field, all_methods, magic_methods при необходимости можно добавить,
    # но они заполняются на этапе анализа и не всегда нужны для простых тестов.

    def is_match(self, node: ControlClass):
        assert isinstance(node, ControlClass)
        assert node.name == self.name
        check_list(self.instance_field, node.instance_field)
        self.rest.is_match(node.rest)

    def is_match_poor(self, node: ControlClass):
        """Нужен для проверки типа, т.к. если в классе будет тип самого класса, это вызывет повторную проверку всего класса, а потом..."""
        assert isinstance(node, ControlClass)
        assert node.name == self.name


@dataclass(slots=True)
class CheckControlEnum(CheckControlABC):
    name: str
    states: list[str]

    def is_match(self, node: ControlEnum):
        assert isinstance(node, ControlEnum)
        assert self.name == node.name
        assert self.states == node.states


# ---------------------- Проверка области видимости ----------------------


@dataclass(slots=True)
class CheckScope(CheckNode):
    scope_type: Scope.Types
    variables: set[str] = field(default_factory=lambda: set())
    functions: set[str] = field(default_factory=lambda: set())
    typedefs: set[str] = field(default_factory=lambda: set())
    classes: set[str] = field(default_factory=lambda: set())
    enums: set[str] = field(default_factory=lambda: set())
    children: list['CheckScope'] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.variables = self.variables.union(self.functions)
        self.variables = self.variables.union(self.classes)
        self.variables = self.variables.union(self.enums)

    def is_match(self, scope: Scope):
        assert scope.type == self.scope_type

        assert set([t.typedef.name for t in scope.typedefs]) == self.typedefs

        print(set([v.name for v in scope.variables]), self.variables)
        assert set([v.name for v in scope.variables]) == self.variables
        assert set([f.name for f in scope.functions]) == self.functions
        assert set([f.name for f in scope.classes]) == self.classes
        assert set([f.name for f in scope.enums]) == self.enums

        check_list(self.children, scope.children)
        assert len(scope.children) == len(self.children)
        for child_scope, child_check in zip(scope.children, self.children):
            child_check.is_match(child_scope)


