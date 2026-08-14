from ...Definitions.Scopes import Scope
from ...Definitions.TreeInterface import IteratorExpression, IteratorControl, IteratorScope
from ...Definitions.Tokens import *

"""
Должен сохранять, а потом удалять временные(не сохранённые) объекты(экземпляры класса с __del__) в выражениях
"""


__all__ = ('add_del_to_temporary_objects',)


class ItScope(IteratorScope):
    def __init__(self):
        self.classes_with_del = []

    # собирает все классы с __del__
    def on_scope(self, scope: Scope):
        for var in scope.variables:
            if var.type == t_error:
                continue
            if var.type.is_simple_class:
                cls = var.type.cls
                if cls.is_bad:
                    continue
                del_ = cls.find_class_field('__del__')
                if del_ is not None:
                    self.classes_with_del.append(cls)
        super().on_scope(scope)


class ItExpr(IteratorExpression):
    counter = 1

    def __init__(self, classes_with_del: list[ControlClass], scope: Scope, code: ControlCodeBlock, index: int):
        self.classes_with_del = classes_with_del
        self.scope = scope
        self.code = code
        self.index = index + 1
        # для отслеживания, что были за родители
        self.parents: list[TokenOperatorWvalueABC | TokenOperatorRvalueABC] = []

    def is_in_classes_with_del(self, cls: ControlClass):
        for c in self.classes_with_del:
            if c is cls:
                return True
        return False

    @staticmethod
    def is_simple_or_array(t: Type):
        while t.is_mod_array:
            t = t.without_one_modifier()
        return t.is_mod_usual

    def __call__(self, node: TokenOperatorRvalueABC | TokenOperatorWvalueABC, parent: TypeExpressionParent):
        self.parents.append(node)
        super().__call__(node, parent)
        self.parents.pop()

    def on_f_call(self, node: TokenOperatorFunctionCall, parent: TypeExpressionParent):
        # в обратном порядке
        super().on_f_call(node, parent)

        if node.res_type == t_error:
            return

        # экземпляры могут делать только функции
        # если эта функция возвращает экземпляр класса с __del__
        if node.res_type is not None and \
                node.res_type.is_simple_class_instance and \
                self.is_in_classes_with_del(node.res_type.cls) and\
                self.is_simple_or_array(node.res_type):
            # если это не массив(или объект) присвоенный(или удалённый)

            # без самого себя
            parents = self.parents[:-1]

            # если эта штука в ретёрн - пропускаем
            if not parents and isinstance(parent, ControlReturn):
                return

            last = parents.pop() if parents else None
            while isinstance(last, TokenOperatorArrayCreation):
                if last:
                    last = parents.pop()
                else:
                    last = None

            if not isinstance(last, (TokenOperatorAssignment, TokenOperatorDeInitializer)):
                # оно не было сохранено(или не удалено сразу), значит, мы должно
                # сохранить его во временную переменную, использовать, а потом удалить.
                temp_var_name = self.scope.get_unique_name(f'expr_del_temp_var_{self.counter}', True)
                self.counter += 1

                temp_var_def = TokenOperatorVariableDefinition(
                    temp_var_name, node.res_type, zero_origin
                )
                temp_var_access = TokenVariableAccess(
                    temp_var_name, zero_origin, False, temp_var_def
                )
                # записываем результат во временную переменную
                new_node = TokenOperatorAssignment(
                    temp_var_def, node, node.origin, node.res_type
                )
                change_child(parent, node, new_node)
                # теперь удаляем штуку
                self.code.block_parts.insert(self.index, ControlExpression(
                    TokenOperatorDeInitializer(
                        temp_var_access, zero_origin, node.res_type
                    ), zero_origin
                    )
                )
                self.scope.add_variable(temp_var_def)


class ItCont(IteratorControl):
    def start(self, code: ControlCodeBlock):
        self.on_code_block(code, False)

    def __init__(self, classes_with_del: list[ControlClass], global_scope: Scope):
        # нужен для учёта того, куда дописывать штуки
        self.classes_with_del = classes_with_del
        self.code_block: list[ControlCodeBlock] = []
        self.scopes: list[Scope] = [global_scope]

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC, index: int):
        it_expr = ItExpr(
            self.classes_with_del, self.scopes[-1], self.code_block[-1], index
        )
        it_expr(exp, parent)

    def on_code_block(self, code: ControlCodeBlock, find_scope_here: bool = True):
        self.code_block.append(code)
        if find_scope_here:
            self.scopes.append(
                self.scopes[-1].get_child_scope_from_creator(code)
            )
        # чтобы итерироваться по изначальным
        unchanged = code.block_parts[:]
        for control in unchanged:
            self(control)
        self.scopes.pop()
        self.code_block.pop()

    def on_expression_control(self, expr: ControlExpression):
        self.on_expr(expr.first, expr,
                     self.code_block[-1].block_parts.index(expr))

    def on_return(self, ret: ControlReturn):
        index = self.code_block[-1].block_parts.index(ret)
        for r in ret.results:
            self.on_expr(r, ret, index)

    def on_mass_assignment(self, mass_asg: ControlMassAssignment):
        index = self.code_block[-1].block_parts.index(mass_asg)
        for w in mass_asg.left:
            self.on_expr(w, mass_asg, index)
        for r in mass_asg.right:
            self.on_expr(r, mass_asg, index)

    def on_if(self, cond: ControlIf):
        self.on_expr(cond.condition, cond,
                     self.code_block[-1].block_parts.index(cond))

        self.scopes.append(
            self.scopes[-1].get_child_scope_from_creator((cond, cond.block_if))
        )
        self.on_code_block(cond.block_if, False)

        self.scopes.append(
            self.scopes[-1].get_child_scope_from_creator((cond, cond.block_else))
        )
        self.on_code_block(cond.block_else, False)


    def on_while(self, while_: ControlWhile):
        self.on_expr(while_.condition, while_,
                     self.code_block[-1].block_parts.index(while_))
        self.scopes.append(
            self.scopes[-1].get_child_scope_from_creator(while_)
        )
        self.on_code_block(while_.code_block, False)

    def on_class(self, cls: ControlClass):
        self.scopes.append(
            self.scopes[-1].get_child_scope_from_creator(cls)
        )
        self.on_code_block(cls.rest, False)

    def on_func_def(self, func_def: ControlFunctionDefinition):
        self.scopes.append(
            self.scopes[-1].get_child_scope_from_creator(func_def)
        )
        self.on_code_block(func_def.code_block, False)


def add_del_to_temporary_objects(code: ControlCodeBlock, scope: Scope):
    it_scope = ItScope()
    it_scope(scope)
    it_control = ItCont(it_scope.classes_with_del, scope)
    it_control.start(code)





