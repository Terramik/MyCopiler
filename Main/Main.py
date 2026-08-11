from .Modules import make_modules
from .TransferToC import transfer_to_c, retransfer_str_modules
from pathlib import Path
from ..Definitions.Exceptions import *
from .Errors import print_error_location
from .Settings import settings_load
import argparse
import sys


# ===== Настройки =====

settings = settings_load()
if settings is None:
    raise ValueError('Не удалось загрузить настройки')


# ===== Аргументы =====

# делаем штуку
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

# пересборка модулей
parser_retransfer = subparsers.add_parser('retransfer_std_modules',
                                          help='Пересобрать стандартные модули')
parser_retransfer.add_argument('-compiler', '--compiler', default=settings['compiler'], help='Компилятор C')

# обычная компиляция
parser_compile = subparsers.add_parser('compile', help='Скомпилировать файл')
parser_compile.add_argument('input', help='Входной файл')
parser_compile.add_argument('output', help='Выходной файл')
parser_compile.add_argument('-compiler', '--compiler', default=settings['compiler'], help='Компилятор C')


# используем

# вставим 'compile' неявно
if len(sys.argv) >= 2 and sys.argv[1] not in ('retransfer_std_modules', 'compile', '-h', '--help'):
    sys.argv.insert(1, 'compile')

args = parser.parse_args()


# ===== Основное =====


match args.command:
    case 'compile':
        # пути и их проверки
        file_path = Path(args.input)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path

        if not file_path.exists():
            raise FileNotFoundError(f'Файла по пути {file_path.as_posix()} нет')
        elif file_path.suffix != '.mylang':
            raise ValueError(f'Файл {file_path.as_posix()} должен иметь расширение .mylang')

        result_path = Path(args.output)
        if not result_path.is_absolute():
            result_path = Path.cwd() / result_path

        if result_path.suffix != '':
            raise ValueError(f'Выходной путь {result_path.as_posix()} не должен иметь расширения')

        # сама компиляция
        the_module, errors = make_modules(file_path)
        if not errors:
            transfer_to_c(the_module, result_path, args.compiler)
        else:
            print(errors)
            for err in errors:
                print_error_location(err.position)

    case 'retransfer_std_modules':
        retransfer_str_modules(args.compiler)
    case _:
        raise ValueError('Неправельные команды')






# THE PLAN
# DONE: добавить сырую штуку для свёртки класса, и его анализированную версию
# DONE: модифицировать тип, чтобы добавить новый базовый тип - собственно класс
# DONE: добавить штуку для анализа класса: имя, поля экземпляра, магические методы, обычные методы, классовые переменные
# DONE: добавить использование магических методов для определения того, можно ли сделать что-то с классами.
# DONE: добавить 2.5 типа операторов ".", "->", "del" ноды для них, и штуки для их свёртки и анализа
# DONE: добавить "вызов" класса и перенаправление в __init__
# DONE: написать анализатор класса и его штук
# DONE: модифицировать scope и module(импорты и экспорты) чтобы работать с этим всем.
# DONE: использовать условия только как вложены if(){}else{}
# DONE: написать тесты для свёртки
# DONE: написать тесты для обработки
# DONE: написать тесты для анализа

# DONE: тип класса
# DONE: перемененные класса и объекта
# DONE: вложенные типы
# DONE: магические методы
# DONE: вызов магических методов
# DONE: деинициализатор

# DONE: встройка в глобальное переименование, и потом сименование
# DONE: типы для классов и их экземпляров
# DONE: трансляция классов, из методов и их создание
# DONE: встройка специальной штуки в __init__
# DONE: наполнение структуры класса
# DONE: обновить трансляцию под новые условия(control if)
# DONE: классы для std
# DONE: прератор деинициализатор
# gcc -IC:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\include -O2 C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/3D/Cube/maind787bc4e0f224d09b7e2a199e2892663.c C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/3D/Cube/defines.c C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/Math/Quaternions.c C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/Math/Matrices.c C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/main.c C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\io_our.c C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\testing_our.c C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\time_our.c C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\math_our.c C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\mem_our.c -o progexe -mconsole

# перечисления
# DONE: сырые и тесты
# DONE: светрка... можно и без тестов
# DONE: типы для этого всего
# DONE: анализ и тесты
# DONE: модификация доступа к полю, сравнения, присваивания
# DONE: трансляция потом
# перечисления для std

# DONE: гит
# DONE: улучшить интерфейс
# DONE: использовать компилятор си прям тут
# DONE: пофиксить размерности неявного среза
