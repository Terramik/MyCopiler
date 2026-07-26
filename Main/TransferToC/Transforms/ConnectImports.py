from .Utils import *


"""
Так как все имена теперь уникальные, мы можем объединить экспортируемые и импортируемые штуки 
под одним именем без каких-либо проблем, и получить взаимосвязанное поле имён, готовое к трансляции в си.
"""


class ItModule(IteratorModule):
    def __init__(self, data: DataContainer):
        self.data = data

    def on_module(self, module: Module):
        # в обратном порядке, чтобы начинать с листьев, и "накапливать" псевдонимы
        super().on_module(module)
        # проходимся по всем импортированным переменным, и даём им имя их прародителя.
        for imp in module.import_:
            if isinstance(imp.thing, TokenOperatorVariableDefinition):
                exp = imp.from_.find_export(imp.name)
                # также, освобождаем занятое имя
                self.data.all_names.remove(imp.thing.name)
                imp.thing.name = exp.thing.name


def connect_imports(modules: Module | list[Module], data: DataContainer):
    """
    Даёт всем импортированным переменным имена их прародителя, также исключает освободившиеся имена из all_names
    """
    it_module = ItModule(data)
    it_module.many_modules(modules)








