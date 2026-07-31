import pytest
from .Simple import *
from ...Definitions.Enums import *
from ...Definitions.Tokens import Type
from ...Definitions import TypesShortener as types


def TTrue(t: Type) -> CheckType:
    return CheckTypeSimple(t)


CLS1 = ClassDescriptorManager()
def CLS1_obj(id_: int) -> CheckType: return CheckTypeClassInstance(CLS1.elem(id_))
def CLS1_obj_p(id_: int) -> CheckType: return CheckTypeClassInstance(CLS1.elem(id_), [Type.ModifierPointer()])
def CLS1_obj_array(id_: int, length: int) -> CheckType:
    return CheckTypeClassInstance(CLS1.elem(id_), [Type.ModifierArray(length)])
def CLS1_obj_slice(id_: int, dims: int) -> CheckType:
    return CheckTypeClassInstance(CLS1.elem(id_), [Type.ModifierSlise(dims)])
def CLS1_itself(id_: int) -> CheckType: return CheckTypeClassItself(CLS1.elem(id_))



@pytest.mark.parametrize('s, expected_block, expected_scope', [
    # 1. Простая функция с объявлением и присваиванием
    pytest.param(
            '''
            def main() -> (int32) 
            {
                var a int8 = 12;
                return 0;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int32)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition(
                                            'a', TTrue(types.int8)
                                        ),
                                        CheckTokenOperatorCast(
                                            TTrue(types.int8),
                                            CheckTokenLiteral(
                                                '12',
                                                TTrue(types.int64)
                                            )
                                        ),
                                        TTrue(types.int8)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorCast(
                                            TTrue(types.int32),
                                            CheckTokenLiteral(
                                                '0',
                                                TTrue(types.int64)
                                            )
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a'},
                    )
                ]
            ),
            id='1'
    ),
    # 2. Функция с параметрами и возвратом нескольких значений
    pytest.param(
            '''
            def main(x int32, y int32) -> (int32, int32)
            {
                var sum int32 = x + y;
                var diff int32 = x - y;
                return sum, diff;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [
                            CheckTokenOperatorVariableDefinition('x', TTrue(types.int32)),
                            CheckTokenOperatorVariableDefinition('y', TTrue(types.int32))
                        ],
                        [TTrue(types.int32), TTrue(types.int32)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('sum', TTrue(types.int32)),
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmAdd,
                                            CheckTokenVariableAccess('x', TTrue(types.int32)),
                                            CheckTokenVariableAccess('y', TTrue(types.int32)),
                                            TTrue(types.int32)
                                        ),
                                        TTrue(types.int32)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('diff', TTrue(types.int32)),
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmSub,
                                            CheckTokenVariableAccess('x', TTrue(types.int32)),
                                            CheckTokenVariableAccess('y', TTrue(types.int32)),
                                            TTrue(types.int32)
                                        ),
                                        TTrue(types.int32)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenVariableAccess('sum', TTrue(types.int32)),
                                        CheckTokenVariableAccess('diff', TTrue(types.int32))
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'x', 'y', 'sum', 'diff'},
                    )
                ]
            ),
            id='2'
    ),
    # 3. Массовое присваивание
    pytest.param(
            '''
            def main() -> ()
            {
                var a int32; var b int32; var c int32;
                a, b = 10, 20;
                c = a + b;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int32))
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorVariableDefinition('b', TTrue(types.int32))
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorVariableDefinition('c', TTrue(types.int32))
                                ),
                                CheckControlMassAssignment(
                                    [
                                        CheckTokenVariableAccess('a', TTrue(types.int32)),
                                        CheckTokenVariableAccess('b', TTrue(types.int32))
                                    ],
                                    [
                                        CheckTokenLiteral('10', TTrue(types.int64)),
                                        CheckTokenLiteral('20', TTrue(types.int64))
                                    ],
                                    [
                                        CheckControlMassAssignmentInner(
                                            CheckTokenLiteral('10', TTrue(types.int64)),
                                            [CheckTokenVariableAccess('a', TTrue(types.int32))],
                                            [TTrue(types.int32)]
                                        ),
                                        CheckControlMassAssignmentInner(
                                            CheckTokenLiteral('20', TTrue(types.int64)),
                                            [CheckTokenVariableAccess('b', TTrue(types.int32))],
                                            [TTrue(types.int32)]
                                        )
                                    ]
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenVariableAccess('c', TTrue(types.int32)),
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmAdd,
                                            CheckTokenVariableAccess('a', TTrue(types.int32)),
                                            CheckTokenVariableAccess('b', TTrue(types.int32)),
                                            TTrue(types.int32)
                                        ),
                                        TTrue(types.int32)
                                    )
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a', 'b', 'c'},
                    )
                ]
            ),
            id='3'
    ),
    # 4. Вызов функции из другой функции
    pytest.param(
            '''
            def inc(a int32) -> (int32)
            {
                return a + 1;
            }
            def main() -> (int32)
            {
                return inc(5);
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'inc',
                        [CheckTokenOperatorVariableDefinition('a', TTrue(types.int32))],
                        [TTrue(types.int32)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorCast(
                                            TTrue(types.int32),
                                            CheckTokenOperatorBinary(
                                                TokenOperatorBinaryTypes.ArfmAdd,
                                                CheckTokenOperatorCast(
                                                    TTrue(types.int64),
                                                    CheckTokenVariableAccess(
                                                        'a', TTrue(types.int32)
                                                    ),
                                                ),
                                                CheckTokenLiteral('1', TTrue(types.int64)),
                                                TTrue(types.int64)
                                            )
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int32)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorFunctionCall(
                                            CheckTokenVariableAccess('inc',
                                                                     TTrue(types.func([types.int32], [types.int32]))),
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.int32),
                                                    CheckTokenLiteral('5', TTrue(types.int64))
                                                )
                                            ],
                                            TTrue(types.int32)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                set(),
                functions={'inc', 'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a'},
                    ),
                    CheckScope(
                        Scope.Types.Function,
                    )
                ]
            ),
            id='4'
    ),
    # 5. Приведение типа
    pytest.param(
            '''
            def main() -> (float64)
            {
                var a int32 = 10;
                var b float64 = a as float64;
                return b / 2;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.float64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('a', TTrue(types.int32)),
                                        CheckTokenOperatorCast(
                                            TTrue(types.int32),
                                            CheckTokenLiteral('10', TTrue(types.int64))
                                        ),
                                        TTrue(types.int32)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('b', TTrue(types.float64)),
                                        CheckTokenOperatorCast(
                                            TTrue(types.float64),
                                            CheckTokenVariableAccess('a', TTrue(types.int32))
                                        ),
                                        TTrue(types.float64)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmDiv,
                                            CheckTokenVariableAccess('b', TTrue(types.float64)),
                                            CheckTokenOperatorCast(
                                                TTrue(types.float64),
                                                CheckTokenLiteral('2', TTrue(types.int64))
                                            ),
                                            TTrue(types.float64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a', 'b'},
                    )
                ]
            ),
            id='5'
    ),
    # 6. Простой цикл while
    pytest.param(
            '''
            def main() -> (int64)
            {
                var i int64 = 0;
                var s int64 = 0;
                while i < 10 {
                    s = s + i;
                    i = i + 1;
                }
                return s;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('i', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('s', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlWhile(
                                    condition=CheckTokenOperatorBinary(
                                        TokenOperatorBinaryTypes.ComprLess,
                                        left=CheckTokenVariableAccess('i',
                                                                      TTrue(types.int64)),
                                        right=CheckTokenLiteral('10', TTrue(types.int64)),
                                        res_type=TTrue(types.bool)
                                    ),
                                    code_block=CheckControlCodeBlock(
                                        [
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    left=CheckTokenVariableAccess('s',
                                                                                  TTrue(types.int64)),
                                                    right=CheckTokenOperatorBinary(
                                                        TokenOperatorBinaryTypes.ArfmAdd,
                                                        left=CheckTokenVariableAccess(
                                                            's', TTrue(types.int64)),
                                                        right=CheckTokenVariableAccess(
                                                            'i', TTrue(types.int64)),
                                                        res_type=TTrue(types.int64)
                                                    ),
                                                    res_type=TTrue(types.int64)
                                                )
                                            ),
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    left=CheckTokenVariableAccess('i',
                                                                                  TTrue(types.int64)),
                                                    right=CheckTokenOperatorBinary(
                                                        TokenOperatorBinaryTypes.ArfmAdd,
                                                        left=CheckTokenVariableAccess(
                                                            'i', TTrue(types.int64)),
                                                        right=CheckTokenLiteral('1', TTrue(types.int64)),
                                                        res_type=TTrue(types.int64)
                                                    ),
                                                    res_type=TTrue(types.int64)
                                                )
                                            )
                                        ]
                                    )
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('s', TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'i', 's'},
                        children=[
                            CheckScope(  # область видимости цикла
                                Scope.Types.Cycle,
                            )
                        ]
                    )
                ]
            ),
            id='6'
    ),
    # 7. Цикл с break и continue
    pytest.param(
            '''
            def main() -> (int64)
            {
                var i int64 = 0;
                var res int64 = 0;
                while i < 5 {
                    i = i + 1;
                    if i == 3 {
                        continue;
                    }
                    if i == 4 {
                        break;
                    }
                    res = res + i;
                }
                return res;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('i', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('res', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlWhile(
                                    condition=CheckTokenOperatorBinary(
                                        TokenOperatorBinaryTypes.ComprLess,
                                        left=CheckTokenVariableAccess('i',
                                                                      TTrue(types.int64)),
                                        right=CheckTokenLiteral('5', TTrue(types.int64)),
                                        res_type=TTrue(types.bool)
                                    ),
                                    code_block=CheckControlCodeBlock(
                                        [
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    CheckTokenVariableAccess('i',
                                                                             TTrue(types.int64)),
                                                    CheckTokenOperatorBinary(
                                                        TokenOperatorBinaryTypes.ArfmAdd,
                                                        CheckTokenVariableAccess(
                                                            'i', TTrue(types.int64)),
                                                        CheckTokenLiteral('1', TTrue(types.int64)),
                                                        TTrue(types.int64)
                                                    ),
                                                    TTrue(types.int64)
                                                )
                                            ),
                                            CheckControlIf(
                                                CheckTokenOperatorBinary(
                                                    TokenOperatorBinaryTypes.ComprEq,
                                                    CheckTokenVariableAccess(
                                                        'i', TTrue(types.int64)),
                                                    CheckTokenLiteral('3', TTrue(types.int64)),
                                                    TTrue(types.bool)
                                                ),
                                                CheckControlCodeBlock([
                                                    CheckControlCycleControl(CycleControlTypes.continue_)
                                                ]),
                                                CheckControlCodeBlock([
                                                ])
                                            ),
                                            CheckControlIf(
                                                CheckTokenOperatorBinary(
                                                    TokenOperatorBinaryTypes.ComprEq,
                                                    CheckTokenVariableAccess(
                                                        'i', TTrue(types.int64)),
                                                    CheckTokenLiteral('4', TTrue(types.int64)),
                                                    TTrue(types.bool)
                                                ),
                                                CheckControlCodeBlock([
                                                    CheckControlCycleControl(CycleControlTypes.break_)
                                                ]),
                                                CheckControlCodeBlock([
                                                ])
                                            ),
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    CheckTokenVariableAccess(
                                                        'res', TTrue(types.int64)),
                                                    CheckTokenOperatorBinary(
                                                        TokenOperatorBinaryTypes.ArfmAdd,
                                                        CheckTokenVariableAccess(
                                                            'res', TTrue(types.int64)),
                                                        CheckTokenVariableAccess(
                                                            'i', TTrue(types.int64)),
                                                        TTrue(types.int64)
                                                    ),
                                                    TTrue(types.int64)
                                                )
                                            )
                                        ]
                                    )
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('res',
                                                              TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'i', 'res'},
                        children=[
                            CheckScope(  # цикл
                                Scope.Types.Cycle,
                                children=[
                                    # первый if
                                    CheckScope(
                                        Scope.Types.Conditional,
                                    ),
                                    CheckScope(
                                        Scope.Types.Conditional,
                                    ),
                                    # второй if
                                    CheckScope(
                                        Scope.Types.Conditional,
                                    ),
                                    CheckScope(
                                        Scope.Types.Conditional,
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            id='7'
    ),
    # 8. if-elif-else с bool условиями
    pytest.param(
            '''
            def main() -> (int64)
            {
                var x bool = true;
                var y int64 = 0;
                if x {
                    y = 10;
                } elif false {
                    y = 20;
                } else {
                    y = 30;
                }
                return y;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('x', TTrue(types.bool)),
                                        CheckTokenLiteral('true', TTrue(types.bool)),
                                        TTrue(types.bool)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('y', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlIf(
                                    CheckTokenVariableAccess('x', TTrue(types.bool)),
                                    CheckControlCodeBlock([
                                        CheckControlExpression(
                                            CheckTokenOperatorAssignment(
                                                CheckTokenVariableAccess(
                                                    'y', TTrue(types.int64)),
                                                CheckTokenLiteral('10', TTrue(types.int64)),
                                                TTrue(types.int64)
                                            )
                                        )
                                    ]),
                                    CheckControlCodeBlock([
                                        CheckControlIf(
                                            CheckTokenLiteral('false', TTrue(types.bool)),
                                            CheckControlCodeBlock([
                                                CheckControlExpression(
                                                    CheckTokenOperatorAssignment(
                                                        CheckTokenVariableAccess(
                                                            'y',
                                                            TTrue(types.int64)),
                                                        CheckTokenLiteral('20', TTrue(types.int64)),
                                                        TTrue(types.int64)
                                                    )
                                                )
                                            ]),
                                            CheckControlCodeBlock([
                                                CheckControlExpression(
                                                    CheckTokenOperatorAssignment(
                                                        left=CheckTokenVariableAccess(
                                                            'y', TTrue(types.int64)),
                                                        right=CheckTokenLiteral('30', TTrue(types.int64)),
                                                        res_type=TTrue(types.int64)
                                                    )
                                                )
                                            ]),
                                        )
                                    ])
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('y', TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'x', 'y'},
                        children=[
                            # if
                            CheckScope(
                                Scope.Types.Conditional,
                            ),
                            CheckScope(
                                Scope.Types.Conditional,
                                children=[
                                    CheckScope( # elif
                                        Scope.Types.Conditional,
                                    ),
                                    CheckScope(  # else
                                        Scope.Types.Conditional,
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            ),
            id='8'
    ),
    # 9. Вложенные циклы и вложенные if (проверка областей видимости)
    pytest.param(
            '''
            def main() -> (int64)
            {
                var a int64 = 0;
                var i int64 = 0;
                while i < 2 {
                    var j int64 = 0;
                    while j < 2 {
                        if j == 0 {
                            a = a + 1;
                        }
                        j = j + 1;
                    }
                    i = i + 1;
                }
                return a;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('a', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('i', TTrue(types.int64)),
                                        CheckTokenLiteral('0', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlWhile(
                                    condition=CheckTokenOperatorBinary(
                                        TokenOperatorBinaryTypes.ComprLess,
                                        left=CheckTokenVariableAccess('i',
                                                                      TTrue(types.int64)),
                                        right=CheckTokenLiteral('2', TTrue(types.int64)),
                                        res_type=TTrue(types.bool)
                                    ),
                                    code_block=CheckControlCodeBlock(
                                        [
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    CheckTokenOperatorVariableDefinition('j', TTrue(types.int64)),
                                                    CheckTokenLiteral('0', TTrue(types.int64)),
                                                    TTrue(types.int64)
                                                )
                                            ),
                                            CheckControlWhile(
                                                condition=CheckTokenOperatorBinary(
                                                    TokenOperatorBinaryTypes.ComprLess,
                                                    left=CheckTokenVariableAccess('j',
                                                                                  TTrue(types.int64)),
                                                    right=CheckTokenLiteral('2', TTrue(types.int64)),
                                                    res_type=TTrue(types.bool)
                                                ),
                                                code_block=CheckControlCodeBlock(
                                                    [
                                                        CheckControlIf(
                                                            CheckTokenOperatorBinary(
                                                                TokenOperatorBinaryTypes.ComprEq,
                                                                left=CheckTokenVariableAccess(
                                                                    'j',
                                                                    TTrue(types.int64)),
                                                                right=CheckTokenLiteral('0', TTrue(types.int64)),
                                                                res_type=TTrue(types.bool)
                                                            ),
                                                            CheckControlCodeBlock([
                                                                CheckControlExpression(
                                                                    CheckTokenOperatorAssignment(
                                                                        left=CheckTokenVariableAccess(

                                                                            'a', TTrue(types.int64)),
                                                                        right=CheckTokenOperatorBinary(
                                                                            TokenOperatorBinaryTypes.ArfmAdd,
                                                                            left=CheckTokenVariableAccess(

                                                                                'a', TTrue(types.int64)),
                                                                            right=CheckTokenLiteral('1',
                                                                                                    TTrue(
                                                                                                        types.int64)),
                                                                            res_type=TTrue(types.int64)
                                                                        ),
                                                                        res_type=TTrue(types.int64)
                                                                    )
                                                                )
                                                            ]),
                                                            CheckControlCodeBlock([
                                                            ])
                                                        ),
                                                        CheckControlExpression(
                                                            CheckTokenOperatorAssignment(
                                                                left=CheckTokenVariableAccess(
                                                                    'j',
                                                                    TTrue(types.int64)),
                                                                right=CheckTokenOperatorBinary(
                                                                    TokenOperatorBinaryTypes.ArfmAdd,
                                                                    left=CheckTokenVariableAccess(
                                                                        'j',
                                                                        TTrue(types.int64)),
                                                                    right=CheckTokenLiteral('1', TTrue(types.int64)),
                                                                    res_type=TTrue(types.int64)
                                                                ),
                                                                res_type=TTrue(types.int64)
                                                            )
                                                        )
                                                    ]
                                                )
                                            ),
                                            CheckControlExpression(
                                                CheckTokenOperatorAssignment(
                                                    left=CheckTokenVariableAccess('i',
                                                                                  TTrue(types.int64)),
                                                    right=CheckTokenOperatorBinary(
                                                        TokenOperatorBinaryTypes.ArfmAdd,
                                                        left=CheckTokenVariableAccess(
                                                            'i', TTrue(types.int64)),
                                                        right=CheckTokenLiteral('1', TTrue(types.int64)),
                                                        res_type=TTrue(types.int64)
                                                    ),
                                                    res_type=TTrue(types.int64)
                                                )
                                            )
                                        ]
                                    )
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('a', TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a', 'i'},
                        children=[
                            CheckScope(  # внешний цикл
                                Scope.Types.Cycle,
                                variables={'j'},
                                children=[
                                    CheckScope(  # внутренний цикл
                                        Scope.Types.Cycle,
                                        children=[
                                            CheckScope(  # if внутри
                                                Scope.Types.Conditional,
                                            ),
                                            CheckScope(
                                                Scope.Types.Conditional,
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            id='9'
    ),
    # 10. Создание массива на месте, присваивание и индексация
    pytest.param(
            '''
            def main() -> (int64)
            {
                var arr (int64[3]) = [1, 2, 3];
                return arr[0];
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('arr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(3)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [
                                                CheckTokenLiteral('1', TTrue(types.int64)),
                                                CheckTokenLiteral('2', TTrue(types.int64)),
                                                CheckTokenLiteral('3', TTrue(types.int64))
                                            ],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorIndex(
                                            CheckTokenVariableAccess('arr',
                                                                     TTrue(types.add_modifiers(types.int64,
                                                                                               [types.mod_array(3)]))),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('0', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'arr'},
                    )
                ]
            ),
            id='10'
    ),
    # 11. Индексация с записью в элемент массива
    pytest.param(
            '''
            def main() -> (int64)
            {
                var arr (int64[3]) = [10, 20, 30];
                arr[1] = 100;
                return arr[1];
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('arr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(3)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [
                                                CheckTokenLiteral('10', TTrue(types.int64)),
                                                CheckTokenLiteral('20', TTrue(types.int64)),
                                                CheckTokenLiteral('30', TTrue(types.int64))
                                            ],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorIndex(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(3)]))),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('1', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        ),
                                        CheckTokenLiteral('100', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorIndex(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(3)]))),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('1', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'arr'},
                    )
                ]
            ),
            id='11'
    ),
    # 12. Указатели: взятие адреса и разыменование
    pytest.param(
            '''
            def main() -> (int64)
            {
                var x int64 = 42;
                var ptr (int64*) = x&;
                var y int64 = ptr*;
                return y;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('x', TTrue(types.int64)),
                                        CheckTokenLiteral('42', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('ptr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_pointer()]))),
                                        CheckTokenOperatorReferencing(
                                            CheckTokenVariableAccess('x', TTrue(types.int64)),
                                            TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('y', TTrue(types.int64)),
                                        CheckTokenOperatorDereferencing(
                                            CheckTokenVariableAccess('ptr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_pointer()]))),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('y', TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'x', 'ptr', 'y'},
                    )
                ]
            ),
            id='12'
    ),
    # 13. Оператор среза на массиве
    pytest.param(
            '''
            def main() -> (int64)
            {
                var arr int64[10] = [0,1,2,3,4,5,6,7,8,9];
                var slice int64[] = arr[2:5];
                return slice[0];
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('arr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(10)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [CheckTokenLiteral(str(i), TTrue(types.int64)) for i in range(10)],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_array(10)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_array(10)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('slice', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_slice(1)]))),
                                        CheckTokenOperatorSlize(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(10)]))),
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('2', TTrue(types.int64))
                                                )
                                            ],
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('5', TTrue(types.int64))
                                                )
                                            ],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorIndex(
                                            CheckTokenVariableAccess('slice', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_slice(1)]))),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('0', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        {'arr', 'slice'},
                    )
                ]
            ),
            id='13'
    ),
    # 14. lenof для массива и среза
    pytest.param(
            '''
            def main() -> (int64)
            {
                var arr (int64[5]) = [1,2,3,4,5];
                var len_arr int64 = lenof arr;
                var slice (int64[]) = arr[0:3];
                var len_slice int64 = lenof slice;
                return len_arr + len_slice;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('arr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(5)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [CheckTokenLiteral(str(i), TTrue(types.int64)) for i in range(1, 6)],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_array(5)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_array(5)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('len_arr', TTrue(types.int64)),
                                        CheckTokenOperatorLenof(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(5)]))),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('slice', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_slice(1)]))),
                                        CheckTokenOperatorSlize(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(5)]))),
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('0', TTrue(types.int64))
                                                )
                                            ],
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('3', TTrue(types.int64))
                                                )
                                            ],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('len_slice', TTrue(types.int64)),
                                        CheckTokenOperatorLenof(
                                            CheckTokenVariableAccess('slice', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_slice(1)]))),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmAdd,
                                            CheckTokenVariableAccess('len_arr', TTrue(types.int64)),
                                            CheckTokenVariableAccess('len_slice', TTrue(types.int64)),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'arr', 'len_arr', 'slice', 'len_slice'},
                    )
                ]
            ),
            id='14'
    ),
    # 15. sizeof типа
    pytest.param(
            '''
            def main() -> (int64)
            {
                var s1 int64 = sizeof int32;
                var s2 int64 = sizeof (int64*);
                var s3 int64 = sizeof (float64[10]);
                return s1 + s2 + s3;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('s1', TTrue(types.int64)),
                                        CheckTokenOperatorSizeof(
                                            TTrue(types.int32),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('s2', TTrue(types.int64)),
                                        CheckTokenOperatorSizeof(
                                            TTrue(types.add_modifiers(types.int64, [types.mod_pointer()])),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('s3', TTrue(types.int64)),
                                        CheckTokenOperatorSizeof(
                                            TTrue(types.add_modifiers(types.float64, [types.mod_array(10)])),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmAdd,
                                            CheckTokenOperatorBinary(
                                                TokenOperatorBinaryTypes.ArfmAdd,
                                                CheckTokenVariableAccess('s1', TTrue(types.int64)),
                                                CheckTokenVariableAccess('s2', TTrue(types.int64)),
                                                TTrue(types.int64)
                                            ),
                                            CheckTokenVariableAccess('s3', TTrue(types.int64)),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'s1', 's2', 's3'},
                    )
                ]
            ),
            id='15'
    ),
    # 16. Массив указателей и доступ к элементу
    pytest.param(
            '''
            def main() -> (int64)
            {
                var a int64 = 10;
                var b int64 = 20;
                var ptrs (int64*[2]) = [a&, b&];
                var val int64 = ptrs[1]*;
                return val;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('a', TTrue(types.int64)),
                                        CheckTokenLiteral('10', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('b', TTrue(types.int64)),
                                        CheckTokenLiteral('20', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('ptrs', TTrue(
                                            types.add_modifiers(types.int64,
                                                                [types.mod_pointer(), types.mod_array(2)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [
                                                CheckTokenOperatorReferencing(
                                                    CheckTokenVariableAccess('a', TTrue(types.int64)),
                                                    TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                                ),
                                                CheckTokenOperatorReferencing(
                                                    CheckTokenVariableAccess('b', TTrue(types.int64)),
                                                    TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                                )
                                            ],
                                            TTrue(types.add_modifiers(types.int64,
                                                                      [types.mod_pointer(), types.mod_array(2)]))
                                        ),
                                        TTrue(
                                            types.add_modifiers(types.int64, [types.mod_pointer(), types.mod_array(2)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('val', TTrue(types.int64)),
                                        CheckTokenOperatorDereferencing(
                                            CheckTokenOperatorIndex(
                                                CheckTokenVariableAccess('ptrs', TTrue(types.add_modifiers(types.int64,
                                                                                                           [
                                                                                                               types.mod_pointer(),
                                                                                                               types.mod_array(
                                                                                                                   2)]))),
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('1', TTrue(types.int64))
                                                ),
                                                TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                            ),
                                            TTrue(types.int64)
                                        ),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlReturn(
                                    [CheckTokenVariableAccess('val', TTrue(types.int64))]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'a', 'b', 'ptrs', 'val'},
                    )
                ]
            ),
            id='16'
    ),
    # 17. Явное приведение указателей
    pytest.param(
            '''
            def main() -> (int8)
            {
                var x int64 = 42;
                var ptr (int64*) = x&;
                var byte_ptr (int8*) = ptr as (int8*);
                return byte_ptr*;
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int8)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('x', TTrue(types.int64)),
                                        CheckTokenLiteral('42', TTrue(types.int64)),
                                        TTrue(types.int64)
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('ptr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_pointer()]))),
                                        CheckTokenOperatorReferencing(
                                            CheckTokenVariableAccess('x', TTrue(types.int64)),
                                            TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_pointer()]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('byte_ptr', TTrue(
                                            types.add_modifiers(types.int8, [types.mod_pointer()]))),
                                        CheckTokenOperatorCast(
                                            TTrue(types.add_modifiers(types.int8, [types.mod_pointer()])),
                                            CheckTokenVariableAccess('ptr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_pointer()])))
                                        ),
                                        TTrue(types.add_modifiers(types.int8, [types.mod_pointer()]))
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorDereferencing(
                                            CheckTokenVariableAccess('byte_ptr', TTrue(
                                                types.add_modifiers(types.int8, [types.mod_pointer()]))),
                                            TTrue(types.int8)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'x', 'ptr', 'byte_ptr'},
                    )
                ]
            ),
            id='18'
    ),
    # 18. Неявный срез arr[:] – начало и размерности не указаны
    pytest.param(
            '''
            def main() -> (int64)
            {
                var arr (int64[10]) = [0,1,2,3,4,5,6,7,8,9];
                var slice (int64[]) = arr[:];
                return slice[5];
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('arr', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(10)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [CheckTokenLiteral(str(i), TTrue(types.int64)) for i in range(10)],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_array(10)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_array(10)]))
                                    )
                                ),
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('slice', TTrue(
                                            types.add_modifiers(types.int64, [types.mod_slice(1)]))),
                                        CheckTokenOperatorSlize(
                                            CheckTokenVariableAccess('arr', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_array(10)]))),
                                            [
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('0', TTrue(types.int64))
                                                )
                                            ],
                                            [
                                                CheckTokenOperatorLenof(
                                                    CheckTokenVariableAccess('arr', TTrue(
                                                        types.add_modifiers(types.int64, [types.mod_array(10)]))),
                                                    TTrue(types.int64)
                                                )
                                            ],
                                            TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                        ),
                                        TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorIndex(
                                            CheckTokenVariableAccess('slice',
                                                                     TTrue(types.add_modifiers(types.int64,
                                                                                               [types.mod_slice(1)]))),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('5', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'arr', 'slice'},
                    )
                ]
            ),
            id='19'
    ),
    # 19. Многомерный массив (2x3) и индексация
    pytest.param(
            '''
            def main() -> (int64)
            {
                var matrix (int64[3][2]) = [[1,2,3],[4,5,6]];
                return matrix[1][2];
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [TTrue(types.int64)],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition('matrix', TTrue(
                                            types.add_modifiers(types.int64,
                                                                [types.mod_array(3), types.mod_array(2)]))),
                                        CheckTokenOperatorArrayCreation(
                                            [
                                                CheckTokenOperatorArrayCreation(
                                                    [
                                                        CheckTokenLiteral('1', TTrue(types.int64)),
                                                        CheckTokenLiteral('2', TTrue(types.int64)),
                                                        CheckTokenLiteral('3', TTrue(types.int64))
                                                    ],
                                                    TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                                ),
                                                CheckTokenOperatorArrayCreation(
                                                    [
                                                        CheckTokenLiteral('4', TTrue(types.int64)),
                                                        CheckTokenLiteral('5', TTrue(types.int64)),
                                                        CheckTokenLiteral('6', TTrue(types.int64))
                                                    ],
                                                    TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                                )
                                            ],
                                            TTrue(types.add_modifiers(types.int64,
                                                                      [types.mod_array(3), types.mod_array(2)]))
                                        ),
                                        TTrue(
                                            types.add_modifiers(types.int64, [types.mod_array(3), types.mod_array(2)]))
                                    )
                                ),
                                CheckControlReturn(
                                    [
                                        CheckTokenOperatorIndex(
                                            CheckTokenOperatorIndex(
                                                CheckTokenVariableAccess('matrix', TTrue(
                                                    types.add_modifiers(types.int64,
                                                                        [types.mod_array(3), types.mod_array(2)]))),
                                                CheckTokenOperatorCast(
                                                    TTrue(types.uint64),
                                                    CheckTokenLiteral('1', TTrue(types.int64))
                                                ),
                                                TTrue(types.add_modifiers(types.int64, [types.mod_array(3)]))
                                            ),
                                            CheckTokenOperatorCast(
                                                TTrue(types.uint64),
                                                CheckTokenLiteral('2', TTrue(types.int64))
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'matrix'},
                    )
                ]
            ),
            id='20'
    ),
    # 20. псевдоним и переопределение
    pytest.param(
            '''
            alias vector (float64[]);
            alias matrix (float64[,]);
    
            def main() -> ()
            {
                var vec1 vector; 
                {
                    alias vec1 (int64[]);
                    var vector vec1;
                }
            }
            ''',
            CheckControlCodeBlock(
                [
                    CheckControlTypedef(
                        'vector',
                        TTrue(types.add_modifiers(types.float64, [types.mod_slice(1)]))
                    ),
                    CheckControlTypedef(
                        'matrix',
                        TTrue(types.add_modifiers(types.float64, [types.mod_slice(2)]))
                    ),
                    CheckControlFunctionDefinition(
                        'main',
                        [],
                        [],
                        None,
                        CheckControlCodeBlock(
                            [
                                CheckControlExpression(
                                    CheckTokenOperatorVariableDefinition('vec1', TTrue(
                                        types.add_modifiers(types.float64, [types.mod_slice(1)])))),
                                CheckControlCodeBlock(
                                    [
                                        CheckControlTypedef(
                                            'vec1',
                                            TTrue(types.add_modifiers(types.int64, [types.mod_slice(1)]))
                                        ),
                                        CheckControlExpression(
                                            CheckTokenOperatorVariableDefinition('vector', TTrue(
                                                types.add_modifiers(types.int64, [types.mod_slice(1)])))),
                                    ]
                                ),
                            ]
                        )
                    )
                ]
            ),
            CheckScope(
                Scope.Types.Global,
                functions={'main'},
                typedefs={'vector', 'matrix'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'vec1'},
                        children=[
                            CheckScope(
                                Scope.Types.Usual,
                                variables={'vector'},
                                typedefs={'vec1'}
                            )
                        ]
                    )
                ]
            ),
            id='21'
    ),
    # 21. класс и тип его элемента
    pytest.param(
        '''
        class MyClass {
            {}
        }
        
        var obj MyClass;
        ''',
        CheckControlCodeBlock([
            CLS1.assign(21, CheckControlClass(
                'MyClass', [],
                CheckControlCodeBlock([
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition('obj', CLS1_obj(21))
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'obj'},
            classes={'MyClass'},
            children=[
                CheckScope(
                    Scope.Types.Class
                )
            ]
        ),
        id='22'
    ),
    # 22. класс с полями экзепляра и обращениями к ним
    pytest.param(
        '''
        class MyClass {
            {
                a int64;
            }
        }
        
        def main() -> (int64) {
            var obj MyClass;
            obj.a = 10;
            return obj.a;
        }
        ''',
        CheckControlCodeBlock([
            CLS1.assign(22, CheckControlClass(
                'MyClass', [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64)),
                ],
                CheckControlCodeBlock([
                ])
            )),
            CheckControlFunctionDefinition(
                'main', [], [TTrue(types.int64)], [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorVariableDefinition('obj', CLS1_obj(22))
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess('obj', CLS1_obj(22)),
                                'a', TTrue(types.int64)
                            ),
                            CheckTokenLiteral('10', TTrue(types.int64)),
                            TTrue(types.int64)
                        )
                    ),
                    CheckControlReturn([
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('obj', CLS1_obj(22)),
                            'a', TTrue(types.int64)
                        )
                    ])
                ])
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            functions={'main'},
            classes={'MyClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                ),
                CheckScope(
                    Scope.Types.Function,
                    variables={'obj'}
                )
            ]
        ),
        id='23'
    ),
    # 23. класс с полями экзепляра и обращениями к ним через указатель
    pytest.param(
        '''
        class MyClass {
            {
                a int64;
            }
        }
        
        def main() -> (int64) {
            var obj_ MyClass;
            var obj (MyClass*) = obj_&;
            obj->a = 10;
            return obj->a;
        }
        ''',
        CheckControlCodeBlock([
            CLS1.assign(23, CheckControlClass(
                'MyClass', [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64)),
                ],
                CheckControlCodeBlock([
                ])
            )),
            CheckControlFunctionDefinition(
                'main', [], [TTrue(types.int64)], [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorVariableDefinition('obj_', CLS1_obj(23))
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorVariableDefinition('obj', CLS1_obj_p(23)),
                            CheckTokenOperatorReferencing(
                                CheckTokenVariableAccess('obj_', CLS1_obj(23)),
                                CLS1_obj_p(23)
                            ),
                            CLS1_obj_p(23)
                        )
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorFieldAccessPointer(
                                CheckTokenVariableAccess('obj', CLS1_obj_p(23)),
                                'a', TTrue(types.int64)
                            ),
                            CheckTokenLiteral('10', TTrue(types.int64)),
                            TTrue(types.int64)
                        )
                    ),
                    CheckControlReturn([
                        CheckTokenOperatorFieldAccessPointer(
                            CheckTokenVariableAccess('obj', CLS1_obj_p(23)),
                            'a', TTrue(types.int64)
                        )
                    ])
                ])
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            functions={'main'},
            classes={'MyClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                ),
                CheckScope(
                    Scope.Types.Function,
                    variables={'obj', 'obj_'}
                )
            ]
        ),
        id='23'
    ),
    # 24. теперь поля класса
    pytest.param(
        '''
        class MyClass {
            {}
            var a int64;
            def b() -> (int64) {
                return 1;
            }
        }
        
        var c int64 = MyClass.a = (MyClass.b)();
        ''',
        CheckControlCodeBlock([
            CLS1.assign(24, CheckControlClass(
                'MyClass', [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                    ),
                    CheckControlFunctionDefinition(
                        'b', [], [TTrue(types.int64)], [],
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenLiteral('1', TTrue(types.int64))
                            ])
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'c', TTrue(types.int64)
                    ),
                    CheckTokenOperatorAssignment(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess(
                                'MyClass', CLS1_itself(24)
                            ), 'a',
                            TTrue(types.int64)
                        ),
                        CheckTokenOperatorFunctionCall(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess(
                                    'MyClass', CLS1_itself(24)
                                ), 'b',
                                TTrue(types.func([], [types.int64]))
                            ), [],
                            TTrue(types.int64)
                        ),
                        TTrue(types.int64)
                    ),
                    TTrue(types.int64)
                )
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'c'},
            classes={'MyClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'b'},
                    variables={'a'},
                    children=[
                        CheckScope(
                            Scope.Types.Function
                        )
                    ]
                )
            ]
        ),
        id='24'
    ),
    # 25. вложенные типы из класса
    pytest.param(
        '''
        class MyClass {
            {}
            alias InnerAlias int64;
            
            class InnerClass {
                {}
            }
        }
        
        var i MyClass.InnerAlias;
        var obj (MyClass.InnerClass);
        ''',
        CheckControlCodeBlock([
            CheckControlClass(
                'MyClass', [],
                CheckControlCodeBlock([
                    CheckControlTypedef('InnerAlias', TTrue(types.int64)),
                    CLS1.assign(25, CheckControlClass(
                        'InnerClass', [],
                        CheckControlCodeBlock([
                        ])
                    ))
                ])
            ),
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'i', TTrue(types.int64)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'obj', CLS1_obj(25)
                )
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'i', 'obj'},
            classes={'MyClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    typedefs={'InnerAlias'},
                    classes={'InnerClass'},
                    children=[
                        CheckScope(
                            Scope.Types.Class
                        )
                    ]
                )
            ]
        ),
        id='25'
    ),
    # 26. __init__
    pytest.param(
        '''
        class MyClass2 {
            {
                f float64;
            }
            
            def __init__(self MyClass2, f float64) -> (MyClass2) {
                self.f = f;
                return self;
            }
        }
        
        var obj MyClass2 = MyClass2(1.0);
        ''',
        CheckControlCodeBlock([
            CLS1.assign(26, CheckControlClass(
                'MyClass2', [
                    CheckTokenOperatorVariableDefinition('f', TTrue(types.float64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        '__init__', [
                            CheckTokenOperatorVariableDefinition('f', TTrue(types.float64))
                        ], [
                            CLS1_obj(26)
                        ], [],
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(26)), 'f', TTrue(types.float64)
                                    ),
                                    CheckTokenVariableAccess('f', TTrue(types.float64)),
                                    TTrue(types.float64)
                                )
                            ),
                            CheckControlReturn([
                                CheckTokenVariableAccess('self', CLS1_obj(26))
                            ])
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'obj', CLS1_obj(26)
                    ),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('MyClass2', CLS1_itself(26)),
                            '__init__', CheckTypeFunc([TTrue(types.float64)], [CLS1_obj(26)])
                        ),
                        [
                            CheckTokenLiteral('1.0', TTrue(types.float64))
                        ],
                        CLS1_obj(26)
                    ),
                    CLS1_obj(26)
                )
            ),
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'obj'},
            classes={'MyClass2'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'f'}
                        )
                    ]
                )
            ]
        ),
        id='26'
    ),
    # 27. __add__ и его использование
    pytest.param(
        '''
        class addsup {
            {a int64;}
            def __init__(self addsup, a int64) -> (addsup) {
                self.a = a;
                return self;
            }
            
            def __add__(self addsup, other addsup) -> (addsup) {
                return addsup(self.a + other.a);
            }
        }
        
        var obj addsup = addsup(1) + addsup(2);
        ''',
        CheckControlCodeBlock([
            CLS1.assign(27, CheckControlClass(
                'addsup',
                [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        '__init__',
                        [
                            CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                        ],
                        [
                            CLS1_obj(27)
                        ], [],
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(27)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenVariableAccess('a', TTrue(types.int64)),
                                    TTrue(types.int64)
                                )
                            ),
                            CheckControlReturn([
                                CheckTokenVariableAccess('self', CLS1_obj(27))
                            ])
                        ])
                    ),
                    CheckControlFunctionDefinition(
                        '__add__',
                        [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(27)),
                            CheckTokenOperatorVariableDefinition('other', CLS1_obj(27))
                        ],
                        [
                            CLS1_obj(27)
                        ], [],
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenOperatorFunctionCall(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('addsup', CLS1_itself(27)),
                                        '__init__',
                                        CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(27)])
                                    ),
                                    [
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmAdd,
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('self', CLS1_obj(27)),
                                                'a',
                                                TTrue(types.int64)
                                            ),
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('other', CLS1_obj(27)),
                                                'a',
                                                TTrue(types.int64)
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ],
                                    CLS1_obj(27)
                                )
                            ])
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('obj', CLS1_obj(27)),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('addsup', CLS1_itself(27)), '__add__',
                            CheckTypeFunc([CLS1_obj(27), CLS1_obj(27)], [CLS1_obj(27)])
                        ),
                        [
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('addsup', CLS1_itself(27)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(27)])
                                ),
                                [
                                    CheckTokenLiteral('1', TTrue(types.int64))
                                ],
                                CLS1_obj(27)
                            ),
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('addsup', CLS1_itself(27)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(27)])
                                ),
                                [
                                    CheckTokenLiteral('2', TTrue(types.int64))
                                ],
                                CLS1_obj(27)
                            )
                        ],
                        CLS1_obj(27)
                    ),
                    CLS1_obj(27)
                )
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'obj'},
            classes={'addsup'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__', '__add__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'a'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'other'}
                        )
                    ]
                )
            ]
        ),
        id='27'
    ),
    # 28. __eq__ и его использование
    pytest.param(
        '''
        class EqClass {
            {a int64;}
            def __init__(self EqClass, a int64) -> (EqClass) {
                self.a = a;
                return self;
            }
            def __eq__(self EqClass, other EqClass) -> (bool) {
                return self.a == other.a;
            }
        }
    
        var b bool = EqClass(1) == EqClass(2);
        ''',
        CheckControlCodeBlock([
            CLS1.assign(28, CheckControlClass(
                'EqClass',
                [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        '__init__',
                        [
                            CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                        ],
                        [CLS1_obj(28)],
                        [],
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(28)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenVariableAccess('a', TTrue(types.int64)),
                                    TTrue(types.int64)
                                )
                            ),
                            CheckControlReturn([
                                CheckTokenVariableAccess('self', CLS1_obj(28))
                            ])
                        ])
                    ),
                    CheckControlFunctionDefinition(
                        '__eq__',
                        [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(28)),
                            CheckTokenOperatorVariableDefinition('other', CLS1_obj(28))
                        ],
                        [TTrue(types.bool)],
                        [],
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenOperatorBinary(
                                    TokenOperatorBinaryTypes.ComprEq,
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(28)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('other', CLS1_obj(28)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    TTrue(types.bool)
                                )
                            ])
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('b', TTrue(types.bool)),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('EqClass', CLS1_itself(28)),
                            '__eq__',
                            CheckTypeFunc([CLS1_obj(28), CLS1_obj(28)], [TTrue(types.bool)])
                        ),
                        [
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('EqClass', CLS1_itself(28)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(28)])
                                ),
                                [CheckTokenLiteral('1', TTrue(types.int64))],
                                CLS1_obj(28)
                            ),
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('EqClass', CLS1_itself(28)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(28)])
                                ),
                                [CheckTokenLiteral('2', TTrue(types.int64))],
                                CLS1_obj(28)
                            )
                        ],
                        TTrue(types.bool)
                    ),
                    TTrue(types.bool)
                )
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'b'},
            classes={'EqClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__', '__eq__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'a'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'other'}
                        )
                    ]
                )
            ]
        ),
        id='28'
    ),
    # 29. __bool__ и его использование (as bool) и явное преобразование в cls.__bool__(...)
    pytest.param(
        '''
        class BoolClass {
            {a int64;}
            def __init__(self BoolClass, a int64) -> (BoolClass) {
                self.a = a;
                return self;
            }
            def __bool__(self BoolClass) -> (bool) {
                return self.a != 0;
            }
        }
    
        var b bool = BoolClass(5) as bool;
        var b2 bool = BoolClass(10);
        ''',
        CheckControlCodeBlock([
            CLS1.assign(29, CheckControlClass(
                'BoolClass',
                [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        '__init__',
                        [
                            CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                        ],
                        [CLS1_obj(29)],
                        [],
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(29)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenVariableAccess('a', TTrue(types.int64)),
                                    TTrue(types.int64)
                                )
                            ),
                            CheckControlReturn([
                                CheckTokenVariableAccess('self', CLS1_obj(29))
                            ])
                        ])
                    ),
                    CheckControlFunctionDefinition(
                        '__bool__',
                        [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(29))
                        ],
                        [TTrue(types.bool)],
                        [],
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenOperatorBinary(
                                    TokenOperatorBinaryTypes.ComprNEq,
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(29)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenLiteral('0', TTrue(types.int64)),
                                    TTrue(types.bool)
                                )
                            ])
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('b', TTrue(types.bool)),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('BoolClass', CLS1_itself(29)),
                            '__bool__',
                            CheckTypeFunc([CLS1_obj(29)], [TTrue(types.bool)])
                        ),
                        [
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('BoolClass', CLS1_itself(29)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(29)])
                                ),
                                [CheckTokenLiteral('5', TTrue(types.int64))],
                                CLS1_obj(29)
                            )
                        ],
                        TTrue(types.bool)
                    ),
                    TTrue(types.bool)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('b2', TTrue(types.bool)),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess('BoolClass', CLS1_itself(29)),
                            '__bool__',
                            CheckTypeFunc([CLS1_obj(29)], [TTrue(types.bool)])
                        ),
                        [
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('BoolClass', CLS1_itself(29)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(29)])
                                ),
                                [CheckTokenLiteral('10', TTrue(types.int64))],
                                CLS1_obj(29)
                            )
                        ],
                        TTrue(types.bool)
                    ),
                    TTrue(types.bool)
                )
            ),
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'b', 'b2'},
            classes={'BoolClass'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__', '__bool__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self', 'a'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                )
            ]
        ),
        id='29'
    ),
    # 30. явная и не явная передача обычного экзепляра в метод
    pytest.param(
        '''
        class Check {
            {a int64;}
            def method(self Check) {}
        }
        
        var obj Check;
        (obj.method)();
        (Check.method)(obj);
        ''',
        CheckControlCodeBlock([
            CLS1.assign(30, CheckControlClass(
                'Check', [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        'method', [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(30))
                        ], [], [],
                        CheckControlCodeBlock([
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'obj', CLS1_obj(30)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Check', CLS1_itself(30)), 'method',
                        CheckTypeFunc([CLS1_obj(30)], [])
                    ),
                    [
                        CheckTokenVariableAccess('obj', CLS1_obj(30))
                    ], None
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Check', CLS1_itself(30)), 'method',
                        CheckTypeFunc([CLS1_obj(30)], [])
                    ),
                    [
                        CheckTokenVariableAccess('obj', CLS1_obj(30))
                    ], None
                )
            ),
        ]),
        CheckScope(
            Scope.Types.Global,
            classes={'Check'},
            variables={'obj'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'method', '__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                )
            ]
        ),
        id='30'
    ),
    # 31. передача в метод, что требует указателя, и использования __init__ без определения(пустой инит),
    # замена обращения к полю классе через экзепляр на прямой доступ
    pytest.param(
        '''
        class Check {
            {a int64;}
            def method(self (Check*)) {}
        }
            
        var obj Check = Check();
        var objp (Check*) = obj&;
        obj.method();
        (objp->method)();
        ''',
        CheckControlCodeBlock([
            CLS1.assign(31, CheckControlClass(
                'Check', [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        'method', [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj_p(31))
                        ], [], [],
                        CheckControlCodeBlock([
                        ])
                    )
                ])
            )),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'obj', CLS1_obj(31)
                    ),
                    CheckTokenOperatorFunctionCall(
                        CheckTokenOperatorFieldAccess(
                            CheckTokenVariableAccess(
                                'Check', CLS1_itself(31)
                            ), '__init__', CheckTypeFunc([], [CLS1_obj(31)])
                        ),
                        [], CLS1_obj(31)
                    ),
                    CLS1_obj(31)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'objp', CLS1_obj_p(31)
                    ),
                    CheckTokenOperatorReferencing(
                        CheckTokenVariableAccess(
                            'obj', CLS1_obj(31)
                        )
                    ),
                    CLS1_obj_p(31)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Check', CLS1_itself(31)), 'method',
                        CheckTypeFunc([CLS1_obj_p(31)], [])
                    ),
                    [
                        CheckTokenOperatorReferencing(
                            CheckTokenVariableAccess('obj', CLS1_obj(31)), CLS1_obj_p(31)
                        )
                    ], None
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Check', CLS1_itself(31)), 'method',
                        CheckTypeFunc([CLS1_obj_p(31)], [])
                    ),
                    [
                        CheckTokenVariableAccess('objp', CLS1_obj_p(31))
                    ], None
                )
            ),
        ]),
        CheckScope(
            Scope.Types.Global,
            classes={'Check'},
            variables={'obj', 'objp'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'method', '__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                )
            ]
        ),
        id='31'
    ),
    # 32. тест неявного удаления при выходе из блоков кода
    pytest.param(
        '''
        class impdel {
            {a int64;}
            def __del__(self impdel) {}
        }
        
        def f(obj impdel[42], obj2 impdel) -> (impdel) {
            var clean_ impdel = impdel();
            del clean_; 
            del obj2;
            var nonclean_ impdel = impdel();
            var clean_2 impdel = impdel();
            return clean_2;
        }
        ''',
        CheckControlCodeBlock([
            CLS1.assign(32, CheckControlClass(
                'impdel', [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ], CheckControlCodeBlock([
                    CheckControlFunctionDefinition(
                        '__del__', [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(32))
                        ], [], [],
                        CheckControlCodeBlock([])
                    )
                ])
            )),
            CheckControlFunctionDefinition(
                'f', [
                    CheckTokenOperatorVariableDefinition('obj', CLS1_obj_array(32, 42)),
                    CheckTokenOperatorVariableDefinition('obj2', CLS1_obj(32))
                ], [
                    CLS1_obj(32)
                ], [],
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorVariableDefinition(
                                'clean_', CLS1_obj(32)
                            ),
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess(
                                        'impdel', CLS1_itself(32)
                                    ), '__init__', CheckTypeFunc([], [CLS1_obj(32)])
                                ), [], CLS1_obj(32)
                            ), CLS1_obj(32)
                        )
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorFunctionCall(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess('impdel', CLS1_itself(32)),
                                '__del__', CheckTypeFunc([CLS1_obj(32)], [])
                            ),
                            [
                                CheckTokenVariableAccess('clean_', CLS1_obj(32)),
                            ], None
                        )
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorFunctionCall(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess('impdel', CLS1_itself(32)),
                                '__del__', CheckTypeFunc([CLS1_obj(32)], [])
                            ),
                            [
                                CheckTokenVariableAccess('obj2', CLS1_obj(32)),
                            ], None
                        )
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorVariableDefinition(
                                'nonclean_', CLS1_obj(32)
                            ),
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess(
                                        'impdel', CLS1_itself(32)
                                    ), '__init__', CheckTypeFunc([], [CLS1_obj(32)])
                                ), [], CLS1_obj(32)
                            ), CLS1_obj(32)
                        )
                    ),
                    CheckControlExpression(
                        CheckTokenOperatorAssignment(
                            CheckTokenOperatorVariableDefinition(
                                'clean_2', CLS1_obj(32)
                            ),
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess(
                                        'impdel', CLS1_itself(32)
                                    ), '__init__', CheckTypeFunc([], [CLS1_obj(32)])
                                ), [], CLS1_obj(32)
                            ), CLS1_obj(32)
                        )
                    ),
                    CheckControlReturn([
                        CheckTokenVariableAccess('clean_2', CLS1_obj(32))
                    ]),
                    # это должно появиться из-за удаления локальных переменных при выходе из блока кода
                    CheckControlExpression(
                        CheckTokenOperatorFunctionCall(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess('impdel', CLS1_itself(32)),
                                '__del__', CheckTypeFunc([CLS1_obj(32)], [])
                            ),
                            [
                                CheckTokenVariableAccess('nonclean_', CLS1_obj(32)),
                            ], None
                        )
                    ),
                ])
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            classes={'impdel'},
            functions={'f'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__del__', '__init__'},
                    children=[
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        ),
                        CheckScope(
                            Scope.Types.Function,
                            variables={'self'}
                        )
                    ]
                ),
                CheckScope(
                    Scope.Types.Function,
                    variables={'clean_', 'clean_2', 'obj', 'obj2', 'nonclean_'}
                )
            ]
        ),
        id='32'
    ),
    # 33. тест удаления временных не сохранённых объектов
    pytest.param(
        '''
        class tempdel {
            {a int64;}
            def __init__(self tempdel, a int64) -> (tempdel) {
                self.a = a;
                return self;
            }
            def __mul__(self tempdel, other tempdel) -> (tempdel) {
                return tempdel(self.a * other.a);
            }
            def __del__(self tempdel) {}
        }

        var obj (tempdel[2]) = [
            tempdel(1),
            tempdel(2) * tempdel(3)
        ];
        ''',
        CheckControlCodeBlock([
            # Определение класса tempdel
            CLS1.assign(33, CheckControlClass(
                'tempdel',
                [
                    CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                ],
                CheckControlCodeBlock([
                    # __init__
                    CheckControlFunctionDefinition(
                        '__init__',
                        [
                            CheckTokenOperatorVariableDefinition('a', TTrue(types.int64))
                        ],
                        [CLS1_obj(33)],
                        None,
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('self', CLS1_obj(33)),
                                        'a',
                                        TTrue(types.int64)
                                    ),
                                    CheckTokenVariableAccess('a', TTrue(types.int64)),
                                    TTrue(types.int64)
                                )
                            ),
                            CheckControlReturn([
                                CheckTokenVariableAccess('self', CLS1_obj(33))
                            ])
                        ])
                    ),
                    # __mul__
                    CheckControlFunctionDefinition(
                        '__mul__',
                        [
                            CheckTokenOperatorVariableDefinition('self', CLS1_obj(33)),
                            CheckTokenOperatorVariableDefinition('other', CLS1_obj(33))
                        ],
                        [CLS1_obj(33)],
                        None,
                        CheckControlCodeBlock([
                            CheckControlReturn([
                                CheckTokenOperatorFunctionCall(
                                    CheckTokenOperatorFieldAccess(
                                        CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                                        '__init__',
                                        CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(33)])
                                    ),
                                    [
                                        CheckTokenOperatorBinary(
                                            TokenOperatorBinaryTypes.ArfmMul,
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('self', CLS1_obj(33)),
                                                'a',
                                                TTrue(types.int64)
                                            ),
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('other', CLS1_obj(33)),
                                                'a',
                                                TTrue(types.int64)
                                            ),
                                            TTrue(types.int64)
                                        )
                                    ],
                                    CLS1_obj(33)
                                )
                            ])
                        ])
                    ),
                    # __del__
                    CheckControlFunctionDefinition(
                        '__del__',
                        [CheckTokenOperatorVariableDefinition('self', CLS1_obj(33))],
                        [],
                        None,
                        CheckControlCodeBlock([])
                    )
                ])
            )),
            # Присваивание obj = [ ... ]
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition('obj', CLS1_obj_array(33, 2)),
                    CheckTokenOperatorArrayCreation(
                        [
                            # Первый элемент: tempdel(1)
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                                    '__init__',
                                    CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(33)])
                                ),
                                [CheckTokenLiteral('1', TTrue(types.int64))],
                                CLS1_obj(33)
                            ),
                            # Второй элемент: (var1 = tempdel(2)) * (var2 = tempdel(3))
                            CheckTokenOperatorFunctionCall(
                                CheckTokenOperatorFieldAccess(
                                    CheckTokenVariableAccess(
                                        'tempdel', CLS1_itself(33)
                                    ), '__mul__', CheckTypeFunc([CLS1_obj(33), CLS1_obj(33)], [CLS1_obj(33)])
                                ),
                                [
                                    # var1 = tempdel(2)
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition(
                                            'expr_del_temp_var_1', CLS1_obj(33)
                                        ),
                                        CheckTokenOperatorFunctionCall(
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                                                '__init__', CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(33)])
                                            ),
                                            [
                                                CheckTokenLiteral('2', TTrue(types.int64))
                                            ], CLS1_obj(33)
                                        ), CLS1_obj(33)
                                    ),
                                    # var2 = tempdel(3)
                                    CheckTokenOperatorAssignment(
                                        CheckTokenOperatorVariableDefinition(
                                            'expr_del_temp_var_2', CLS1_obj(33)
                                        ),
                                        CheckTokenOperatorFunctionCall(
                                            CheckTokenOperatorFieldAccess(
                                                CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                                                '__init__', CheckTypeFunc([TTrue(types.int64)], [CLS1_obj(33)])
                                            ),
                                            [
                                                CheckTokenLiteral('3', TTrue(types.int64))
                                            ], CLS1_obj(33)
                                        ), CLS1_obj(33)
                                    ),
                                ], CLS1_obj(33)
                            )
                        ], CLS1_obj_array(33, 2)
                    ), CLS1_obj_array(33, 2)
                )
            ),
            # Деинициализаторы
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                        '__del__', CheckTypeFunc([CLS1_obj(33)], [])
                    ),
                    [
                        CheckTokenVariableAccess('expr_del_temp_var_2', CLS1_obj(33)),
                    ], None
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorFunctionCall(
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                        '__del__', CheckTypeFunc([CLS1_obj(33)], [])
                    ),
                    [
                        CheckTokenVariableAccess('expr_del_temp_var_1', CLS1_obj(33)),
                    ], None
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'expanded_deinitializer_slice_1', CLS1_obj_slice(33, 1)
                    ),
                    CheckTokenOperatorSlize(
                        CheckTokenVariableAccess('obj', CLS1_obj_array(33, 2)),
                        [
                            CheckTokenLiteral('0', TTrue(types.int64))
                        ], [
                            CheckTokenLiteral('2', TTrue(types.int64))
                        ], CLS1_obj_slice(33, 1)
                    ),
                    CLS1_obj_slice(33, 1)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenOperatorVariableDefinition(
                        'expanded_deinitializer_index_1', TTrue(types.int64)
                    ),
                    CheckTokenLiteral('0', TTrue(types.int64)),
                    TTrue(types.int64)
                )
            ),
            CheckControlWhile(
                CheckTokenOperatorBinary(
                    TokenOperatorBinaryTypes.ComprLessOrEq,
                    CheckTokenVariableAccess('expanded_deinitializer_index_1', TTrue(types.int64)),
                    CheckTokenOperatorLenof(
                        CheckTokenVariableAccess('expanded_deinitializer_slice_1', CLS1_obj_slice(33, 1)),
                        TTrue(types.int64)
                    ),
                    TTrue(types.bool)
                ),
                CheckControlCodeBlock([
                    CheckControlExpression(
                        CheckTokenOperatorFunctionCall(
                            CheckTokenOperatorFieldAccess(
                                CheckTokenVariableAccess('tempdel', CLS1_itself(33)),
                                '__del__', CheckTypeFunc([CLS1_obj(33)], [])
                            ),
                            [
                                CheckTokenOperatorIndex(
                                    CheckTokenVariableAccess('expanded_deinitializer_slice_1', CLS1_obj_slice(33, 1)),
                                    CheckTokenVariableAccess('expanded_deinitializer_index_1', TTrue(types.int64)),
                                    CLS1_obj(33)
                                )
                            ], None
                        )
                    ),
                ])
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'obj',
                       'expr_del_temp_var_1', 'expr_del_temp_var_2',
                       'expanded_deinitializer_index_1',
                       'expanded_deinitializer_slice_1'},
            classes={'tempdel'},
            children=[
                CheckScope(
                    Scope.Types.Class,
                    functions={'__init__', '__mul__', '__del__'},
                    children=[
                        CheckScope(Scope.Types.Function, variables={'self', 'a'}),
                        CheckScope(Scope.Types.Function, variables={'self', 'other'}),
                        CheckScope(Scope.Types.Function, variables={'self'}),
                    ]
                ),
                CheckScope(
                    Scope.Types.Cycle
                )
            ]
        ),
        id='33'
    ),
    # 34. перечисления, само, и его типы, и обращение к полю
    pytest.param(
        '''
        enum Errors {
            MemoryNotFound;
            FileNotFound;
            ZeroDivision;
            ValueError;
            AssertionError;
        }
        
        var err_state Errors;
        err_state = Errors.AssertionError;
        err_state == Errors.FileNotFound;
        ''',
        CheckControlCodeBlock([
            enum_34 := CheckControlEnum(
                'Errors', [
                    'MemoryNotFound',
                    'FileNotFound',
                    'ZeroDivision',
                    'ValueError',
                    'AssertionError',
                ]
            ),
            CheckControlExpression(
                CheckTokenOperatorVariableDefinition(
                    'err_state', CheckTypeEnumInstance(enum_34)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorAssignment(
                    CheckTokenVariableAccess(
                        'err_state', CheckTypeEnumInstance(enum_34)
                    ),
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Errors', CheckTypeEnum(enum_34)),
                        'AssertionError', CheckTypeEnumInstance(enum_34)
                    ),
                    CheckTypeEnumInstance(enum_34)
                )
            ),
            CheckControlExpression(
                CheckTokenOperatorBinary(
                    TokenOperatorBinaryTypes.ComprEq,
                    CheckTokenVariableAccess(
                        'err_state', CheckTypeEnumInstance(enum_34)
                    ),
                    CheckTokenOperatorFieldAccess(
                        CheckTokenVariableAccess('Errors', CheckTypeEnum(enum_34)),
                        'FileNotFound', CheckTypeEnumInstance(enum_34)
                    ),
                    TTrue(types.bool)
                )
            )
        ]),
        CheckScope(
            Scope.Types.Global,
            variables={'err_state'},
            enums={'Errors'}
        ),
        id='34'
    )
])
def test_1(s, expected_block, expected_scope):
    block, scope = parse_and_analyze(s)
    expected_block.is_match(block)
    expected_scope.is_match(scope)

