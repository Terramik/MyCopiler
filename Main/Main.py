from .Modules import make_modules
from .TransferToC import transfer_to_c, retransfer_str_modules
from pathlib import Path
from ..Definitions.Exceptions import *
from .Errors import print_error_location
from .Settings import settings_load
import shutil
import argparse
import sys


path_to_scripts = (Path(__file__).resolve().parent.parent / 'scripts')


# path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')


# m
file_path = path_to_scripts / r'Better\Math\Matrices.mylang'


result_path = path_to_scripts / r'result'


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

        if result_path.exists() and not result_path.is_dir():
            raise ValueError(f'Выходной путь {result_path.as_posix()} должен быть директорией')

        # сама компиляция
        try:
            the_module = make_modules(file_path)
        except OurSyntaxError as err:
            print_error_location(err.position)
            print(err)
        except SemanticError as err:
            print_error_location(err.position)
            print(err)
            # raise err
        else:
            if result_path.exists():
                shutil.rmtree(result_path)
            transfer_to_c(the_module, result_path, args.compiler)

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
# классы для std
# DONE: прератор деинициализатор


# перечисления
# DONE: сырые и тесты
# DONE: светрка... можно и без тестов
# DONE: типы для этого всего
# DONE: анализ и тесты
# DONE: модификация доступа к полю, сравнения, присваивания
# DONE: трансляция потом
# перечисления для std



