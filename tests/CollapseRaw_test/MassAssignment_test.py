import pytest
from .Simple import *
from ...Definitions.Raw import *
from ...Definitions.Exceptions import OurSyntaxError
from ...Main.CollapseRaw.MassAssignment import is_mass_assignment, collapse_mass_assignment


@pytest.mark.parametrize("s, expected", [
    ("a, b = c, d", True),
    ("a = b", False),
    ("a, b = f()", True),
    ("(a, b) = c", False),
    ("a, = b", True),
])
def test_1(s, expected):
    assert is_mass_assignment(tokenize(s)) == expected


@pytest.mark.parametrize("s, expected", [
    (
        "a, b = c, d",
        CheckControlRawMassAssignment(
            [
                [CTR(T_WRD, 'a')],
                [CTR(T_WRD, 'b')]
            ],
            [
                [CTR(T_WRD, 'c')],
                [CTR(T_WRD, 'd')]
            ]
        )
    ),
    (
        "x, y = f(1), 2 * 3",
        CheckControlRawMassAssignment(
            [
                [CTR(T_WRD, 'x')],
                [CTR(T_WRD, 'y')]
            ],
            [

                [
                    CTR(T_WRD, 'f'),
                    CTR(T_SYM, '('),
                    CTR(T_LIT, '1'),
                    CTR(T_SYM, ')')
                ],
                [
                    CTR(T_LIT, '2'),
                    CTR(T_SYM, '*'),
                    CTR(T_LIT, '3')
                ]
            ]
        )
    ),
    (
        "x, y, z = f(), a - 3",
        CheckControlRawMassAssignment(
            [
                [CTR(T_WRD, 'x')],
                [CTR(T_WRD, 'y')],
                [CTR(T_WRD, 'z')]
            ],
            [
                [
                    CTR(T_WRD, 'f'),
                    CTR(T_SYM, '('),
                    CTR(T_SYM, ')')
                ],
                [
                    CTR(T_WRD, 'a'),
                    CTR(T_SYM, '-'),
                    CTR(T_LIT, '3')
                ]
            ]
        )
    )
])
def test_collapse_mass_assignment(s, expected):
    err, res = [], []
    collapse_mass_assignment(tokenize(s), err, res)
    assert not err
    assert len(res) == 1
    expected.is_match(res[0])


@pytest.mark.parametrize("s", [
    "a, b =",
    "= a, b",
    "a,,b = c",
    "a, b = c,,d",
])
def test_3(s):
    err, res = [], []
    collapse_mass_assignment(tokenize(s), err, res)
    assert err
