import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Function import is_function, collapse_function


@pytest.mark.parametrize('s, expected', [
    ('def foo()', True),
    ('a = 5', False),
    ('return a, b + c', False),
    ('a = b + c = d', False),
    ('def x(int32 a)', True),
    ('def asdasdasd(int32 a) -> (bool)', True),
])
def test_1(s, expected):
    assert is_function(tokenize(s)) == expected


dummy_block = ControlRawCodeBlock([], zero_origin)
dummy_check_block = CheckControlRawCodeBlock([])

@pytest.mark.parametrize('s, expected', [
    (
        'def foo() -> ()',
        CheckControlRawFunctionDefinition(
            'foo',
            [],
            [],
            dummy_check_block
        )
    ),
    (
        'def boo(int32 x, float32 f)',
        CheckControlRawFunctionDefinition(
            'boo',
            [
                [
                    CTR(T_WRD, 'int32'),
                    CTR(T_WRD, 'x'),
                ],
                [
                    CTR(T_WRD, 'float32'),
                    CTR(T_WRD, 'f'),
                ],
            ],
            [],
            dummy_check_block
        )
    ),
    (
        'def xd(bool _is) -> (int16)',
        CheckControlRawFunctionDefinition(
            'xd',
            [
                [
                    CTR(T_WRD, 'bool'),
                    CTR(T_WRD, '_is'),
                ]
            ],
            [
                [CTR(T_WRD, 'int16')],
            ],
            dummy_check_block
        )
    ),
    (
        'def foo() -> (int16, int32, int64)',
        CheckControlRawFunctionDefinition(
            'foo',
            [],
            [
                [CTR(T_WRD, 'int16')],
                [CTR(T_WRD, 'int32')],
                [CTR(T_WRD, 'int64')],
            ],
            dummy_check_block
        )
    )
])
def test_2(s, expected):
    err, res = [], []
    collapse_function(tokenize(s), dummy_block, err, res)
    assert not err
    assert len(res) == 1
    expected.is_match(res[0])


@pytest.mark.parametrize('s', [
    'def',
    'def ()',
    'def foo(',
    'def foo)',
    'def foo(,)',
    'def foo()->)',
    'def foo()->(',
])
def test_3(s):
    err, res = [], []
    collapse_function(tokenize(s), dummy_block, err, res)
    assert err
