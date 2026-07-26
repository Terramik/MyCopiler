import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Enums import is_enum, collapse_enum


@pytest.mark.parametrize('s, expected', [
    ('enum foo', True),
    ('a = 5', False),
    ('return a, b + c', False),
    ('a = b + c = d', False),
    ('enum ERRORS', True),
    ('enum asdasdasd', True),
])
def test_1(s, expected):
    assert is_enum(tokenize(s)) == expected


dummy_block = ControlRawCodeBlock([], zero_origin)


@pytest.mark.parametrize('s, code_block, expected', [
    (
        'enum blob',
        ControlRawCodeBlock([
            ControlRawExpression([TokenRawWord('a', zero_origin)], zero_origin),
            ControlRawExpression([TokenRawWord('b', zero_origin)], zero_origin),
        ], zero_origin
        ),
        CheckControlRawEnum(
            'blob', [
                'a', 'b'
            ]
        )
    ),
    (
        'class ERRORS',
        ControlRawCodeBlock([
            ControlRawExpression([TokenRawWord('FNF', zero_origin)], zero_origin),
            ControlRawExpression([TokenRawWord('MNF', zero_origin)], zero_origin),
            ControlRawExpression([TokenRawWord('ZDE', zero_origin)], zero_origin),
        ], zero_origin
        ),
        CheckControlRawEnum(
            'ERRORS', [
                'FNF', 'MNF', 'ZDE'
            ]
        )
    )
])
def test_2(s, code_block, expected):
    expected.is_match(collapse_enum(tokenize(s), code_block))


@pytest.mark.parametrize('s', [
    'enum',
    'enum ()',
    'enum foo( asd asd',
])
def test_3(s):
    with pytest.raises(OurSyntaxError):
        collapse_enum(tokenize(s), dummy_block)
