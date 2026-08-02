from ...Definitions.Base import *
import sys


def print_error_location(origin: TokenOrigin) -> None:
    """
    Печатает в stdout сообщение об ошибке с указанием места в файле.
    Строки и колонки в origin имеют нулевую индексацию, но в выводе
    номера строк показываются с единицы.
    """
    file_path = origin.file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Не удалось прочитать файл {file_path}: {e}", file=sys.stderr)
        return

    start_line = origin.start.line
    end_line = origin.end.line
    if start_line < 0 or end_line < 0 or start_line >= len(lines) or end_line >= len(lines):
        print("Ошибка: указанная позиция выходит за пределы файла", file=sys.stderr)
        return

    # Ширина для выравнивания номеров строк
    max_line_num = end_line + 1  # т.к. номера с 1
    width = len(str(max_line_num))

    for line_idx in range(start_line, end_line + 1):
        line = lines[line_idx].rstrip('\n')  # убираем перевод, но сохраняем пробелы

        # Определяем начало и конец подчёркивания для текущей строки
        if line_idx == start_line:
            start_col = origin.start.column
        else:
            start_col = 0

        if line_idx == end_line:
            end_col = origin.end.column
        else:
            end_col = len(line)  # подчёркиваем до конца строки

        # Корректировка, чтобы не выходить за длину строки
        if start_col > len(line):
            start_col = len(line)
        if end_col > len(line):
            end_col = len(line)
        if end_col < start_col:
            end_col = start_col

        # Печатаем строку с номером
        print(f"{line_idx + 1:>{width}}: {line}")

        # Строим строку с каретками (пробелы + '^')
        if end_col - start_col > 0:
            caret = ' ' * start_col + '^' * (end_col - start_col)
        else:
            # Если диапазон нулевой, показываем одну крышку в позиции start_col
            caret = ' ' * start_col + '^'

        # Отступ для выравнивания с номером строки
        indent = ' ' * (width + 2)  # +2 за счёт ": "
        print(indent + caret)