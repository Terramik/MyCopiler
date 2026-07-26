import pytest
from ..Definitions.Raw import *
from ..Definitions.Exceptions import ReadError
from ..Main.Tokenize import tokenize_file
from dataclasses import dataclass
from io import StringIO


@dataclass(slots=True)
class CheckType:
    type: ControlRawABC
    val: str


def test_1():
    data = StringIO('''
    def main(  \t  ) -> ( \nint32 ) { 
        float32 f = 1.2; 
        {
            f = f * 2; # blob glob
        }  # xd
        # blob and glob
        f = f - f;
        var str int8[] = "bloba and globa shili \\v meste i ne tushilu";
        return 0;
        }
    ''')
    tokens = tokenize_file(data, Path(''))
    needed = (
        CheckType(TokenRawWord, 'def'),
        CheckType(TokenRawWord, 'main'),
        CheckType(TokenRawSymbol, '('),
        CheckType(TokenRawSymbol, ')'),
        CheckType(TokenRawSymbol, '->'),
        CheckType(TokenRawSymbol, '('),
        CheckType(TokenRawWord, 'int32'),
        CheckType(TokenRawSymbol, ')'),
        CheckType(TokenRawSymbol, '{'),
        CheckType(TokenRawWord, 'float32'),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, '='),
        CheckType(TokenRawLiteral, '1.2'),
        CheckType(TokenRawSymbol, ';'),
        CheckType(TokenRawSymbol, '{'),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, '='),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, '*'),
        CheckType(TokenRawLiteral, '2'),
        CheckType(TokenRawSymbol, ';'),
        CheckType(TokenRawSymbol, '}'),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, '='),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, '-'),
        CheckType(TokenRawWord, 'f'),
        CheckType(TokenRawSymbol, ';'),
        CheckType(TokenRawSymbol, 'var'),
        CheckType(TokenRawWord, 'str'),
        CheckType(TokenRawWord, 'int8'),
        CheckType(TokenRawSymbol, '['),
        CheckType(TokenRawSymbol, ']'),
        CheckType(TokenRawSymbol, '='),
        CheckType(TokenRawLiteral, '"bloba and globa shili \\v meste i ne tushilu"'),
        CheckType(TokenRawSymbol, ';'),
        CheckType(TokenRawWord, 'return'),
        CheckType(TokenRawLiteral, '0'),
        CheckType(TokenRawSymbol, ';'),
        CheckType(TokenRawSymbol, '}'),
    )
    assert len(tokens) == len(needed)
    for tok, need in (
        ((tokens[i], needed[i]) for i in range(len(tokens)))
    ):
        assert isinstance(tok, need.type)
        v = None
        match tok:
            case TokenRawWord():
                v = tok.word
            case TokenRawSymbol():
                v = tok.symbol
            case TokenRawLiteral():
                v = tok.literal
        assert v == need.val


@pytest.mark.parametrize('forbidden', [
    '$ # xd', '№ and №', '@@@@@@@'
])
def test_2(forbidden):
    data = StringIO(forbidden)
    with pytest.raises(ReadError):
        tokenize_file(data, Path(''))


