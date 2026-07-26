from .Simple import *
from .Types.Simple import IteratorModule
from .STDModules import get_path_to_std_module, get_path_to_std_header


__all__ = ('make_makefile',)


class ItModule(IteratorModule):
    """
    Должен собрать все импользуемые std модули
    """
    def __init__(self):
        self.all_std: set[str] = set()
        self.all_paths: list[str] = []

    def on_module(self, module: Module):
        if module.is_std:
            self.all_std.add(module.transfer_path.name)
        else:
            self.all_paths.append(
                module.path_c.as_posix()
            )
        super().on_module(module)


def make_makefile(modules: list[Module], result_path: Path):
    """
    Создаёт точку входа
    """
    makefile = (result_path / f'makefile')

    it_module = ItModule()
    it_module.many_modules(modules)

    with open(makefile, 'w') as f:
        f.write(rf'''
CC       = gcc
CFLAGS   = -I{get_path_to_std_header()} -O2 # -g # -Wall -Wextra
LDFLAGS  = -mconsole
TARGET   = program.exe

SOURCES := { # просто перечислен всё
    ' \\\n'.join(
        p for p in it_module.all_paths
    )}
    
SOURCES += src/main.c

{
    ''.join(
        f'SOURCES += {get_path_to_std_module(mod)}\n'
        for mod in it_module.all_std
    )
}

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

''')






