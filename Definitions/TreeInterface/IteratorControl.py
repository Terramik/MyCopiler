from .Utils import *
from ..Scopes import Scope, scope_creator
from typing import Iterator
from dataclasses import dataclass


class IteratorControl:
    def __call__(self, control: ControlABC):
        match control:
            case ControlCodeBlock():
                self.on_code_block(control)
            case ControlFunctionDefinition():
                self.on_func_def(control)
            case ControlExpression():
                self.on_expression_control(control)
            case ControlReturn():
                self.on_return(control)
            case ControlMassAssignment():
                self.on_mass_assignment(control)
            case ControlIf():
                self.on_if(control)
            case ControlWhile():
                self.on_while(control)
            case ControlCycleControl():
                self.on_cycle_control(control)
            case ControlTypedef():
                self.on_typedef(control)
            case ControlImport():
                self.on_import(control)
            case ControlExport():
                self.on_export(control)
            case ControlClass():
                self.on_class(control)
            case ControlEnum():
                self.on_enum(control)

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        pass

    def on_code_block(self, code: ControlCodeBlock):
        for control in code.block_parts:
            self(control)

    def on_func_def(self, func_def: ControlFunctionDefinition):
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


class IteratorControlWithScope(IteratorControl):
    """
    Итератор, который при обходе AST поддерживает стеки текущего блока кода (ControlCodeBlock)
    и текущей области видимости (Scope).
    """

    def __init__(self):
        self._scope_stack: list[Scope] = []
        self._block_stack: list[ControlCodeBlock] = []

    def start(self, code: ControlCodeBlock, scope: Scope):
        self._block_stack = [code]
        self._scope_stack = [scope]
        self.on_code_block(code, False)

    @property
    def current_scope(self) -> Scope:
        return self._scope_stack[-1]

    @property
    def current_block(self) -> ControlCodeBlock:
        return self._block_stack[-1]

    def _enter_block(self, block: ControlCodeBlock, creator: scope_creator) -> None:
        self._block_stack.append(block)
        child_scope = self.current_scope.get_child_scope_from_creator(creator)
        self._scope_stack.append(child_scope)

    def _exit_block(self) -> None:
        self._block_stack.pop()
        self._scope_stack.pop()

    def _get_index(self, control: ControlABC) -> int:
        """
        Возвращает индекс управляющей конструкции в текущем блоке.
        Используется для определения позиции выражения при необходимости вставки.
        """
        return self.current_block.block_parts.index(control)

    # ---------- Основные методы обхода, где есть блоки кода ----------

    def on_func_def(self, func_def: ControlFunctionDefinition) -> None:
        self._enter_block(func_def.code_block, func_def)
        for control in func_def.code_block.block_parts:
            self(control)
        self._exit_block()

    def on_if(self, cond: ControlIf) -> None:
        self.on_expr(cond.condition, cond, self._get_index(cond))

        self._enter_block(cond.block_if, (cond, cond.block_if))
        for control in cond.block_if.block_parts:
            self(control)
        self._exit_block()

        self._enter_block(cond.block_else, (cond, cond.block_else))
        for control in cond.block_else.block_parts:
            self(control)
        self._exit_block()

    def on_while(self, while_: ControlWhile) -> None:
        self.on_expr(while_.condition, while_, self._get_index(while_))

        self._enter_block(while_.code_block, while_)
        for control in while_.code_block.block_parts:
            self(control)
        self._exit_block()

    def on_class(self, cls: ControlClass) -> None:
        self._enter_block(cls.rest, cls)
        for control in cls.rest.block_parts:
            self(control)
        self._exit_block()

    def on_expression_control(self, expr: ControlExpression) -> None:
        self.on_expr(expr.first, expr, self._get_index(expr))

    def on_return(self, ret: ControlReturn) -> None:
        idx = self._get_index(ret)
        for r in ret.results:
            self.on_expr(r, ret, idx)

    def on_mass_assignment(self, mass_asg: ControlMassAssignment) -> None:
        idx = self._get_index(mass_asg)
        for w in mass_asg.left:
            self.on_expr(w, mass_asg, idx)
        for r in mass_asg.right:
            self.on_expr(r, mass_asg, idx)

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC, index: int) -> None:
        pass

    def on_code_block(self, code: ControlCodeBlock, add_itself: bool = True) -> None:
        if add_itself:
            self._enter_block(code, code)
        for control in code.block_parts:
            self(control)
        if add_itself:
            self._exit_block()


