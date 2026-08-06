from __future__ import annotations
from ...Definitions.Raw import *
from ...Main.Tokenize import tokenize_file
from io import StringIO
from dataclasses import dataclass
from abc import ABC, abstractmethod


def tokenize(data: str) -> list[TokenRawABC]:
    return tokenize_file(StringIO(data), zero_origin.file)


TypeCheckControlRaw = Union[
    'CheckControlRawExpression',
    'CheckControlRawReturn',
    'CheckControlRawMassAssignment',
    'CheckControlRawCodeBlock',
    'CheckControlRawFunctionDefinition',
    'CheckControlRawWhile',
    'CheckControlRawCycleControl',
    'CheckControlRawIf'
]


class CheckABS(ABC):
    @abstractmethod
    def is_match(self, control: ...):
        pass


@dataclass(slots=True)
class CheckTokenRaw(CheckABS):
    type: ControlRawABC
    val: str

    def is_match(self, tok: TokenRawWord | TokenRawSymbol | TokenRawLiteral):
        assert isinstance(tok, self.type)
        v = None
        match tok:
            case TokenRawWord():
                v = tok.word
            case TokenRawSymbol():
                v = tok.symbol
            case TokenRawLiteral():
                v = tok.literal
        assert v == self.val


T_WRD = TokenRawWord
T_SYM = TokenRawSymbol
T_LIT = TokenRawLiteral
CTR = CheckTokenRaw


def check_depth_one(need: list[CheckABS], have: list[...]):
    print(len(need), len(have))
    assert len(need) == len(have)
    for n, h in zip(need, have):
        n.is_match(h)


def check_depth_two(need: list[list[CheckABS]], have: list[list[...]]):
    assert len(need) == len(have)
    for _need, _have in zip(need, have):
        assert isinstance(_have, list)
        assert len(_need) == len(_have)
        for n, h in zip(_need, _have):
            n.is_match(h)


@dataclass(slots=True)
class CheckControlRawExpression(CheckABS):
    tokens: list[CheckTokenRaw]

    def is_match(self, control: ControlRawExpression | ...):
        assert isinstance(control, ControlRawExpression)
        assert len(self.tokens) == len(control.tokens)
        for i in range(len(self.tokens)):
            self.tokens[i].is_match(control.tokens[i])


@dataclass(slots=True)
class CheckControlRawReturn(CheckABS):
    tokens: list[list[CheckTokenRaw]]

    def is_match(self, control: ControlRawReturn | ...):
        assert isinstance(control, ControlRawReturn)
        check_depth_two(self.tokens, control.tokens)


@dataclass(slots=True)
class CheckControlRawMassAssignment(CheckABS):
    left: list[list[CheckTokenRaw]]
    right: list[list[CheckTokenRaw]]

    def is_match(self, control: ControlRawMassAssignment | ...):
        assert isinstance(control, ControlRawMassAssignment)
        check_depth_two(self.left, control.left)
        check_depth_two(self.right, control.right)


@dataclass(slots=True)
class CheckControlRawCodeBlock(CheckABS):
    block_parts: list[TypeCheckControlRaw]

    def is_match(self, control: ControlRawCodeBlock | ...):
        assert isinstance(control, ControlRawCodeBlock)
        assert len(self.block_parts) == len(control.block_parts)
        for i in range(len(self.block_parts)):
            self.block_parts[i].is_match(control.block_parts[i])


@dataclass(slots=True)
class CheckControlRawFunctionDefinition(CheckABS):
    name: str
    parameters: list[list[CheckTokenRaw]]
    results: list[list[CheckTokenRaw]]
    code_block: CheckControlRawCodeBlock

    def is_match(self, control: ControlRawFunctionDefinition | ...):
        assert isinstance(control, ControlRawFunctionDefinition)
        assert self.name == control.name
        check_depth_two(self.parameters, control.parameters)
        check_depth_two(self.results, control.results)
        self.code_block.is_match(control.code_block)


@dataclass(slots=True)
class CheckControlRawIf(CheckABS):
    type: ConditionalPartTypes
    condition: list[CheckTokenRaw]
    block_if: CheckControlRawCodeBlock
    block_else: CheckControlRawCodeBlock

    def is_match(self, control: ControlRawIf | ...):
        assert isinstance(control, ControlRawIf)
        assert self.type == control.type
        self.block_if.is_match(control.block_if)
        self.block_else.is_match(control.block_else)


@dataclass(slots=True)
class CheckControlRawWhile(CheckABS):
    condition: list[CheckTokenRaw]
    code_block: CheckControlRawCodeBlock

    def is_match(self, control: ControlRawWhile | ...):
        assert isinstance(control, ControlRawWhile)
        check_depth_one(self.condition, control.condition)
        self.code_block.is_match(control.code_block)


@dataclass(slots=True)
class CheckControlRawCycleControl(CheckABS):
    type: CycleControlTypes

    def is_match(self, control: ControlRawCycleControl | ...):
        assert isinstance(control, ControlRawCycleControl)
        assert self.type == control.type


@dataclass(slots=True)
class CheckControlRawTypedef(CheckABS):
    name: str
    type: list[CheckTokenRaw]

    def is_match(self, control: ControlRawTypedef | ...):
        assert isinstance(control, ControlRawTypedef)
        assert self.name == control.type
        check_depth_one(self.type, control.type)


@dataclass(slots=True)
class CheckControlRawClass(CheckABS):
    name: str
    instance_field: CheckControlRawCodeBlock
    rest: CheckControlRawCodeBlock

    def is_match(self, control: ControlRawClass):
        assert isinstance(control, ControlRawClass)


@dataclass(slots=True)
class CheckControlRawEnum(CheckABS):
    name: str
    states: list[str]

    def is_match(self, control: ControlRawEnum):
        assert isinstance(control, ControlRawEnum)
        assert self.name == control.name
        assert self.states == control.states
