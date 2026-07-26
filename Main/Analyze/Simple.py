from ...Definitions.Enums import *
from ...Definitions.Scopes import *
from ...Definitions.Tokens import *
from ...Definitions.Exceptions import SemanticError


def is_in_key_word(word: str) -> bool:
    if word in BaseTypes or word in KeyWords:
        return True
    return False
