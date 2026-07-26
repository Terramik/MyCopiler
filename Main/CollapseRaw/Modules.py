from __future__ import annotations
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


def is_import(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Import_Part1.value:
        return True
    return False


def collapse_import(data: list[TokenRawABC]) -> ControlRawImport:
    i = 0
    n = len(data)
    while i < n:
        cur = data[i]
        if isinstance(cur, TokenRawWord) and cur.word == KeyWords.Import_Part2.value:
            part2_i = i
            break
        i += 1
    else:
        raise OurSyntaxError(f'В импорте должно быть {KeyWords.Import_Part2.value}',
                             data[0].origin + data[-1].origin)

    file = data[1:part2_i]
    if not file:
        raise OurSyntaxError('В импорте не указан файл',
                             data[0].origin + data[part2_i].origin)

    names = data[part2_i + 1:]
    if not names:
        raise OurSyntaxError('В импорте не указаны импортируемые имена',
                             data[part2_i].origin + data[-1].origin)

    return ControlRawImport(
        file, split_by_comma(names, 'Имене в импорте должны быть указаны'),
        data[0].origin + data[-1].origin
    )


def is_export(data: list[TokenRawABC]) -> bool:
    first = data[0]
    if isinstance(first, TokenRawWord) and first.word == KeyWords.Export.value:
        return True
    return False


def collapse_export(data: list[TokenRawABC]) -> ControlRawExport:
    names = data[1:]
    if not names:
        raise OurSyntaxError('В экспорте не указаны экспортируемые имена',
                             data[0].origin + data[-1].origin)

    return ControlRawExport(
        split_by_comma(names, 'Имена в экспорте должны быть указаны'),
        data[0].origin + data[-1].origin
    )
