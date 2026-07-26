from .Utils import *


class IteratorModule:
    def many_modules(self, module: Module | list[Module]):
        """
        Точка входа, не нужно её переопределять, работайте с on_module.
        """
        if isinstance(module, Module):
            self.on_module(module)
        else:
            for m in module:
                self.on_module(m)

    def on_module(self, module: Module):
        for m in module.imported_modules:
            self.on_module(m)



