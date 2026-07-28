from .Modules import make_modules
from .TransferToC import transfer_to_c
from pathlib import Path
from ..Definitions.Exceptions import *
from .Errors import print_error_location
from .Settings import settings_load
import shutil


path_to_scripts = (Path(__file__).resolve().parent.parent / 'scripts')


# path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')


# m
file_path = path_to_scripts / r'Better\Math\Matrices.mylang'


result_path = path_to_scripts / r'result'


settings = settings_load()
if settings is None:
    raise ValueError('Не удалось загрузить настройки')

if not file_path.exists():
    raise FileNotFoundError('Такого файле нет.')

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
    transfer_to_c(the_module, result_path)



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











# with open(path_in, 'r') as f:
#     tokens = tokenize_file(f)
#     raw_code = collapse_raw(tokens)
#     code = process_raw(raw_code)
#     scope = analyze(code)
#     transform(code, scope)
#
#     # print_all(code, scope)
#     with open(path_out, 'w') as fw:
#         transfer_to_c(fw, code, scope)


# if __name__ == '__main__':
#     args = sys.argv[1:]
#     if len(args) == 3:
#         PRINT = True if args[0] == '1' else False
#         file_name = args[1]
#         compile = True if args[2] == '1' else False
#
#     path_in = os.path.join(path, f'{file_name}.txt')
#     path_out = os.path.join(path, f'{file_name}.c')
#     path_exe = os.path.join(path, f'{file_name}.exe')
#
#     with open(path_in, 'r') as f:
#         tokens = tokenize_file(f)
#
#     if PRINT:
#         print(s)
#         for t in tokens:
#             print(t, end=', ') # print(f'{t}-{t.origin}', end=', ')
#         print()
#         print(s)
#     raw_block = collapse_raw(tokens)
#     if PRINT:
#         for i in raw_block.block_parts:
#             print(i)
#         print(s)
#     block = process_raw(raw_block)
#     if PRINT:
#         for i in block.block_parts:
#             print(i)
#         print(s)
#         # print_all(block)
#     scope = analyze(block)
#     if PRINT:
#         for i in block.block_parts:
#             print(i)
#         print(s)
#         print_all(block, scope)
#     with open(path_out, 'w') as f:
#         transfer_to_c(f, block, scope)
#     if PRINT:
#         with open(path_out, 'r') as f:
#             print(f.read())
#         print(s)
#         # print_all(block, scope)
#
#     if compile:
#         subprocess.run(['gcc', path_out, '-o', path_exe])
#
#
#     # save_as_svg(block, scope)



# TODO:
# нужно будет создать свой printf, что будет работать с нашими спецификаторами, и что важнее, не требовать нуль-терминатора.
