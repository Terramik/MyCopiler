from __future__ import annotations
from ...Main.Tokenize import tokenize_file
from ...Main.CollapseRaw import collapse_raw
from ...Main.ProcessRaw import process_raw
from ...Definitions.Tokens import *
from ...Definitions.Raw import ControlRawCodeBlock
from ...Definitions.Enums import TokenOperatorBinaryTypes, TokenOperatorPrefixTypes
from ...Definitions.Exceptions import OurSyntaxError
from dataclasses import dataclass
from typing import Any
from io import StringIO
from abc import ABC, abstractmethod


def tokenize_and_process(code: str) -> ControlRawCodeBlock:
    code, err = collapse_raw(tokenize_file(StringIO(code), zero_origin.file))
    assert not err
    return code


def tokenize_and_process_raw(code: str) -> ControlCodeBlock:
    raw_code, err = collapse_raw(tokenize_file(StringIO(code), zero_origin.file))
    code, err2 = process_raw(raw_code)
    err = err + err2
    assert not err
    return code


def check_list(need: list[CheckNode], have: list[Any]) -> None:
    assert len(need) == len(have)
    for n, h in zip(need, have):
        n.is_match(h)


# ----------------------------------------------------------------------
# Абстрактные базовые классы для проверяющих узлов (вместо Union)
# ----------------------------------------------------------------------
class CheckNode(ABC):
    @abstractmethod
    def is_match(self, node: Any):
        pass


class CheckNodeRValue(CheckNode):
    """Базовый класс для проверки RValue-узлов."""
    @abstractmethod
    def is_match(self, node: Any):
        pass


class CheckNodeWValue(CheckNode):
    """Базовый класс для проверки WValue-узлов."""
    @abstractmethod
    def is_match(self, node: Any):
        pass


class CheckNodeControl(CheckNode):
    """Базовый класс для проверки управляющих конструкций."""
    @abstractmethod
    def is_match(self, node: Any):
        pass


# ----------------------------------------------------------------------
# Проверяющие классы для токенов (операторов)
# ----------------------------------------------------------------------

@dataclass(slots=True)
class CheckType(CheckNode):
    type: Type

    def is_match(self, node: Type):
        assert isinstance(node, Type)
        assert self.type == node


@dataclass(slots=True)
class CheckTokenOperatorVariableDefinition(CheckNodeWValue):
    name: str
    type: CheckType

    def is_match(self, node: TokenOperatorVariableDefinition):
        assert isinstance(node, TokenOperatorVariableDefinition)
        assert node.name == self.name
        self.type.is_match(node.type)


@dataclass(slots=True)
class CheckTokenVariableAccess(CheckNodeRValue, CheckNodeWValue):
    name: str

    def is_match(self, node: TokenVariableAccess):
        assert isinstance(node, TokenVariableAccess)
        assert node.name == self.name


@dataclass(slots=True)
class CheckTokenLiteral(CheckNodeRValue):
    value: str
    type: CheckType

    def is_match(self, node: TokenLiteral):
        assert isinstance(node, TokenLiteral)
        assert node.value == self.value
        self.type.is_match(node.res_type)


@dataclass(slots=True)
class CheckTokenOperatorAssignment(CheckNodeRValue):
    left: CheckNodeWValue
    right: CheckNodeRValue

    def is_match(self, node: TokenOperatorAssignment):
        assert isinstance(node, TokenOperatorAssignment)
        self.left.is_match(node.left)
        self.right.is_match(node.right)


@dataclass(slots=True)
class CheckTokenOperatorFunctionCall(CheckNodeRValue):
    arguments: list[CheckNodeRValue]

    def is_match(self, node: TokenOperatorFunctionCall):
        assert isinstance(node, TokenOperatorFunctionCall)
        check_list(self.arguments, node.arguments)


@dataclass(slots=True)
class CheckTokenOperatorBinary(CheckNodeRValue):
    op: TokenOperatorBinaryTypes
    left: CheckNodeRValue
    right: CheckNodeRValue

    def is_match(self, node: TokenOperatorBinary):
        assert isinstance(node, TokenOperatorBinary)
        assert node.type == self.op
        self.left.is_match(node.left)
        self.right.is_match(node.right)


