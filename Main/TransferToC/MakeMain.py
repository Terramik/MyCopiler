from .Types.Simple import IteratorModule
from ...Definitions import TypesShortener as types
from .Simple import *
from uuid import uuid4


__all__ = ('make_main',)


class ItModule(IteratorModule):
    """
    Должен: найти пользовательскую функцию main, собрать все инициализаторы глобальных фунций
    """
    def __init__(self):
        self.main: ControlFunctionDefinition | None = None
        self.main_module: Module | None = None
        self.variables_initializers: list[Module] = []
        self.std_initializers: set[str] = set()

    # делаем мы так(проход в обратном порядке) чтобы инициализаторы переменных были в правильном порядке
    def on_module(self, module: Module):
        # работаем в обратном проходе(для правильного порядка инициализаторов глобальных функций
        super().on_module(module)
        if not module.is_std:
            # ищём main
            if module.type == Module.Types.Main:
                f = module.scope.find_function_in_cur_scope('not_very_main')
                assert f
                self.main = f
                self.main_module = module
            # инициализатор
            if module.global_variables_initializer is not None:
                self.variables_initializers.append(module)
        else:
            self.std_initializers.add(
                f'vars_initializer_{module.transfer_path.name}'
            )


def write_import(it_module: ItModule, file: TextIO):
    file.write(f'#include "../include/{it_module.main_module.relative_path.with_suffix('.h').as_posix()}"\n')
    for mod in it_module.variables_initializers:
        file.write(f'#include "../include/{mod.relative_path.with_suffix('.h').as_posix()}"\n')


def write_globals_initializer(it_module: ItModule, file: TextIO):
    for std in it_module.std_initializers:
        file.write(f'{std}();')
    for mod in it_module.variables_initializers:
        file.write(f'{mod.global_variables_initializer}();')


def make_main(modules: list[Module], result_path: Path):
    """
    Создаёт точку входа
    """
    main = (result_path / f'src/main.c')
    # собираем данные
    it_module = ItModule()
    it_module.many_modules(modules)

    with open(main, 'w') as f:
        f.write('''
#include "../include/project_base.h"         
''')
        write_import(it_module, f)
        # собственно наша точка входа
        f.write('''
int main() {        
''')
        # инициализаторы
        write_globals_initializer(it_module, f)

        # немного магичем с результатами main
        if it_module.main.var.type == types.func([], [types.int64]):
            f.write('''
return not_very_main.func(not_very_main.env);
''')
        else:
            f.write('''
    not_very_main.func(not_very_main.env);
return 0;
''')
        f.write('}\n')




