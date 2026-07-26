import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Return import is_return, collapse_return


@pytest.mark.parametrize('s, expected', [
    ('return', True),
    ('a = 5', False),
    ('return a, b + c', True),
    ('a = b + c = d', False),
    ('return (a, b), c', True),
])
def test_1(s, expected):
    assert is_return(tokenize(s)) == expected


@pytest.mark.parametrize('s, expected', [
    (
        'return ',
        CheckControlRawReturn([])
    ),
    (
        'return a',
        CheckControlRawReturn([
            [CTR(T_WRD, 'a')]
        ])
    ),
    (
        'return a, b + c',
        CheckControlRawReturn([
            [CTR(T_WRD, 'a')],
            [
                CTR(T_WRD, 'b'),
                CTR(T_SYM, '+'),
                CTR(T_WRD, 'c')
            ],
        ])
    ),
    (
        'return (a, b), c',
        CheckControlRawReturn([
            [
                CTR(T_SYM, '('),
                CTR(T_WRD, 'a'),
                CTR(T_SYM, ','),
                CTR(T_WRD, 'b'),
                CTR(T_SYM, ')')
            ],
            [CTR(T_WRD, 'c')],
        ])
    )
])
def test_2(s, expected):
    expected.is_match(collapse_return(tokenize(s)))


@pytest.mark.parametrize('s', [
    'return ,',
    'return a,',
    'return ,a',
    'return a,,b',
])
def test_3(s):
    with pytest.raises(OurSyntaxError):
        collapse_return(tokenize(s))
