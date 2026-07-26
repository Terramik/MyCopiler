from .Simple import *
from ....Definitions.TreeInterface import *


__all__ = ('collect_all_types',)


class ItExpr(IteratorExpression):
    def __init__(self, types: set[Type]):
        self.types = types

    def __call__(self, node: TokenOperatorRvalueABC | TokenOperatorWvalueABC, parent: TypeExpressionParent):
        if node.res_type is not None:
            node.res_type = node.res_type.full_type
            self.types.add(node.res_type)
        super().__call__(node, parent)


class ItCont(IteratorControl):
    def __init__(self, exp: ItExpr):
        self.types = exp.types
        self.exp = exp

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        self.exp(exp, parent)

    def on_func_def(self, func_def: ControlFunctionDefinition):
        for var in func_def.parameters:
            var.type = var.type.full_type
            self.types.add(var.type)
        func_def.var.type = func_def.var.type.full_type
        self.types.add(func_def.var.type)
        super().on_func_def(func_def)

    def on_typedef(self, typedef: ControlTypedef):
        self.types.add(typedef.typedef.type.full_type)

    def on_class(self, cls: ControlClass):
        # тип самого класса и его экземпляра
        self.types.add(cls.class_var.type)
        self.types.add(Type(Type.SimpleTypeClassInstance(cls), []))
        super().on_class(cls)

    def on_enum(self, enum: ControlEnum):
        self.types.add(enum.enum_var.type)
        self.types.add(Type(Type.SimpleTypeEnumInstance(enum), []))


class ItModule(IteratorModule):
    def __init__(self):
        self.types: set[Type] = set()
        self.it_control = ItCont(ItExpr(self.types))
        self.processed: set[Path] = set()

    def on_module(self, module: Module):
        if module.path_to_file in self.processed:
            return
        self.processed.add(module.path_to_file)

        for inp in module.import_:
            self.it_control(inp.thing)
        # экспорта нет, т.к. все вещи из него обязательно будут обработаны
        # в отличии от импорта, псевдонимов, и аргументов функций, что могут и
        # не быть использованы в выражениях, и не обработаны

        self.it_control(module.code)
        super().on_module(module)


def collect_all_types(module: list[Module] | Module) -> set[Type]:
    """
    Собирает все типы, используемые в программе.
    """
    it_module = ItModule()
    it_module.many_modules(module)
    # для массивов и срезов добавим также и меньшие типы, получаемые после индексации этих.
    for t in it_module.types.copy():
        if t.is_mod_array:
            while t.is_mod_array:
                t = t.without_one_modifier()
                it_module.types.add(t)
        elif t.is_mod_slize:
            dims = t.dimensions
            t = t.without_one_modifier()
            it_module.types.add(t)
            for i in range(1, dims):
                it_module.types.add(t.add_modifier(Type.ModifierSlise(i)))

    return it_module.types




