import pytest
from .Simple import *
from ...Main.CollapseRaw.CollapseRaw import collapse_nest
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError


@pytest.mark.parametrize('s, expected', [
    (
        '''
        def main() -> (int32) 
        {
            foo = 2.0 - 1.999;
            bar = foo*foo*foo;
            return bar;
        }
        ''',
        CheckControlRawCodeBlock(
            [
                CheckControlRawFunctionDefinition(
                    'main',
                    [],
                    [[CTR(T_WRD, 'int32')]],
                    CheckControlRawCodeBlock(
                        [
                            CheckControlRawExpression(
                                [
                                    CTR(T_WRD, 'foo'),
                                    CTR(T_SYM, '='),
                                    CTR(T_LIT, '2.0'),
                                    CTR(T_SYM, '-'),
                                    CTR(T_LIT, '1.999'),
                                ]
                            ),
                            CheckControlRawExpression(
                                [
                                    CTR(T_WRD, 'bar'),
                                    CTR(T_SYM, '='),
                                    CTR(T_WRD, 'foo'),
                                    CTR(T_SYM, '*'),
                                    CTR(T_WRD, 'foo'),
                                    CTR(T_SYM, '*'),
                                    CTR(T_WRD, 'foo'),
                                ]
                            ),
                            CheckControlRawReturn(
                                [
                                    [CTR(T_WRD, 'bar')]
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    ),
    (
        '''
        def cosss(float32 x) -> (float32) 
        {
            float32 x2, float32 x4 = x*x, x*x*x*x;
            return 1 - x2 / 2 + x4 / 24; 
        }
        ''',
        CheckControlRawCodeBlock(
            [
                CheckControlRawFunctionDefinition(
                    'cosss',
                    [[CTR(T_WRD, 'float32'), CTR(T_WRD, 'x')]],
                    [[CTR(T_WRD, 'float32')]],
                    CheckControlRawCodeBlock(
                        [
                            CheckControlRawMassAssignment(
                                [
                                    [CTR(T_WRD, 'float32'), CTR(T_WRD, 'x2')],
                                    [CTR(T_WRD, 'float32'), CTR(T_WRD, 'x4')]
                                ],
                                [
                                    [CTR(T_WRD, 'x'), CTR(T_SYM, '*'), CTR(T_WRD, 'x')],
                                    [CTR(T_WRD, 'x'), CTR(T_SYM, '*'), CTR(T_WRD, 'x'), CTR(T_SYM, '*'),
                                     CTR(T_WRD, 'x'), CTR(T_SYM, '*'), CTR(T_WRD, 'x')],
                                ]
                            ),
                            CheckControlRawReturn(
                                [
                                    [
                                        CTR(T_LIT, '1'),
                                        CTR(T_SYM, '-'),
                                        CTR(T_WRD, 'x2'),
                                        CTR(T_SYM, '/'),
                                        CTR(T_LIT, '2'),
                                        CTR(T_SYM, '+'),
                                        CTR(T_WRD, 'x4'),
                                        CTR(T_SYM, '/'),
                                        CTR(T_LIT, '24'),
                                    ]
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    ),
    (
        '''
        def main()
        {
            def m1() {}
            def m3()->(int8) { return 16; }
            m3();
        }
        ''',
        CheckControlRawCodeBlock(
            [
                CheckControlRawFunctionDefinition(
                    'main',
                    [],
                    [],
                    CheckControlRawCodeBlock(
                        [
                            CheckControlRawFunctionDefinition(
                                'm1', [], [], CheckControlRawCodeBlock([])
                            ),
                            CheckControlRawFunctionDefinition(
                                'm3',
                                [],
                                [[CTR(T_WRD, 'int8')]],
                                CheckControlRawCodeBlock(
                                    [
                                        CheckControlRawReturn(
                                            [
                                                [CTR(T_LIT, '16')]
                                            ]
                                        )
                                    ]
                                )
                            ),
                            CheckControlRawExpression(
                                [
                                    CTR(T_WRD, 'm3'),
                                    CTR(T_SYM, '('),
                                    CTR(T_SYM, ')'),
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    ),
    (
        '''
        def countdown() -> (int32)
        {
            var int32 i = 10;
            while i > 0
            {
                i = i - 1;
            }
            return i;
        }
        ''',
        CheckControlRawCodeBlock(
            [
                CheckControlRawFunctionDefinition(
                    'countdown',
                    [],
                    [[CTR(T_WRD, 'int32')]],
                    CheckControlRawCodeBlock(
                        [
                            CheckControlRawExpression(
                                [
                                    CTR(T_SYM, 'var'),
                                    CTR(T_WRD, 'int32'),
                                    CTR(T_WRD, 'i'),
                                    CTR(T_SYM, '='),
                                    CTR(T_LIT, '10'),
                                ]
                            ),
                            CheckControlRawWhile(
                                condition=[
                                    CTR(T_WRD, 'i'),
                                    CTR(T_SYM, '>'),
                                    CTR(T_LIT, '0'),
                                ],
                                code_block=CheckControlRawCodeBlock(
                                    [
                                        CheckControlRawExpression(
                                            [
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '='),
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '-'),
                                                CTR(T_LIT, '1'),
                                            ]
                                        )
                                    ]
                                )
                            ),
                            CheckControlRawReturn(
                                [
                                    [CTR(T_WRD, 'i')]
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    ),
    (
        '''
        def test_break_continue()
        {
            var int32 i = 0;
            while i < 10
            {
                if i == 5
                {
                    break;
                }
                if i % 2 == 0
                {
                    i = i + 1;
                    continue;
                } else {
                    1 + 1;
                }
                i = i + 1;
            }
        }
        ''',
        CheckControlRawCodeBlock(
            [
                CheckControlRawFunctionDefinition(
                    'test_break_continue',
                    [],
                    [],
                    CheckControlRawCodeBlock(
                        [
                            CheckControlRawExpression(
                                [
                                    CTR(T_SYM, 'var'),
                                    CTR(T_WRD, 'int32'),
                                    CTR(T_WRD, 'i'),
                                    CTR(T_SYM, '='),
                                    CTR(T_LIT, '0'),
                                ]
                            ),
                            CheckControlRawWhile(
                                [
                                    CTR(T_WRD, 'i'),
                                    CTR(T_SYM, '<'),
                                    CTR(T_LIT, '10'),
                                ],
                                CheckControlRawCodeBlock(
                                    [
                                        CheckControlRawIf(
                                            ConditionalPartTypes.start,
                                            [
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '=='),
                                                CTR(T_LIT, '5'),
                                            ],
                                            CheckControlRawCodeBlock([
                                                CheckControlRawCycleControl(CycleControlTypes.break_)
                                            ]),
                                            CheckControlRawCodeBlock([])
                                        ),
                                        CheckControlRawIf(
                                            ConditionalPartTypes.start,
                                            [
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '%'),
                                                CTR(T_LIT, '2'),
                                                CTR(T_SYM, '=='),
                                                CTR(T_LIT, '0'),
                                            ],
                                            CheckControlRawCodeBlock([
                                                CheckControlRawExpression(
                                                    [
                                                        CTR(T_WRD, 'i'),
                                                        CTR(T_SYM, '='),
                                                        CTR(T_WRD, 'i'),
                                                        CTR(T_SYM, '+'),
                                                        CTR(T_LIT, '1'),
                                                    ]
                                                ),
                                                CheckControlRawCycleControl(CycleControlTypes.continue_)
                                            ]),
                                            CheckControlRawCodeBlock([
                                                CheckControlRawExpression(
                                                    [
                                                        CTR(T_LIT, '1'),
                                                        CTR(T_SYM, '+'),
                                                        CTR(T_LIT, '1'),
                                                    ]
                                                )
                                            ])
                                        ),
                                        CheckControlRawExpression(
                                            [
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '='),
                                                CTR(T_WRD, 'i'),
                                                CTR(T_SYM, '+'),
                                                CTR(T_LIT, '1'),
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )
    )
])
def test_1(s, expected):
    expected.is_match(collapse_nest(tokenize(s)))


@pytest.mark.parametrize('s', [
    'blob sfg asd; asd',
    'sdgsgd {',
    'def main() { {} }}',
    'def main() { {a; b} }}',
    'def main() { {a b} }}',
])
def test_2(s):
    with pytest.raises(OurSyntaxError):
        collapse_nest(tokenize(s))

