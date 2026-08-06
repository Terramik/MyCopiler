import pytest
from .Simple import *
from ...Main.CollapseRaw.Typedef import is_typedef, collapse_typedef


@pytest.mark.parametrize('s, expected', [
    ('alias a int64', True),
    ('a = 5', False),
    ('alias vec (float64[]))', True),
    ('a = b + c = d', False),
    ('alias aa22bbcc ((float64)[])', True),
])
def test_1(s, expected):
    assert is_typedef(tokenize(s)) == expected


@pytest.mark.parametrize('s, expected', [
    (
        'alias a a',
        CheckControlRawTypedef(
            'a',
        [
            CTR(T_WRD, 'a'),
        ])
    ),
    (
        'alias field (int64[100, 300])',
        CheckControlRawTypedef(
            'field',
        [
            CTR(T_SYM, '('),
            CTR(T_WRD, 'int64'),
            CTR(T_SYM, '['),
            CTR(T_LIT, '100'),
            CTR(T_SYM, ','),
            CTR(T_LIT, '300'),
            CTR(T_SYM, ']'),
            CTR(T_SYM, ')'),
        ])
    ),
])
def test_2(s, expected):
    err, res = [], []
    collapse_typedef(tokenize(s), err, res)
    assert not err
    assert len(res) == 1
    expected.is_match(res[0])


@pytest.mark.parametrize('s', [
    (
        'alias a'
    ),
    (
        'alias'
    ),
])
def test_2(s):
    err, res = [], []
    collapse_typedef(tokenize(s), err, res)
    assert err