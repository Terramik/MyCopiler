import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Class import is_class, collapse_class
from ...Main.CollapseRaw import collapse_raw


@pytest.mark.parametrize('s, expected', [
    ('def foo()', False),
    ('class foo', True),
    ('return a, b + c', False),
    ('a = b + c = d', False),
    ('elif bob and tom', False),
    ('class _1_2_3_4_5_4_3_2_1_', True),
])
def test_1(s, expected):
    assert is_class(tokenize(s)) == expected


dummy_block_ = ControlRawCodeBlock([], zero_origin)
dummy_block = ControlRawCodeBlock([ControlRawCodeBlock([], zero_origin)], zero_origin)
dummy_check_block = CheckControlRawCodeBlock([])


@pytest.mark.parametrize('code, expected', [
    (
        '''
        class glob {
            {}        
        }
        ''',
        CheckControlRawClass(
            'glob',
            CheckControlRawCodeBlock([
            ]),
            CheckControlRawCodeBlock([
                CheckControlRawCodeBlock([

                ])
            ])
        )
    ),
    (
        '''
        class blob {
            {
                a int64;
                b (int64*); 
            }        
        }
        ''',
        CheckControlRawClass(
            'glob',
            CheckControlRawCodeBlock([
                CheckControlRawExpression([
                    CTR(T_WRD, 'a'),
                    CTR(T_WRD, 'int64'),
                ]),
                CheckControlRawExpression([
                    CTR(T_WRD, 'b'),
                    CTR(T_SYM, '('),
                    CTR(T_WRD, 'int64'),
                    CTR(T_SYM, '*'),
                    CTR(T_SYM, ')'),
                ])
            ]),
            CheckControlRawCodeBlock([
                CheckControlRawCodeBlock([
                    CheckControlRawExpression([
                        CTR(T_WRD, 'a'),
                        CTR(T_WRD, 'int64'),
                    ]),
                    CheckControlRawExpression([
                        CTR(T_WRD, 'b'),
                        CTR(T_SYM, '('),
                        CTR(T_WRD, 'int64'),
                        CTR(T_SYM, '*'),
                        CTR(T_SYM, ')'),
                    ])
                ])
            ])
        )
    ),
    (
        '''
        class asdasd {
            {}        
            var blob bool;
        }
        ''',
        CheckControlRawClass(
            'asdasd',
            CheckControlRawCodeBlock([
            ]),
            CheckControlRawCodeBlock([
                CheckControlRawCodeBlock([
                ]),
                CheckControlRawExpression([
                    CTR(T_WRD, 'var'),
                    CTR(T_WRD, 'a'),
                    CTR(T_WRD, 'int64'),
                ])
            ])
        )
    ),
])
def test_2(code, expected):
    expected.is_match(collapse_raw(tokenize(code)).block_parts[0])


@pytest.mark.parametrize('s, block', [
    ('class', dummy_block),
    ('class ()', dummy_block),
    ('class and', dummy_block),
    ('class blob', ControlRawCodeBlock([], zero_origin)),
])
def test_3(s, block):
    with pytest.raises(OurSyntaxError):
        collapse_class(tokenize(s), block)
