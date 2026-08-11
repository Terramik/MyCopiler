from .Utils import *
from pathlib import Path

from ..Tokenize import tokenize_file
from ..CollapseRaw import collapse_raw
from ..ProcessRaw import process_raw
from ...Definitions.Enums import KeyWords
from ...Definitions.STDModules import std_modules
from ...Definitions.Exceptions import OurSyntaxError, SemanticError
from ..Analyze import analyze


def get_module(path: Path, import_origin: TokenOrigin) -> Module:
    """
    Читает модуль по пути, обрабатывает его до стадии обработки сырых конструкций
    """

    # это не обычный модуль, а модуль стандартной библиотеки
    if path.parent.name == KeyWords.Modules_std.value:
        name = path.stem
        if name not in std_modules:
            raise SemanticError(f'Модуль {name} не является частью стандартной библиотеки', import_origin)

        return std_modules[name]

    # это обычный модуль
    else:
        # проверяем файл
        if not path.exists():
            raise SemanticError(f'Модуля по пути {path} не существует', import_origin)

        # проходим файл до обработки сырых конструкций
        with open(path, 'r', encoding='utf-8') as f:
            raw_tokens = tokenize_file(f, path)
            raw_code, err = collapse_raw(raw_tokens)
            code, err2 = process_raw(raw_code)
        err = err + err2

        # готово
        return Module(
            Module.Types.Usual, path, code, errors=err
        )


def process_module(module: Module, processed_modules: dict[Path, Module], ignore_main: bool = False):
    errors = module.errors

    # стандартные не трогаем
    if module.type == Module.Types.Standard:
        return

    if module.path_to_file in processed_modules:
        return
    processed_modules[module.path_to_file] = module

    # собёрём импорты
    i = 0
    imports_ = []
    while i < len(module.code.block_parts) and isinstance(module.code.block_parts[i], ControlImport):
        imports_.append(module.code.block_parts[i])
        i += 1

    # теперь получаем модули
    processed: set[Path] = set()
    paths = set()
    modules = []

    for imp in imports_:
        path = (module.path_to_file / imp.path).with_suffix('.mylang').resolve()
        if path not in paths:
            if path in processed:
                continue
            processed.add(path)
            if path in processed_modules:
                modules.append(processed_modules[path])
            else:
                paths.add(path)
                mod = get_module(path, imp.origin)
                modules.append(mod)

    module.imported_modules = modules

    # обрабатываем
    for mod in modules:
        process_module(mod, processed_modules, ignore_main)

    imported = []
    imported_names = set()

    # теперь получаем то, что хотим импортировать
    for mod, imp in zip(modules, imports_):
        if not mod.is_std:
            mod = processed_modules[mod.path_to_file]
        imp: ControlImport
        imp.is_allowed = True # разрешаем
        # если всё, добавляем всё
        if imp.all:
            for exported in mod.export_:
                if exported.alias in imported_names:
                    errors.append(SemanticError(f'Имя {exported.alias} уже занято', imp.origin))
                    continue
                # копируем
                if isinstance(exported.thing, TokenOperatorVariableDefinition):
                    thing = TokenOperatorVariableDefinition(exported.alias, exported.thing.type, exported.thing.origin)
                else:
                    thing = ControlTypedef(Type.Typedef(exported.thing.typedef.type, exported.alias), exported.thing.origin)
                # добавляем
                imported.append(Module.ImportData(
                    mod, exported.alias, thing
                ))
                imported_names.add(exported.alias)

        # теперь, поимённо
        for name, alias in imp.names:
            exported = mod.find_export(name)
            # проверка
            if exported is None:
                errors.append(SemanticError(f'Имени {name} не обнаружено в импортируемом модуле', imp.origin))
            if alias in imported_names:
                errors.append(SemanticError(f'Имя {alias} уже занято', imp.origin))
            # копируем, добавляем псевдоним
            if isinstance(exported.thing, TokenOperatorVariableDefinition):
                thing = TokenOperatorVariableDefinition(alias, exported.thing.type, exported.thing.origin)
            else:
                thing = ControlTypedef(Type.Typedef(exported.thing.typedef.type, alias), exported.thing.origin)
            # добавляем
            imported.append(Module.ImportData(
                mod, name, thing
            ))
            imported_names.add(alias)

    module.import_ = imported

    # добавляем штуки и анализируем
    to_add = [i.thing for i in imported]
    module.scope, err = analyze(module.code, to_add)
    module.errors.extend(err)

    # проверка на присутствие точки входа
    if not ignore_main:
        if module.type == Module.Types.Usual and module.scope.find_function_in_cur_scope('main') is not None:
            errors.append(SemanticError('Точка входа вне основного модуля',
                                        module.scope.find_function_in_cur_scope('main').origin))
        elif module.type == Module.Types.Main and module.scope.find_function_in_cur_scope('main') is None:
            errors.append(SemanticError('Точки входа не обнаружено', module.code.origin))

    # теперь экспорт
    exported = []
    exported_names = set()

    for exp in filter(lambda x: isinstance(x, ControlExport), module.code.block_parts):
        exp: ControlExport
        # экспортируем все глобальные имена
        if exp.all:
            for var in module.scope.variables:
                if var.name in exported_names:
                    errors.append(SemanticError(f'Име {var.name} уже занято', exp.origin))
                    continue
                exported.append(Module.ExportData(
                    var, var.name
                ))
                exported_names.add(var.name)
            for typedef in module.scope.typedefs:
                if typedef.typedef.name in exported_names:
                    errors.append(SemanticError(f'Име {typedef.typedef.name} уже занято', exp.origin))
                    continue
                exported.append(Module.ExportData(
                    typedef, typedef.typedef.name
                ))
                exported_names.add(typedef.typedef.name)
            # классов нету(как и функций и ) т.к. они - переменные

        for name, alias in exp.names:
            if alias in exported_names:
                errors.append(SemanticError(f'Имя {alias} уже занято', exp.origin))
                continue
            thing = module.scope.find_variable_in_cur_scope(name) # это даст и функции, и классы, т.к. они переменные.
            if thing:
                exported.append(Module.ExportData(
                    thing, alias
                ))
            else:
                thing = module.scope.find_typedef_in_cur_scope(name)
                if thing:
                    exported.append(Module.ExportData(
                        thing, alias
                    ))
                else:
                    errors.append(SemanticError(f'Имени {name} не было найдено', exp.origin))
                    continue
            exported_names.add(alias)

    module.export_ = exported


