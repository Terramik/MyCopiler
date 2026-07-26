from .Utils import *


class IteratorScope:
    def __call__(self, scope: Scope):
        self.on_scope(scope)

    def on_scope(self, scope: Scope):
        for s in scope.children:
            self.on_scope(s)