from ...Definitions.TreeInterface import IteratorControl, IteratorExpression, IteratorControlWithScope
from ...Definitions.Modules import Module
from ...Definitions.Scopes import Scope
from ...Definitions.Tokens import *


__all__ = ()


RWValue = TokenOperatorRvalueABC | TokenOperatorWvalueABC
ResNode = TokenOperatorRvalueABC | TokenOperatorWvalueABC | ControlABC | Type | None


class ItExpr():
    def __call__(self, node: RWValue, pos: TextPosition) -> ResNode:
        match node:
            case TokenOperatorVariableDefinition(): return self.on_var_def(node, pos)
            case TokenVariableAccess(): return self.on_var_access(node, pos)
            case TokenLiteral(): return self.on_literal(node, pos)
            case TokenOperatorAssignment(): return self.on_assignment(node, pos)
            case TokenOperatorFunctionCall(): return self.on_f_call(node, pos)
            case TokenOperatorBinary(): return self.on_binary(node, pos)
            case TokenOperatorPrefix(): return self.on_prefix(node, pos)
            case TokenOperatorPostfix(): return self.on_postfix(node, pos)
            case TokenOperatorCast(): return self.on_cast(node, pos)
            case TokenOperatorSizeof(): return self.on_sizeof(node, pos)
            case TokenOperatorLenof(): return self.on_lenof(node, pos)
            case TokenOperatorSlize(): return self.on_slize(node, pos)
            case TokenOperatorIndex(): return self.on_index(node, pos)
            case TokenOperatorArrayCreation(): return self.on_array_creation(node, pos)
            case TokenOperatorReferencing(): return self.on_referencing(node, pos)
            case TokenOperatorDereferencing(): return self.on_dereferencing(node, pos)
            case TokenOperatorFieldAccess(): return self.on_field_access(node, pos)
            case TokenOperatorFieldAccessPointer(): return self.on_field_access_pointer(node, pos)
            case TokenOperatorDeInitializer(): return self.on_deinitializer(node, pos)
            case TokenOperatorError(): return self.on_error_node(node, pos)
            case _: raise NotImplementedError('Что-то пошло не так')

    # методы для всего

    def on_var_def(self, node: TokenOperatorVariableDefinition, pos: TextPosition) -> ResNode:
        if pos in node.type.origin:
            return node.type
        elif pos in node.origin:
            return node

    def on_var_access(self, node: TokenVariableAccess, pos: TextPosition) -> ResNode:
        if pos in node.origin:
            return node

    def on_literal(self, node: TokenLiteral, pos: TextPosition) -> ResNode:
        if pos in node.origin:
            return node

    def on_assignment(self, node: TokenOperatorAssignment, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        left = self(node.left, pos)
        if left is not None:
            return left
        return self(node.right, pos)

    def on_f_call(self, node: TokenOperatorFunctionCall, pos: TextPosition) -> ResNode:
        f = self(node.func, pos)
        if f is not None: return f
        for ar in node.arguments:
            ar = self(ar, pos)
            if ar is not None: return ar

    def on_binary(self, node: TokenOperatorBinary, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        left = self(node.left, pos)
        if left is not None: return left
        return self(node.right, pos)

    def on_prefix(self, node: TokenOperatorPrefix, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_postfix(self, node: TokenOperatorPostfix, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_cast(self, node: TokenOperatorCast, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        elif pos in node.cast_type.origin: return node.cast_type
        return self(node.operand, pos)

    def on_sizeof(self, node: TokenOperatorSizeof, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        elif pos in node.res_type.origin: return node.res_type

    def on_lenof(self, node: TokenOperatorLenof, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_slize(self, node: TokenOperatorSlize, pos: TextPosition) -> ResNode:
        sl = self(node.operand, pos)
        if sl is not None: return sl
        for index in node.position_start:
            index = self(index, pos)
            if index is not None: return index
        for dim in node.result_dimensions:
            dim = self(dim, pos)
            if dim is not None: return dim

    def on_index(self, node: TokenOperatorIndex, pos: TextPosition) -> ResNode:
        operand = self(node.operand, pos)
        if operand is not None: return operand
        return self(node.index, pos)

    def on_array_creation(self, node: TokenOperatorArrayCreation, pos: TextPosition) -> ResNode:
        for dim in node.operands:
            dim = self(dim, pos)
            if dim is not None: return dim

    def on_referencing(self, node: TokenOperatorReferencing, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_dereferencing(self, node: TokenOperatorDereferencing, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_field_access(self, node: TokenOperatorFieldAccess, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_field_access_pointer(self, node: TokenOperatorFieldAccessPointer, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_deinitializer(self, node: TokenOperatorDeInitializer, pos: TextPosition) -> ResNode:
        if pos in node.origin: return node
        return self(node.operand, pos)

    def on_error_node(self, err: TokenOperatorError, pos: TextPosition):
        if pos in err.origin:
            return err


it_expr = ItExpr()


class ItCont():
    def __call__(self, control: ControlABC, pos: TextPosition) -> ResNode:
        match control:
            case ControlCodeBlock(): return self.on_code_block(control, pos)
            case ControlFunctionDefinition(): return self.on_func_def(control, pos)
            case ControlExpression(): return self.on_expression_control(control, pos)
            case ControlReturn(): return self.on_return(control, pos)
            case ControlMassAssignment(): return self.on_mass_assignment(control, pos)
            case ControlIf(): return self.on_if(control, pos)
            case ControlWhile(): return self.on_while(control, pos)
            case ControlCycleControl(): return self.on_cycle_control(control, pos)
            case ControlTypedef(): return self.on_typedef(control, pos)
            case ControlImport(): return self.on_import(control, pos)
            case ControlExport(): return self.on_export(control, pos)
            case ControlClass(): return self.on_class(control, pos)
            case ControlEnum(): return self.on_enum(control, pos)

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, pos: TextPosition) -> ResNode:
        return it_expr(exp, pos)

    def on_code_block(self, code: ControlCodeBlock, pos: TextPosition) -> ResNode:
        if pos not in code.origin: return None
        for control in code.block_parts:
            control = self(control, pos)
            if control is not None: return control

    def on_func_def(self, func_def: ControlFunctionDefinition, pos: TextPosition) -> ResNode:
        if pos in func_def.origin:
            for param in func_def.parameters:
                if pos in param.origin:
                    return param
                if pos in param.type.origin:
                    return param.type
            for res in func_def.results:
                if pos in res.origin: return res
            return func_def
        return self(func_def.code_block, pos)

    def on_expression_control(self, expr: ControlExpression, pos: TextPosition) -> ResNode:
        if pos not in expr.origin: return None
        return self.on_expr(expr.first, pos)

    def on_return(self, ret: ControlReturn, pos: TextPosition) -> ResNode:
        if pos not in ret.origin: return None
        for r in ret.results:
            r = self.on_expr(r, pos)
            if r is not None: return r

    def on_mass_assignment(self, mass_asg: ControlMassAssignment, pos: TextPosition) -> ResNode:
        if pos not in mass_asg.origin: return None
        for w in mass_asg.left:
            w = self.on_expr(w, pos)
            if w is not None: return w
        for r in mass_asg.right:
            r = self.on_expr(r, pos)
            if r is not None: return r

    def on_if(self, cond: ControlIf, pos: TextPosition) -> ResNode:
        if pos in cond.origin:
            return self.on_expr(cond.condition, pos)
        if_ = self(cond.block_if, pos)
        if if_ is not None: return if_
        return self(cond.block_else, pos)

    def on_while(self, while_: ControlWhile, pos: TextPosition) -> ResNode:
        if pos in while_.origin:
            return self.on_expr(while_.condition, pos)
        return self(while_.code_block, pos)

    def on_cycle_control(self, cycle_control: ControlCycleControl, pos: TextPosition) -> ResNode:
        if pos in cycle_control.origin:
            return cycle_control

    def on_typedef(self, typedef: ControlTypedef, pos: TextPosition) -> ResNode:
        if pos in typedef.typedef.type.origin:
            return typedef.typedef.type
        elif pos in typedef.origin:
            return typedef

    def on_import(self, import_: ControlImport, pos: TextPosition) -> ResNode:
        pass

    def on_export(self, export_: ControlExport, pos: TextPosition) -> ResNode:
        pass

    def on_class(self, cls: ControlClass, pos: TextPosition) -> ResNode:
        if pos in cls.origin:
            return cls
        return self(cls.rest, pos)

    def on_enum(self, enum: ControlEnum, pos: TextPosition) -> ResNode:
        if pos in enum.origin:
            return enum


it_cont = ItCont()


class ItContScopes(ItCont):
    def __init__(self):
        self.scopes: list[Scope] = []
        self.last_scope: Scope | None = None

    @property
    def current_scope(self) -> Scope:
        return self.scopes[-1]

    def enter_scope(self, creator):
        self.scopes.append(
            self.current_scope.get_child_scope_from_creator(creator)
        )
        self.last_scope = self.current_scope  # костылииииииии

    def exit_scope(self):
        self.scopes.pop()

    def start(self, code: ControlCodeBlock, scope: Scope, pos: TextPosition) -> tuple[ResNode, Scope]:
        self.scopes.append(scope)
        self.last_scope = scope
        return self(code, pos), self.last_scope

    def __call__(self, control: ControlABC, pos: TextPosition, add_to_f: bool = False) -> ResNode:
        match control:
            case ControlCodeBlock(): return self.on_code_block(control, pos, add_to_f)
            case ControlFunctionDefinition(): return self.on_func_def(control, pos)
            case ControlExpression(): return self.on_expression_control(control, pos)
            case ControlReturn(): return self.on_return(control, pos)
            case ControlMassAssignment(): return self.on_mass_assignment(control, pos)
            case ControlIf(): return self.on_if(control, pos)
            case ControlWhile(): return self.on_while(control, pos)
            case ControlCycleControl(): return self.on_cycle_control(control, pos)
            case ControlTypedef(): return self.on_typedef(control, pos)
            case ControlImport(): return self.on_import(control, pos)
            case ControlExport(): return self.on_export(control, pos)
            case ControlClass(): return self.on_class(control, pos)
            case ControlEnum(): return self.on_enum(control, pos)

    def on_code_block(self, code: ControlCodeBlock, pos: TextPosition, add_scope: bool = False) -> ResNode:
        if pos not in code.origin: return None
        if add_scope:
            self.enter_scope(code)
        for control in code.block_parts:
            control = self(control, pos, True)
            if control is not None: return control
        if add_scope:
            self.exit_scope()

    def on_func_def(self, func_def: ControlFunctionDefinition, pos: TextPosition) -> ResNode:
        if pos in func_def.origin:
            for param in func_def.parameters:
                if pos in param.origin:
                    return param
                if pos in param.type.origin:
                    return param.type
            for res in func_def.results:
                if pos in res.origin: return res
            return func_def

        self.enter_scope(func_def)
        inn = self(func_def.code_block, pos)
        self.exit_scope()
        return inn

    def on_if(self, cond: ControlIf, pos: TextPosition) -> ResNode:
        if pos in cond.origin:
            return self.on_expr(cond.condition, pos)
        self.enter_scope((cond, cond.block_if))
        if_ = self(cond.block_if, pos)
        self.exit_scope()
        if if_ is not None: return if_
        self.enter_scope((cond, cond.block_else))
        else_ = self(cond.block_else, pos)
        self.exit_scope()
        return else_

    def on_while(self, while_: ControlWhile, pos: TextPosition) -> ResNode:
        if pos in while_.origin:
            return self.on_expr(while_.condition, pos)
        self.enter_scope(while_)
        inn = self(while_.code_block, pos)
        self.exit_scope()
        return inn

    def on_class(self, cls: ControlClass, pos: TextPosition) -> ResNode:
        if pos in cls.origin:
            return cls
        self.enter_scope(cls)
        inn = self(cls.rest, pos)
        self.exit_scope()
        return inn


def position_to_node(module: Module, position: TextPosition) -> ResNode:
    return it_cont(module.code, position)


def position_to_node_with_scope(module: Module, position: TextPosition) -> tuple[ResNode, Scope]:
    it = ItContScopes()
    return it.start(module.code, module.scope, position)

