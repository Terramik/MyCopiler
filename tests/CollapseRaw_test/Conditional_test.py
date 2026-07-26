import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.Conditional import is_conditional, collapse_conditional, clue_conditional


@pytest.mark.parametrize('s, expected', [
    ('def foo()', False),
    ('if true != false', True),
    ('return a, b + c', False),
    ('a = b + c = d', False),
    ('elif bob and tom', True),
    ('else', True),
])
def test_1(s, expected):
    assert is_conditional(tokenize(s)) == expected


dummy_block = ControlRawCodeBlock([], zero_origin)
dummy_check_block = CheckControlRawCodeBlock([])


@pytest.mark.parametrize('s, expected', [
    (
        'if tom and bob',
        CheckControlRawIf(
            ConditionalPartTypes.start,
            [
                CTR(T_WRD, 'tom'),
                CTR(T_SYM, 'and'),
                CTR(T_WRD, 'bob'),
            ],
            dummy_check_block, dummy_check_block
        )
    ),
    (
        'elif bob != tom',
        CheckControlRawIf(
            ConditionalPartTypes.middle,
            [
                CTR(T_WRD, 'bob'),
                CTR(T_SYM, '!='),
                CTR(T_WRD, 'tom'),
            ],
            dummy_check_block, dummy_check_block
        )
    ),
    (
        'else',
        CheckControlRawIf(
            ConditionalPartTypes.end,
            [],
            dummy_check_block, dummy_check_block
        )
    ),
])
def test_2(s, expected):
    expected.is_match(collapse_conditional(tokenize(s), dummy_block))


@pytest.mark.parametrize('s, expected', [
    (
        [
            'if blob > 1',
            'elif blob > 2',
            'elif blob > 3',
            None
        ],
        [
            CheckControlRawIf(
                ConditionalPartTypes.start,
                [
                    CTR(T_WRD, 'blob'),
                    CTR(T_SYM, '>'),
                    CTR(T_LIT, '1'),
                ],
                dummy_check_block,
                CheckControlRawCodeBlock([
                    CheckControlRawIf(
                        ConditionalPartTypes.middle,
                        [
                            CTR(T_WRD, 'blob'),
                            CTR(T_SYM, '>'),
                            CTR(T_LIT, '2'),
                        ],
                        dummy_check_block,
                        CheckControlRawCodeBlock([
                            CheckControlRawIf(
                                ConditionalPartTypes.middle,
                                [
                                    CTR(T_WRD, 'blob'),
                                    CTR(T_SYM, '>'),
                                    CTR(T_LIT, '3'),
                                ],
                                dummy_check_block, dummy_check_block
                            )
                        ])
                    )
                ])
            ),
            dummy_check_block
        ]
    ),
    (
        [
            'if not false',
            'else',
            'if true',
            'elif blob > 3'
        ],
        [
            CheckControlRawIf(
                ConditionalPartTypes.start,
                [
                    CTR(T_SYM, 'not'),
                    CTR(T_LIT, 'false'),
                ],
                dummy_check_block,
                dummy_check_block
            ),
            CheckControlRawIf(
                ConditionalPartTypes.start,
                [
                    CTR(T_LIT, 'true'),
                ],
                dummy_check_block,
                CheckControlRawCodeBlock([
                    CheckControlRawIf(
                        ConditionalPartTypes.middle,
                        [
                            CTR(T_WRD, 'blob'),
                            CTR(T_SYM, '>'),
                            CTR(T_LIT, '3'),
                        ],
                        dummy_check_block,
                        dummy_check_block
                    )
                ])
            )
        ]
    ),
    (
        [
            None,
            'if bob',
            'elif tom',
            'else',
            None
        ],
        [
            dummy_check_block,
            CheckControlRawIf(
                ConditionalPartTypes.start,
                [
                    CTR(T_WRD, 'bob'),
                ],
                dummy_check_block,
                CheckControlRawCodeBlock([
                    CheckControlRawIf(
                        ConditionalPartTypes.middle,
                        [
                            CTR(T_WRD, 'tom'),
                        ],
                        dummy_check_block,
                        dummy_check_block
                    )
                ])
            ),
            dummy_check_block
        ]
    ),
])
def test_3(s, expected):
    s = [collapse_conditional(tokenize(l), dummy_block) if l is not None else dummy_block for l in s]
    clue_conditional(s)
    check_depth_one(expected, s)


@pytest.mark.parametrize('s', [
    [
        'elif blob > 3',
        'if blob > 1',
    ],
    [
        'else',
        'if blob > 1',
    ],
    [
        'if blob > 1',
        None,
        'elif blob > 3',
    ],
    [
        'if blob > 1',
        None,
        'else',
    ],
])
def test_4(s):
    s = [collapse_conditional(tokenize(l), dummy_block) if l is not None else dummy_block for l in s]
    with pytest.raises(OurSyntaxError):
        clue_conditional(s)




