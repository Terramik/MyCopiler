import pytest
from .Simple import *
from ...Definitions.Enums import BaseTypes, TokenOperatorBinaryTypes, TokenOperatorPrefixTypes
from ...Definitions.Tokens import Type


def T(t: str, modifiers: list | None = None) -> CheckType:
    if modifiers is None:
        modifiers = []
    """Вспомогательная функция для создания CheckType."""
    return CheckType(Type.from_raw(t, modifiers, zero_origin))


def TTrue(type: Type) -> CheckType:
    return CheckType(type)


def TFull(t: BaseTypes, modifiers: list[Type.ModifierABS] | None = None) -> CheckType:
    if modifiers is None:
        modifiers = []
    return CheckType(Type(Type.SimpleTypeBase(t), []))


@pytest.mark.parametrize('code, expected_main_block, shorten_main', [
    # Простое присваивание
    (
        """
        def main() -> () {
            a = 5;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenLiteral('5', TFull(BaseTypes.int64))
                )
            )
        ]),
        True
    ),
    # Присваивание с арифметикой
    (
        """
        def main() -> () {
            a = b + c;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorBinary(
                        TokenOperatorBinaryTypes.ArfmAdd,
                        CheckTokenVariableAccess('b'),
                        CheckTokenVariableAccess('c')
                    )
                )
            )
        ]),
        True
    ),
    # Объявление переменной без инициализации
    (
        """
        def main() -> () {
            var x int32;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition('x', T('int32'))
            )
        ]),
        True
    ),
    # Объявление с инициализацией
    (
        """
        def main() -> () {
            var x int32 = 5;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('x', T('int32')),
                    CheckTokenLiteral('5', TFull(BaseTypes.int64))
                )
            )
        ]),
        True
    ),
    # Возврат одного значения
    (
        """
        def main() -> (int32) {
            return 42;
        }
        """,
        CheckControlCodeBlock([
            CheckControlReturn([
                CheckTokenLiteral('42', TFull(BaseTypes.int64))
            ])
        ]),
        True
    ),
    # Возврат нескольких значений
    (
        """
        def main() -> (int32, float64) {
            return 1, 2.0;
        }
        """,
        CheckControlCodeBlock([
            CheckControlReturn([
                CheckTokenLiteral('1', TFull(BaseTypes.int64)),
                CheckTokenLiteral('2.0', TFull(BaseTypes.float64))
            ])
        ]),
        True
    ),
    # Массовое присваивание
    (
        """
        def main() -> () {
            x, y = 1, 2;
        }
        """,
        CheckControlCodeBlock([
            CheckControlMassAssignment(
                [
                    CheckTokenVariableAccess('x'),
                    CheckTokenVariableAccess('y')
                ],
                [
                    CheckTokenLiteral('1', TFull(BaseTypes.int64)),
                    CheckTokenLiteral('2', TFull(BaseTypes.int64))
                ]
            )
        ]),
        True
    ),
    # Вызов функции
    (
        """
        def foo(a int32) -> (int32) { return a; }
        def main() -> () {
            foo(5);
        }
        """,
        # Глобальный блок содержит две функции: foo и main
        CheckControlCodeBlock([
            CheckControlFunctionDefinition(
                'foo',
                [CheckTokenOperatorVariableDefinition('a', T('int32'))],
                [T('int32')],
                CheckControlCodeBlock([
                    CheckControlReturn([
                        CheckTokenVariableAccess('a')
                    ])
                ])
            ),
            CheckControlFunctionDefinition(
                'main',
                [],
                [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorFunctionCall(
                            [CheckTokenLiteral('5', TFull(BaseTypes.int64))]
                        )
                    )
                ])
            )
        ]),
        False
    ),
    # Унарный минус
    (
        """
        def main() -> () {
            a = -b;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorPrefix(
                        TokenOperatorPrefixTypes.ArfmUnMin,
                        CheckTokenVariableAccess('b')
                    )
                )
            )
        ]),
        True
    ),
    # Приведение типа
    (
        """
        def main() -> () {
            a = b as int32;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorCast(
                        T('int32'),
                        CheckTokenVariableAccess('b')
                    )
                )
            )
        ]),
        True
    ),
    # Вложенный блок
    (
        """
        def main() -> () {
            {
                var x int32;
                x = 1;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlCodeBlock([
                CheckControlExpression(
                    CheckTokenOperatorVariableDefinition('x', T('int32'))
                ),
                CheckControlExpression(
                    CheckTokenOperatorAssignment(
                        CheckTokenVariableAccess('x'),
                        CheckTokenLiteral('1', TFull(BaseTypes.int64))
                    )
                )
            ])
        ]),
        True
    ),
    # Сложное выражение с приоритетами
    (
        """
        def main() -> () {
            a = b * c + d;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorBinary(
                        TokenOperatorBinaryTypes.ArfmAdd,
                        CheckTokenOperatorBinary(
                            TokenOperatorBinaryTypes.ArfmMul,
                            CheckTokenVariableAccess('b'),
                            CheckTokenVariableAccess('c')
                        ),
                        CheckTokenVariableAccess('d')
                    )
                )
            )
        ]),
        True
    ),
    # Выражение со скобками, меняющими приоритет
    (
        """
        def main() -> () {
            a = b * (c + d);
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorBinary(
                        TokenOperatorBinaryTypes.ArfmMul,
                        CheckTokenVariableAccess('b'),
                        CheckTokenOperatorBinary(
                            TokenOperatorBinaryTypes.ArfmAdd,
                            CheckTokenVariableAccess('c'),
                            CheckTokenVariableAccess('d')
                        )
                    )
                )
            )
        ]),
        True
    ),
    # Условная штука 1
    (
        """
        def main() -> () {
            if not false {
                var v int64;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlIf(
                CheckTokenOperatorPrefix(
                    TokenOperatorPrefixTypes.LogNot,
                    CheckTokenLiteral('false', TFull(BaseTypes.bool))
                ),
                CheckControlCodeBlock(
                    [
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'v', T('int64')
                            )
                        )
                    ]
                ),
                CheckControlCodeBlock([])
            )
        ]),
        True
    ),
    # Условная штука 2
    (
        """
        def main() -> () {
            if not false {
                var x int64;
            }
            else {
                var v int32;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlIf(
                CheckTokenOperatorPrefix(
                    TokenOperatorPrefixTypes.LogNot,
                    CheckTokenLiteral('false', TFull(BaseTypes.bool))
                ),
                CheckControlCodeBlock(
                    [
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'x', T('int64')
                            )
                        )
                    ]
                ),
                CheckControlCodeBlock(
                    [
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'v', T('int32')
                            )
                        )
                    ]
                )
            ),
        ]),
        True
    ),
    # Условная штука 3
    (
        """
        def main() -> () {
            if not false {
                var x int64;
            }
            elif false ^ true {
                xd();
            }
            elif true {
                var blobus bool;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlIf(
                CheckTokenOperatorPrefix(
                    TokenOperatorPrefixTypes.LogNot,
                    CheckTokenLiteral('false', TFull(BaseTypes.bool))
                ),
                CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'x', T('int64')
                            )
                        )
                ]),
                CheckControlCodeBlock([
                    CheckControlIf(
                        CheckTokenOperatorBinary(
                            TokenOperatorBinaryTypes.BitXor,
                            CheckTokenLiteral('false', TFull(BaseTypes.bool)),
                            CheckTokenLiteral('true', TFull(BaseTypes.bool))
                        ),
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorFunctionCall(
                                    []
                                )
                            )
                        ]),
                        CheckControlCodeBlock([
                            CheckControlIf(
                                CheckTokenLiteral('true', TFull(BaseTypes.bool)),
                                CheckControlCodeBlock([
                                        CheckControlExpression(
                                            CheckTokenOperatorVariableDefinition(
                                                'blobus', T('bool')
                                            )
                                        )
                                ]),
                                CheckControlCodeBlock([
                                ])
                            )
                        ])
                    ),

                ])
            ),
        ]),
        True
    ),
    # Простой цикл while
    (
        """
        def main() -> () {
            while x < 10 {
                x = x + 1;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlWhile(
                CheckTokenOperatorBinary(
                    TokenOperatorBinaryTypes.ComprLess,
                    CheckTokenVariableAccess('x'),
                    CheckTokenLiteral('10', TFull(BaseTypes.int64))
                ),
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenVariableAccess('x'),
                            CheckTokenOperatorBinary(
                                TokenOperatorBinaryTypes.ArfmAdd,
                                CheckTokenVariableAccess('x'),
                                CheckTokenLiteral('1', TFull(BaseTypes.int64))
                            )
                        )
                    )
                ])
            )
        ]),
        True
    ),
    # Цикл с break
    (
        """
        def main() -> () {
            while true {
                break;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlWhile(
                CheckTokenLiteral('true', TFull(BaseTypes.bool)),
                CheckControlCodeBlock([
                    CheckControlCycleControl(CycleControlTypes.break_)
                ])
            )
        ]),
        True
    ),
    # Цикл с continue
    (
        """
        def main() -> () {
            while x < 5 {
                if x == 3 {
                    continue;
                }
                x = x + 1;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlWhile(
                CheckTokenOperatorBinary(
                    TokenOperatorBinaryTypes.ComprLess,
                    CheckTokenVariableAccess('x'),
                    CheckTokenLiteral('5', TFull(BaseTypes.int64))
                ),
                CheckControlCodeBlock([
                    CheckControlIf(
                        CheckTokenOperatorBinary(
                            TokenOperatorBinaryTypes.ComprEq,
                            CheckTokenVariableAccess('x'),
                            CheckTokenLiteral('3', TFull(BaseTypes.int64))
                        ),
                        CheckControlCodeBlock([
                            CheckControlCycleControl(CycleControlTypes.continue_)
                        ]),
                        CheckControlCodeBlock([
                        ])
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenVariableAccess('x'),
                            CheckTokenOperatorBinary(
                                TokenOperatorBinaryTypes.ArfmAdd,
                                CheckTokenVariableAccess('x'),
                                CheckTokenLiteral('1', TFull(BaseTypes.int64))
                            )
                        )
                    )
                ])
            )
        ]),
        True
    ),
    # Вложенные циклы с break из внутреннего
    (
        """
        def main() -> () {
            while a < 10 {
                while b < 5 {
                    break;
                }
                a = a + 1;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlWhile(
                CheckTokenOperatorBinary(
                    TokenOperatorBinaryTypes.ComprLess,
                    CheckTokenVariableAccess('a'),
                    CheckTokenLiteral('10', TFull(BaseTypes.int64))
                ),
                CheckControlCodeBlock([
                    CheckControlWhile(
                        CheckTokenOperatorBinary(
                            TokenOperatorBinaryTypes.ComprLess,
                            CheckTokenVariableAccess('b'),
                            CheckTokenLiteral('5', TFull(BaseTypes.int64))
                        ),
                        CheckControlCodeBlock([
                            CheckControlCycleControl(CycleControlTypes.break_)
                        ])
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenVariableAccess('a'),
                            CheckTokenOperatorBinary(
                                TokenOperatorBinaryTypes.ArfmAdd,
                                CheckTokenVariableAccess('a'),
                                CheckTokenLiteral('1', TFull(BaseTypes.int64))
                            )
                        )
                    )
                ])
            )
        ]),
        True
    ),
    # Индексация массива (чтение)
    (
        """
        def main() -> () {
            a = arr[5];
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('a'),
                    CheckTokenOperatorIndex(
                        CheckTokenVariableAccess('arr'),
                        CheckTokenLiteral('5', TFull(BaseTypes.int64))
                    )
                )
            )
        ]),
        True
    ),
    # Взятие адреса & (постфикс)
    (
        """
        def main() -> () {
            ptr = x&;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('ptr'),
                    CheckTokenOperatorReferencing(
                        CheckTokenVariableAccess('x')
                    )
                )
            )
        ]),
        True
    ),
    # Разыменование * (постфикс)
    (
        """
        def main() -> () {
            val = ptr*;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('val'),
                    CheckTokenOperatorDereferencing(
                        CheckTokenVariableAccess('ptr')
                    )
                )
            )
        ]),
        True
    ),
    # sizeof тип
    (
        """
        def main() -> () {
            s = sizeof int64;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('s'),
                    CheckTokenOperatorSizeof(T('int64'))
                )
            )
        ]),
        True
    ),
    # lenof массива/среза
    (
        """
        def main() -> () {
            l = lenof arr;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('l'),
                    CheckTokenOperatorLenof(
                        CheckTokenVariableAccess('arr')
                    )
                )
            )
        ]),
        True
    ),
    # Создание массива на месте [a, b, c]
    (
        """
        def main() -> () {
            arr = [1, 2, 3];
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('arr'),
                    CheckTokenOperatorArrayCreation([
                        CheckTokenLiteral('1', TFull(BaseTypes.int64)),
                        CheckTokenLiteral('2', TFull(BaseTypes.int64)),
                        CheckTokenLiteral('3', TFull(BaseTypes.int64))
                    ])
                )
            )
        ]),
        True
    ),
    # Срез: arr[5:10:2] (начало, количество, размерности)
    (
        """
        def main() -> () {
            s = arr[5:2];
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('s'),
                    CheckTokenOperatorSlize(
                        CheckTokenVariableAccess('arr'),
                        position_start=[CheckTokenLiteral('5', TFull(BaseTypes.int64))],
                        result_dimensions=[CheckTokenLiteral('2', TFull(BaseTypes.int64))]
                    )
                )
            )
        ]),
        True
    ),
    # тип среза
    (
        """
        def main() -> () {
            var x (int8[,]);
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'x',
                    T('int8', [Type.ModifierSlise(2)])
                )
            )
        ]),
        True
    ),
    # Объявление переменной-указателя
    (
        """
        def main() -> () {
            var ptr (int64*);
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'ptr',
                    T('int64', [Type.ModifierPointer()])
                )
            )
        ]),
        True
    ),
    # Приведение с указателем
    (
        """
        def main() -> () {
            ptr2 = ptr1 as (bool*);
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('ptr2'),
                    CheckTokenOperatorCast(
                        T('bool', [Type.ModifierPointer()]),
                        CheckTokenVariableAccess(

                            'ptr1'
                        ),
                    )
                )
            )
        ]),
        True
    ),
    # Сочетание индексации и взятия адреса
    (
        """
        def main() -> () {
            ptr = arr[2]*;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('ptr'),
                    CheckTokenOperatorDereferencing(
                        CheckTokenOperatorIndex(
                            CheckTokenVariableAccess('arr'),
                            CheckTokenLiteral('2', TFull(BaseTypes.int64))
                        )
                    )
                )
            )
        ]),
        True
    ),
    # Множественное индексирование
    (
        """
        def main() -> () {
            arr[2,3,4];
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorIndex(
                    CheckTokenOperatorIndex(
                        CheckTokenOperatorIndex(
                            CheckTokenVariableAccess('arr'),
                            CheckTokenLiteral('2', TFull(BaseTypes.int64))
                        ),
                        CheckTokenLiteral('3', TFull(BaseTypes.int64))
                    ),
                    CheckTokenLiteral('4', TFull(BaseTypes.int64))
                )
            )
        ]),
        True
    ),
    # Многомерный массив
    (
        """
        def main() -> () {
            arr = [[1,2,3],[4,5,6]];
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess('arr'),
                    CheckTokenOperatorArrayCreation(
                        [
                            CheckTokenOperatorArrayCreation([
                                CheckTokenLiteral('1', TFull(BaseTypes.int64)),
                                CheckTokenLiteral('2', TFull(BaseTypes.int64)),
                                CheckTokenLiteral('3', TFull(BaseTypes.int64)),
                            ]),
                            CheckTokenOperatorArrayCreation([
                                CheckTokenLiteral('4', TFull(BaseTypes.int64)),
                                CheckTokenLiteral('5', TFull(BaseTypes.int64)),
                                CheckTokenLiteral('6', TFull(BaseTypes.int64)),
                            ])
                        ]
                    )
                )
            )
        ]),
        True
    ),
    # тип-функция
    (
        """
        def main() -> () {
            var sinp func (float64) -> (float64) = sin;
        }
        """,
        CheckControlCodeBlock([
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'sinp',
                        TTrue(Type(
                            Type.SimpleTypeFunc(
                                [Type(Type.SimpleTypeRaw('float64'), [])],
                                [Type(Type.SimpleTypeRaw('float64'), [])]
                            ), []
                        ))
                    ),
                    CheckTokenVariableAccess(
                        'sin'
                    )
                )
            )
        ]),
        True
    ),
    # typedef
    (
        """
        def main() -> () {
            alias vec (float64[]);
        }
        """,
        CheckControlCodeBlock([
            CheckControlTypedef(
                'vec', T('float64', [Type.ModifierSlise(1)])
            )
        ]),
        True
    ),
    # импорт и экспорт с псевдонимами и без
    (
        """
        from std/math import sin, cos as cos_;
        
        export sin as sin_, cos_;
        """,
        CheckControlCodeBlock([
            CheckControlImport(
                'std/math', False, [
                    ('sin', 'sin'),
                    ('cos', 'cos_'),
                ]
            ),
            CheckControlExport(
                False, [
                    ('sin', 'sin_'),
                    ('cos_', 'cos_'),
                ]
            )
        ]),
        False
    ),
    # импорт и экспорт со всем
    (
        """
        from std/io import all;
        from ./Defines import all;
        
        export all;
        """,
        CheckControlCodeBlock([
            CheckControlImport(
                'std/io', True, []
            ),
            CheckControlImport(
                './Defines', True, []
            ),
            CheckControlExport(
                True, []
            )
        ]),
        False
    ),
    # пустой класс
    (
        """
        class empty {
            {}
        }
        """,
        CheckControlCodeBlock([
            CheckControlClass(
                'empty', [],
                CheckControlCodeBlock([
                ])
            )
        ]),
        False
    ),
    # класс с полями экземпляра
    (
        """
        class fields_only {
            {
                a int64;
                b (int8*);
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlClass(
                'fields_only', [
                    CheckTokenOperatorVariableDefinition('a', T('int64', [])),
                    CheckTokenOperatorVariableDefinition('b', T('int8', [Type.ModifierPointer()])),
                ],
                CheckControlCodeBlock([
                ])
            )
        ]),
        False
    ),
    # класс с полями класса
    (
        """
        class class_vars {
            {}
            var class_var int64;
            def method() {
                return 1;
            }
        }
        """,
        CheckControlCodeBlock([
            CheckControlClass(
                'class_vars', [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorVariableDefinition(
                            'class_var', T('int64')
                        )
                    ),
                    CheckControlFunctionDefinition(
                        'method', [], [],
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenLiteral('1', TFull(BaseTypes.int64)),
                            ])
                        ])
                    )
                ])
            )
        ]),
        False
    ),
])
def test_1(code, expected_main_block, shorten_main):
    """Проверяет, что process_raw преобразует код в ожидаемый AST."""
    raw_block = tokenize_and_process_raw(code)
    # это для писания меньше, если есть только код в main
    if shorten_main:
        # также, что raw_block содержит только функцию main
        assert len(raw_block.block_parts) == 1
        func = raw_block.block_parts[0]
        assert isinstance(func, ControlFunctionDefinition)
        assert func.name == 'main'
        actual = func.code_block
    else:
        actual = raw_block
    expected_main_block.is_match(actual)
