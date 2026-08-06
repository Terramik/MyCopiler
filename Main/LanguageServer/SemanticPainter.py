from ...Definitions.Tokens import *
from ...Definitions.Modules import Module
from ...Definitions.TreeInterface import IteratorControl, IteratorExpression

from enum import Enum
from dataclasses import dataclass


__all__ = ('LEGEND_TOKEN_TYPES', 'LEGEND_MODIFIERS', 'sematic_print')


# ===== Типы токенов =====


LEGEND_TOKEN_TYPES = [
    "namespace", "type", "class", "enum", "interface", "struct",
    "typeParameter", "parameter", "variable", "property", "enumMember",
    "function", "method", "macro", "keyword", "modifier", "comment",
    "string", "number", "regexp", "operator", "decorator"
]

LEGEND_MODIFIERS = [
    "declaration", "definition", "readonly", "static", "deprecated",
    "abstract", "async", "modification", "documentation", "defaultLibrary"
]


class NameToIndex:
    def __init__(self, data: dict[str, int]):
        super().__setattr__('data', data)

    def __getattr__(self, item):
        return self.data[item]


LegendTokens = NameToIndex({
    s.capitalize(): i
    for i, s in enumerate(LEGEND_TOKEN_TYPES)
})

LegendModifiers = NameToIndex({
    s.capitalize(): 1 << i
    for i, s in enumerate(LEGEND_MODIFIERS)
})


# ===== Интерфейс для добавления =====


class SemanticWeaver:
    def __init__(self, line_to_size: list[int]):
        self.line_to_size = line_to_size
        self.data: list[int] = []
        self.last_line: int = 0
        self.last_col: int = 0

    def weave(self, origin: TokenOrigin, token: int, modifiers: int):
        is_one_line = origin.start.line == origin.end.line

        if is_one_line:
            end_col = origin.end.column
        else:
            end_col = self.line_to_size[origin.start.line]

        if self.last_line != origin.start.line:
            self.last_col = 0

        self.data.extend((
            origin.start.line - self.last_line,  # dline
            origin.start.column - self.last_col,  # dcol
            end_col - origin.start.column,  # length
            token,
            modifiers
        ))

        if not is_one_line:
            # "закрасим" всё промежуточное
            for i in range(origin.start.line + 1, origin.end.line):
                self.data.extend((0, 0, self.line_to_size[i], token, modifiers))
            # и теперь конечное
            self.data.extend((0, 0, origin.end.column, token, modifiers))

        self.last_line = origin.end.line
        self.last_col = origin.end.column


def count_line_and_size(path: Path) -> list[int]:
    """Считает длину каждой строки"""
    res = []
    with open(path, 'r') as f:
        for line in f:
            res.append(len(line))
    return res


# ===== Собственно проход =====


RWValue = TokenOperatorRvalueABC | TokenOperatorWvalueABC


class ItExpr(IteratorExpression):
    def __init__(self):
        to_print: list[tuple[TokenOrigin, int, int]] = []

    # Токены в выражениях, в отличие от токенов в управляющих
    # конструкциях, не идут друг за другом линейно. Так что нам нужно будет их отсортировать.
    def start(self, weaver: SemanticWeaver, first: RWValue):
        self(first, None)
        ...


class ItCont(IteratorControl):
    def __init__(self, weaver: SemanticWeaver):
        self.weaver = weaver

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        pass

    def on_code_block(self, code: ControlCodeBlock):
        for control in code.block_parts:
            self(control)

    def on_func_def(self, func_def: ControlFunctionDefinition):
        # пишем def
        self.weaver.weave(
            TokenOrigin(
                func_def.origin.start,
                TextPosition(
                    func_def.origin.start.line,
                    func_def.origin.start.column + len(KeyWords.Function.value),
                ),
                func_def.origin.file
            ),
            LegendTokens.Keyword,
            0
        )
        self(func_def.code_block)

    def on_expression_control(self, expr: ControlExpression):
        self.on_expr(expr.first, expr)

    def on_return(self, ret: ControlReturn):
        for r in ret.results:
            self.on_expr(r, ret)

    def on_mass_assignment(self, mass_asg: ControlMassAssignment):
        for w in mass_asg.left:
            self.on_expr(w, mass_asg)
        for r in mass_asg.right:
            self.on_expr(r, mass_asg)

    def on_if(self, cond: ControlIf):
        self.on_expr(cond.condition, cond)
        self(cond.block_if)
        self(cond.block_else)

    def on_while(self, while_: ControlWhile):
        self.on_expr(while_.condition, while_)
        self(while_.code_block)

    def on_cycle_control(self, cycle_control: ControlCycleControl):
        pass

    def on_typedef(self, typedef: ControlTypedef):
        pass

    def on_import(self, import_: ControlImport):
        pass

    def on_export(self, export_: ControlExport):
        pass

    def on_class(self, cls: ControlClass):
        self(cls.rest)

    def on_enum(self, enum: ControlEnum):
        pass


def sematic_print(module: Module) -> list[int]:
    with open(Path(__file__).parent / 'logs.txt', 'a') as f:
        print(f'file {module.path_to_file} SemanticPrint start', file=f)
        line_to_size = count_line_and_size(module.path_to_file)
        weaver = SemanticWeaver(line_to_size)

        it_cont = ItCont(weaver)
        it_cont(module.code)
        i = 0
        while i < len(weaver.data) // 5:
            print(weaver.data[i*5:i*5+5], file=f)

        return weaver.data


#(LegendTokens.Class, LegendModifiers.Declaration | LegendModifiers.Abstract)