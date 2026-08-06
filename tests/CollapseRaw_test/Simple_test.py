import pytest
from .Simple import CheckTokenRaw, tokenize
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Simple import split_by_comma



@pytest.mark.parametrize('s, needed', [
    (
        'a, b , c, f ,x',
        [
            [CheckTokenRaw(TokenRawWord, 'a')],
            [CheckTokenRaw(TokenRawWord, 'b')],
            [CheckTokenRaw(TokenRawWord, 'c')],
            [CheckTokenRaw(TokenRawWord, 'f')],
            [CheckTokenRaw(TokenRawWord, 'x')],
        ]
    ),

    (
        'aa, b, c + x',
        [
            [CheckTokenRaw(TokenRawWord, 'aa')],
            [CheckTokenRaw(TokenRawWord, 'b')],
            [
                CheckTokenRaw(TokenRawWord, 'c'),
                CheckTokenRaw(TokenRawSymbol, '+'),
                CheckTokenRaw(TokenRawWord, 'x'),
            ],
        ]
    ),

    (
        'a, (b + c, d)',
        [
            [CheckTokenRaw(TokenRawWord, 'a')],
            [
                CheckTokenRaw(TokenRawSymbol, '('),
                CheckTokenRaw(TokenRawWord, 'b'),
                CheckTokenRaw(TokenRawSymbol, '+'),
                CheckTokenRaw(TokenRawWord, 'c'),
                CheckTokenRaw(TokenRawSymbol, ','),
                CheckTokenRaw(TokenRawWord, 'd'),
                CheckTokenRaw(TokenRawSymbol, ')'),
            ],
        ]
    ),

    (
        'ax',
        [
            [CheckTokenRaw(TokenRawWord, 'ax')],
        ]
    ),

    (
        '',
        [
        ]
    ),

])
def test_1(s, needed):
    err = []
    tokens = tokenize(s)
    result = split_by_comma(tokens, "ошибка", err)

    assert not err

    assert len(result) == len(needed)

    for have, need in (
        ((result[i], needed[i]) for i in range(len(needed)))
    ):
        assert isinstance(have, list)
        assert len(have) == len(need)
        for i in range(len(need)):
            need[i].is_match(have[i])


@pytest.mark.parametrize('forbidden', [
    'blob,,,', 'x,x,', ',x,x', 'x,,x', ','
])
def test_2(forbidden):
    err = []
    split_by_comma(tokenize(forbidden), '', err)
    assert err