@dataclass(slots=True)
class CheckTokenOperatorPrefix(CheckNodeRValue):
    op: TokenOperatorPrefixTypes
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorPrefix):
        assert isinstance(node, TokenOperatorPrefix)
        assert node.type == self.op
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorPostfix(CheckNodeRValue):
    op: TokenOperatorPostfixTypes
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorPostfix):
        assert isinstance(node, TokenOperatorPostfix)
        assert node.type == self.op
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorCast(CheckNodeRValue):
    cast_type: CheckType
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorCast):
        assert isinstance(node, TokenOperatorCast)
        self.cast_type.is_match(node.cast_type)
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorIndex(CheckNodeRValue, CheckNodeWValue):
    operand: CheckNodeRValue | CheckNodeWValue
    index: CheckNodeRValue

    def is_match(self, node: TokenOperatorIndex):
        assert isinstance(node, TokenOperatorIndex)
        self.operand.is_match(node.operand)
        self.index.is_match(node.index)


@dataclass(slots=True)
class CheckTokenOperatorSlize(CheckNodeRValue):
    operand: CheckNodeRValue
    position_start: list[CheckNodeRValue] | None
    result_dimensions: list[CheckNodeRValue] | None

    def is_match(self, node: TokenOperatorSlize):
        assert isinstance(node, TokenOperatorSlize)
        self.operand.is_match(node.operand)
        if self.position_start is None:
            assert node.position_start is None
        else:
            assert node.position_start is not None
            check_list(self.position_start, node.position_start)
        if self.result_dimensions is None:
            assert node.result_dimensions is None
        else:
            check_list(self.result_dimensions, node.result_dimensions)


@dataclass(slots=True)
class CheckTokenOperatorReferencing(CheckNodeRValue):
    operand: CheckNodeWValue

    def is_match(self, node: TokenOperatorReferencing):
        assert isinstance(node, TokenOperatorReferencing)
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorDereferencing(CheckNodeRValue, CheckNodeWValue):
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorDereferencing):
        assert isinstance(node, TokenOperatorDereferencing)
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorSizeof(CheckNodeRValue):
    type: CheckType

    def is_match(self, node: TokenOperatorSizeof):
        assert isinstance(node, TokenOperatorSizeof)
        self.type.is_match(node.type)


@dataclass(slots=True)
class CheckTokenOperatorLenof(CheckNodeRValue):
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorLenof):
        assert isinstance(node, TokenOperatorLenof)
        self.operand.is_match(node.operand)


@dataclass(slots=True)
class CheckTokenOperatorArrayCreation(CheckNodeRValue):
    operands: list[CheckNodeRValue]

    def is_match(self, node: TokenOperatorArrayCreation):
        assert isinstance(node, TokenOperatorArrayCreation)
        check_list(self.operands, node.operands)


@dataclass(slots=True)
class CheckTokenOperatorFieldAccess(CheckNodeRValue, CheckNodeWValue):
    operand: CheckNodeRValue
    name: str

    def is_match(self, node: TokenOperatorFieldAccess):
        assert isinstance(node, TokenOperatorFieldAccess)
        self.operand.is_match(node.operand)
        assert node.name == self.name


@dataclass(slots=True)
class CheckTokenOperatorFieldAccessPointer(CheckNodeRValue, CheckNodeWValue):
    operand: CheckNodeRValue
    name: str

    def is_match(self, node: TokenOperatorFieldAccessPointer):
        assert isinstance(node, TokenOperatorFieldAccessPointer)
        self.operand.is_match(node.operand)
        assert node.name == self.name


@dataclass(slots=True)
class CheckTokenOperatorDeInitializer(CheckNodeRValue):
    operand: CheckNodeRValue

    def is_match(self, node: TokenOperatorDeInitializer):
        assert isinstance(node, TokenOperatorDeInitializer)
        self.operand.is_match(node.operand)


