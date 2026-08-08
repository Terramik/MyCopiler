from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from ....Definitions.Scopes import *
from ....Definitions.Tokens import *
from ....Definitions.Exceptions import SemanticError
import random
from functools import singledispatch


@singledispatch
def analyze_wvalue(node: TokenOperatorWvalueABC, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    raise NotImplementedError(f"analyze_wvalue не реализован для {type(node).__name__}")


@singledispatch
def analyze_rvalue(node: TokenOperatorRvalueABC, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    raise NotImplementedError(f"analyze_rvalue не реализован для {type(node).__name__}")


def cast_if_need(operand: TokenOperatorRvalueABC, type_need: Type) -> TokenOperatorRvalueABC:
    """Вставляет узел приведения, если типы не совпадают."""
    if operand.res_type == type_need:
        return operand
    return TokenOperatorCast(type_need, operand, zero_origin)


def err(node: TokenOperatorWvalueABC | TokenOperatorRvalueABC) -> Type:
    """Устанавливает состояние надо на ошибку и возвращает её"""
    node.res_type = t_error
    return t_error


def is_in_key_word(word: str) -> bool:
    return word in BaseTypes or word in KeyWords


def analyze_type(_type: Type, scope: Scope, origin: TokenOrigin, errors: list[SemanticError]) -> Type:
    """Анализирует тип, проверяет и делает то что нужно."""
    # функция
    if _type.is_simple_func:
        args = [
            analyze_type(t, scope, origin, errors)
            for t in _type.simple.arguments
        ]
        if any(t == t_error for t in args):
            return t_error
        res = [
            analyze_type(t, scope, origin, errors)
            for t in _type.simple.results
        ]
        if any(t == t_error for t in res):
            return t_error
        return Type(Type.SimpleTypeFunc(args, res), _type.modifiers, _type.origin)
    else:
        # сырое слово
        assert _type.is_simple_raw
        raw_name: str = _type.simple.raw_name
        indexes: list[str] = _type.simple.indexes

        # просто базовый тип
        if raw_name in BaseTypes:
            _type.simple = Type.SimpleTypeBase(BaseTypes(raw_name))
        # если это не он - это псевдоним или класс(возможно в классе)
        else:
            if raw_name in KeyWords or any(n in KeyWords for n in indexes):
                errors.append(SemanticError('Неожиданное использование ключевых слов', origin))
                return t_error

            last_scope = scope

            if indexes:
                indexes = [raw_name] + indexes
                raw_name = indexes[-1]
                start_name = indexes[0]
                indexes = indexes[1:-1]
                # есть индексы, start_name - имя класса, так что перейдём в него
                cls = last_scope.find_variable(start_name, False)
                if not (cls is not None and cls[0].type.is_simple_class):
                    errors.append(SemanticError(f'Класса {start_name} нету', origin))
                    return t_error
                cls = cls[0].type.cls
                assert isinstance(cls, ControlClass)
                assert cls.scope
                last_scope = cls.scope

                i = 0
                # проходимся по вложенным скоупам класса
                while i < len(indexes):
                    name = indexes[i]
                    class_ = last_scope.find_class_in_cur_scope(name)
                    if class_ is None:
                        errors.append(SemanticError(f'Имени класса "{name}" не обнаружено', origin))
                        return t_error
                    last_scope = last_scope.get_child_scope_from_creator(class_)
                    i += 1

            # теперь, когда мы тем или иным путём в нужном скоупе, делаем сам простой тип
            typedef = last_scope.find_typedef(raw_name)
            if typedef is None:
                var = last_scope.find_variable(raw_name, False)
                if not (
                    var is not None and (
                        var[0].type.is_simple_class or var[0].type.is_simple_enum
                    )
                ):
                    errors.append(SemanticError(f'Имени "{raw_name}" нет ни как класса, ни как псевдонима, '
                                                'ни как перечисления для использования как типа', origin))
                    return t_error

                var = var[0]
                if var.type.is_simple_class:
                    cls = var.type.cls
                    simple = Type.SimpleTypeClassInstance(cls)
                else:
                    enum = var.type.enum
                    simple = Type.SimpleTypeEnumInstance(enum)
            else:
                simple = Type.SimpleTypeTypedef(typedef.typedef, typedef.typedef.conj(_type.modifiers))

            return Type(simple, _type.modifiers, _type.origin)