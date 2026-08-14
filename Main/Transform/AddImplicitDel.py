from ...Definitions.Scopes import Scope
from ...Definitions.TreeInterface import IteratorExpression, IteratorControl, IteratorScope
from ...Definitions.Tokens import *

"""
Должен вставлять неявные __del__ для массивов и просто объектов при выходе из областей видимости, где они были созданы
"""


__all__ = ('add_implicit_del',)


# проверяет, что это тот тип, что нам нужен
def is_type_class_instance(t: Type, classes_with_del: list[ControlClass]):
    if t.is_simple_class_instance:
        cls = t.cls
        # класс должен иметь __del__
        for c in classes_with_del:
            if c is cls:
                # это должен быть или элемент или массив любой размерности
                while t.is_mod_array:
                    t = t.without_one_modifier()

                if t.is_mod_usual:
                    # делаем переменную
                    return True
    return False


class ItExpr(IteratorExpression):
    def __init__(self, classes_with_del: list[ControlClass], vars_states: list[tuple[TokenOperatorVariableDefinition, bool]] ):
        self.classes_with_del = classes_with_del
        self.vars_states = vars_states

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        if node.res_type == t_error:
            return

        if is_type_class_instance(node.type, self.classes_with_del):
            self.vars_states.append((node, False))

    def on_assignment(self, node: TokenOperatorAssignment, parent: TypeExpressionParent):
        # проходимся в обратном порядке
        super().on_assignment(node, parent)
        if node.res_type == t_error:
            return

        # если мы записываем в переменную, то обновляем её, что там теперь что-то есть.
        if isinstance(node.left, TokenVariableAccess | TokenOperatorVariableDefinition):
            var = node.left.var_def if isinstance(node.left, TokenVariableAccess) else node.left
            for i, (var_, _) in enumerate(self.vars_states):
                if var is var_:
                    self.vars_states[i] = (var, True)
                    break

    def on_deinitializer(self, node: TokenOperatorDeInitializer, parent: TypeExpressionParent):
        # и тут тоже
        super().on_deinitializer(node, parent)
        if node.res_type == t_error:
            return

        # если мы де инициализируем, то мы де инициализируем
        if isinstance(node.operand, TokenVariableAccess):
            var = node.operand.var_def
            for i, (var_, _) in enumerate(self.vars_states):
                if var is var_:
                    self.vars_states[i] = (var, False)
                    break


class ItCont(IteratorControl):
    def __init__(self, classes_with_del: list[ControlClass]):
        # классы, чьи объекты нужно проверять
        self.classes_with_del: list[ControlClass] = classes_with_del
        # переменные с экземплярами выше указанных классов, bool говорит, если ли там что-то не удалённое, для всех блоков кода
        self.vars_states: list[list[tuple[TokenOperatorVariableDefinition, bool]]] = []
        # код блока, куда нужно писать del
        self.code_blocks: list[ControlCodeBlock] = []
        # чтобы понять, в классе мы или нет
        self.is_class: list[bool] = []

    def enter_block(self, code_block: ControlCodeBlock, are_we_in_class: bool = False):
        self.is_class.append(are_we_in_class)
        self.vars_states.append([])  # входим в блок кода
        self.code_blocks.append(code_block)

    def exit_block(self):
        code_block = self.code_blocks.pop()
        cur_var_state = self.vars_states.pop()
        # если в переменной что-то есть, то мы вставляем неявное удаление
        for var, is_exist in cur_var_state:
            if is_exist:
                code_block.block_parts.append(
                    ControlExpression(
                        TokenOperatorDeInitializer(
                            TokenVariableAccess(
                                var.name, zero_origin, False, var
                            ), zero_origin, var.type
                        ), zero_origin
                    )
                )

    # проходимся по выражениям и проверяем всё
    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        itexpr = ItExpr(self.classes_with_del, self.vars_states[-1])
        itexpr(exp, parent)

    def on_code_block(self, code: ControlCodeBlock, add_things: bool = True):
        if add_things:
            self.enter_block(code)
        super().on_code_block(code)
        if add_things:
            self.exit_block()

    # тут мы переопределяем штуки, чтобы входить и выходить из блоков кода
    def on_func_def(self, func_def: ControlFunctionDefinition):
        self.enter_block(func_def.code_block)
        self.on_code_block(func_def.code_block, False)
        self.exit_block()

    def on_while(self, while_: ControlWhile):
        self.on_expr(while_.condition, while_)
        self.enter_block(while_.code_block)
        self.on_code_block(while_.code_block, False)
        self.exit_block()

    def on_if(self, cond: ControlIf):
        self.on_expr(cond.condition, cond)

        self.enter_block(cond.block_if)
        self.on_code_block(cond.block_if, False)
        self.exit_block()

        self.enter_block(cond.block_else)
        self.on_code_block(cond.block_else, False)
        self.exit_block()

    def on_class(self, cls: ControlClass):
        self.enter_block(cls.rest, True)
        self.on_code_block(cls.rest, False)
        self.exit_block()

    def on_return(self, ret: ControlReturn):
        # сначало пройдёмся
        super().on_return(ret)
        # теперь, если что-то на вершине это нужная нам переменная, то не будем её удалять, т.к. она возвращается
        for thing in ret.results:
            if isinstance(thing, TokenVariableAccess):
                if thing.res_type.is_simple_class_instance:
                    for i, (var, _) in enumerate(self.vars_states[-1]):
                        if thing.var_def is var:
                            self.vars_states[-1][i] = (var, False)
                            break


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


def add_implicit_del(code: ControlCodeBlock, scope: Scope):
    it_scope = ItScope()
    it_scope(scope)
    it_control = ItCont(it_scope.classes_with_del)
    it_control(code)



