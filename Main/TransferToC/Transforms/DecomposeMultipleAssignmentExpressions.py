from .Utils import *


"""
В наших выражениях могут встречаться множественные присваивания в разных 
ветвях. Мы разделим эти ветви, чтобы гарантировать порядок их вычисления
"""


__all__ = ('decompose_multiple_assignment_expressions',)


class ItExpr(IteratorExpression):
    def __init__(self, data: DataContainer, code_block: ControlCodeBlock, index: int):
        self.data = data
        self.code_block = code_block
        self.index = index
        self.first_assignment_found = False

    def on_assignment(self, node: TokenOperatorAssignment, parent: TypeExpressionParent):
        # проверка, пропускаем первый нод
        skip = False
        if not self.first_assignment_found:
            skip = True
            self.first_assignment_found = True

        # сперва проходимся по дереву далее, потом разделяем
        super().on_assignment(node, parent)
        if skip:
            return

        # делаем новую переменную, куда записываем промежуточный результат
        temp_var_name = get_unique_name(self.data.all_names, '_decompose')
        temp_var_def = TokenOperatorVariableDefinition(
            temp_var_name, node.res_type, zero_origin
        )
        # присвоение всего этого временной переменной
        temp_var_assignment = TokenOperatorAssignment(
            temp_var_def, node, zero_origin, node.res_type
        )
        # записываем это в выражение за существующим
        temp_var_expression = ControlExpression(
            temp_var_assignment, zero_origin
        )
        self.code_block.block_parts.insert(self.index, temp_var_expression)
        # доступ к нашей переменной
        temp_var_access = TokenVariableAccess(
            temp_var_name, zero_origin, False, temp_var_def
        )
        # и заменяем это всё на обращение к временной переменной
        change_child(parent, node, temp_var_access)
        # self.expr_it.scope.add_variable(var_def)


class ItCont(IteratorControl):
    def __init__(self, data: DataContainer):
        self.data = data
        self.code_blocks: list[ControlCodeBlock] = []

    def on_code_block(self, code: ControlCodeBlock):
        self.code_blocks.append(code)
        super().on_code_block(code)
        self.code_blocks.pop()

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        ItExpr(
            self.data, self.code_blocks[-1], self.code_blocks[-1].block_parts.index(parent)
               )(
            exp, parent
        )

    def on_if(self, cond: ControlIf):
        index = self.code_blocks[-1].block_parts.index(cond)
        ItExpr(
            self.data, self.code_blocks[-1], index
               )(
            cond.condition, cond
        )
        self(cond.block_if)
        self(cond.block_else)


class ItModule(IteratorModule):
    def __init__(self, data: DataContainer):
        self.it_control = ItCont(data)

    def on_module(self, module: Module):
        self.it_control(module.code)
        super().on_module(module)


def decompose_multiple_assignment_expressions(modules: Module | list[Module], data: DataContainer):
    """
    Разделяет ветви с множественными присваиваниями в одном выражении для гарантирования порядка их вычисления.
    """
    it_module = ItModule(data)
    it_module.many_modules(modules)