# ----------------------------------------------------------------------
# Проверяющие классы для управляющих конструкций
# ----------------------------------------------------------------------

@dataclass(slots=True)
class CheckControlExpression(CheckNodeControl):
    first: CheckNodeRValue | CheckTokenOperatorVariableDefinition

    def is_match(self, node: ControlExpression):
        assert isinstance(node, ControlExpression)
        self.first.is_match(node.first)


@dataclass(slots=True)
class CheckControlReturn(CheckNodeControl):
    results: list[CheckNodeRValue]

    def is_match(self, node: ControlReturn):
        assert isinstance(node, ControlReturn)
        check_list(self.results, node.results)


@dataclass(slots=True)
class CheckControlMassAssignment(CheckNodeControl):
    left: list[CheckNodeWValue]
    right: list[CheckNodeRValue]

    def is_match(self, node: ControlMassAssignment):
        assert isinstance(node, ControlMassAssignment)
        check_list(self.left, node.left)
        check_list(self.right, node.right)


@dataclass(slots=True)
class CheckControlFunctionDefinition(CheckNodeControl):
    name: str
    parameters: list[CheckTokenOperatorVariableDefinition]
    results: list[CheckType]
    code_block: CheckControlCodeBlock

    def is_match(self, node: ControlFunctionDefinition):
        assert isinstance(node, ControlFunctionDefinition)
        assert node.name == self.name
        check_list(self.parameters, node.parameters)
        check_list(self.results, node.results)
        self.code_block.is_match(node.code_block)


@dataclass(slots=True)
class CheckControlIf(CheckNodeControl):
    condition: CheckNodeRValue
    block_if: CheckControlCodeBlock
    block_else: CheckControlCodeBlock

    def is_match(self, node: ControlIf | Any):
        assert isinstance(node, ControlIf)
        self.condition.is_match(node.condition)
        self.block_if.is_match(node.block_if)
        self.block_else.is_match(node.block_else)


@dataclass(slots=True)
class CheckControlCodeBlock(CheckNodeControl):
    block_parts: list[CheckNodeControl]

    def is_match(self, node: ControlCodeBlock):
        assert isinstance(node, ControlCodeBlock)
        check_list(self.block_parts, node.block_parts)


@dataclass(slots=True)
class CheckControlWhile(CheckNodeControl):
    condition: CheckNodeRValue
    code_block: CheckControlCodeBlock

    def is_match(self, node: ControlWhile):
        assert isinstance(node, ControlWhile)
        self.condition.is_match(node.condition)
        self.code_block.is_match(node.code_block)


@dataclass(slots=True)
class CheckControlCycleControl(CheckNodeControl):
    type: CycleControlTypes

    def is_match(self, node: ControlCycleControl):
        assert isinstance(node, ControlCycleControl)
        assert node.type == self.type


@dataclass(slots=True)
class CheckControlTypedef(CheckNodeControl):
    name: str
    type: CheckType

    def is_match(self, node: ControlTypedef):
        assert isinstance(node, ControlTypedef)
        assert self.name == node.typedef.name
        self.type.is_match(node.typedef.type)


@dataclass(slots=True)
class CheckControlImport(CheckNodeControl):
    path: str
    all: bool
    names: list[tuple[str, str]]

    def is_match(self, node: ControlImport):
        assert isinstance(node, ControlImport)
        assert node.path == self.path
        assert node.all == self.all
        assert node.names == self.names


@dataclass(slots=True)
class CheckControlExport(CheckNodeControl):
    all: bool
    names: list[tuple[str, str]]

    def is_match(self, node: ControlExport):
        assert isinstance(node, ControlExport)
        assert node.all == self.all
        assert node.names == self.names


@dataclass(slots=True)
class CheckControlClass(CheckNodeControl):
    name: str
    instance_field: list[CheckTokenOperatorVariableDefinition]
    rest: CheckControlCodeBlock

    def is_match(self, node: ControlClass):
        assert isinstance(node, ControlClass)
        assert node.name == self.name
        check_list(self.instance_field, node.instance_field)
        self.rest.is_match(node.rest)
