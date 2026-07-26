from .Utils import *
from ..Transforms.Utils import *

"""
Модуль собирает все имена, но ни как их не меняет, создан исключительно для стандартных модулей и их особой структуры
"""


class ItCont(IteratorControl):
    def __init__(self):
        self.all_names = set()

    def on_func_def(self, func_def: ControlFunctionDefinition):
        self.all_names.add(func_def.name)
        # аргументы тоже
        for arg in func_def.parameters:
            self.all_names.add(arg.name)
        super().on_func_def(func_def)

    def on_expression_control(self, expr: ControlExpression):
        if isinstance(expr.first, TokenOperatorVariableDefinition):
            self.all_names.add(expr.first.name)

    def on_class(self, cls: ControlClass):
        self.all_names.add(cls.name)
        super().on_class(cls)


class ItModule(IteratorModule):
    def __init__(self, all_names: set[str]):
        self.all_names = all_names
        self.it_control = ItCont()

    def on_module(self, module: Module):
        for exp in module.export_:
            if isinstance(exp.thing, TokenOperatorVariableDefinition):
                self.all_names.add(exp.thing.name)
        self.it_control(module.code)
        super().on_module(module)


def collect_all_names(modules: Module | list[Module], data: DataContainer):
    """
    Собирает все имена, ничего не меняет, создан для стандартных модулей.
    """
    it_module = ItModule(data.all_names)
    it_module.many_modules(modules)
