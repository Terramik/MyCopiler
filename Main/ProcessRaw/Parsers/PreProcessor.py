from ....Definitions.Raw import *
from .Definitions import *
from ....Definitions.Exceptions import OurSyntaxError

# должен сделать из рядов сырых токенов что-то более обрабатываемое


def preprocess(data: list[TokenRawABC]) -> list[PreprocessResults]:
    """
    Преобразовывает массив из сырых токенов в что-то более удобное
    """
    res = []
    for tok in data:
        match tok:
            case TokenRawLiteral():
                res.append(RawOperand(tok, tok.origin))
            case TokenRawWord():
                res.append(RawOperand(tok, tok.origin))
            case TokenRawSymbol():
                s = tok.symbol
                match s:
                    case '(':
                        res.append(BracketOpen(tok.origin))
                    case ')':
                        res.append(BracketClose(tok.origin))
                    case ',':
                        res.append(Separator(tok.origin))
                    case '[':
                        res.append(SquareBracketOpen(tok.origin))
                    case ']':
                        res.append(SquareBracketClose(tok.origin))
                    case ':':
                        res.append(Delimiter(tok.origin))
                    case _:
                        if not (
                                s in TokenOperatorBinaryTypes or
                                s in TokenOperatorPrefixTypes or
                                s in TokenOperatorPostfixTypes
                        ):
                            raise OurSyntaxError(f'Символ {s} не является оператором ', tok.origin)
                        res.append(RawOperator(
                            tok.symbol, tok.origin
                        ))
    return res
