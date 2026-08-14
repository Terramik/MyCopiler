from ...Definitions.Scopes import Scope
from ...Definitions.TreeInterface import IteratorControlWithScope
from ...Definitions.Tokens import *
from functools import reduce


"""
Должен делать из del(что-то то там) в явное cls.__del__(...), и циклы и прочее при надобности
"""


__all__ = ('expand_deinitializers',)


class ItCont(IteratorControlWithScope):
    NAMES_COUNT = 1

    def on_expression_control(self, expr: ControlExpression):
        # начинаем
        if isinstance(expr.first, TokenOperatorDeInitializer):
            if expr.first.res_type == t_error:
                return

            thing_to_del = expr.first.operand
            type_to_del = thing_to_del.res_type
            cls = type_to_del.cls
            del_origin = expr.first.origin

            assert isinstance(cls, ControlClass)
            if cls.is_bad:
                return

            if type_to_del.is_mod_usual or type_to_del.is_mod_pointer:
                # это просто Class*, разыменуем
                if type_to_del.is_mod_pointer:
                    type_to_del = type_to_del.without_one_modifier()
                    thing_to_del = TokenOperatorDereferencing(
                        thing_to_del, del_origin, type_to_del
                    )

                # теперь это просто Class, вызовем __del__ и всё
                expr.first = TokenOperatorFunctionCall(
                    TokenOperatorFieldAccess(
                        TokenVariableAccess(cls.name, del_origin, False, cls.class_var)
                        , '__del__', del_origin, Type(Type.SimpleTypeFunc([type_to_del], []), []),
                        cls.find_class_field('__del__')
                    ), [
                        thing_to_del
                    ], del_origin, None
                )
            else:
                # всё сложнее, так что... мы будем итерироваться

                # для начала, сделаем количество нужных элементов, и представим это всё как 1д срез

                # делаем срез
                if type_to_del.is_mod_array:
                    # подсчитаем количество размерностей и количество элементов
                    dims_num = 0
                    elem_num = 1
                    while type_to_del.is_mod_array:
                        dims_num += 1
                        elem_num *= type_to_del.length
                        type_to_del = type_to_del.without_one_modifier()
                    # теперь сделаем сам срез
                    type_to_del_slice = types.add_modifiers(type_to_del, [Type.ModifierSlise(1)])
                    thing_to_del = TokenOperatorSlize(
                        thing_to_del, [
                            TokenLiteral.from_raw(TokenRawLiteral('0', del_origin))
                            for _ in range(dims_num)
                        ], [
                            TokenLiteral.from_raw(TokenRawLiteral(str(elem_num), del_origin))
                        ], del_origin, type_to_del_slice
                    )
                elif type_to_del.is_mod_slize:
                    # нужно сделать мега-структуру индексации
                    to_index = [thing_to_del]
                    for _ in range(type_to_del.dimensions-1):
                        to_index.append(
                            TokenOperatorIndex(
                                to_index[-1],
                                TokenLiteral.from_raw(TokenRawLiteral('0', del_origin)),
                                del_origin,
                                to_index[-1].res_type.without_one_dimension()
                            )
                        )
                    to_index = [
                        TokenOperatorLenof(t, del_origin, types.int64)
                        for t in to_index
                    ]

                    def reducer(left: TokenOperatorRvalueABC, right: TokenOperatorRvalueABC) -> TokenOperatorRvalueABC:
                        return TokenOperatorBinary(
                            TokenOperatorBinaryTypes.ArfmMul,
                            left, right, del_origin, types.int64
                        )

                    elem_num = reduce(reducer, to_index)
                    # и сам срез
                    type_to_del_slice = types.add_modifiers(type_to_del, [Type.ModifierSlise(1)])
                    thing_to_del = TokenOperatorSlize(
                        thing_to_del, [
                            TokenLiteral.from_raw(TokenRawLiteral('0', del_origin))
                            for _ in range(type_to_del.dimensions)
                        ], [
                            elem_num
                        ], del_origin, type_to_del_slice
                    )
                else:
                    raise ValueError('blob')


                # переменные
                # для среза
                slice_var_name = self.current_scope.get_unique_name(f'expanded_deinitializer_slice_{self.NAMES_COUNT}')
                slice_var_def = TokenOperatorVariableDefinition(slice_var_name, type_to_del_slice, del_origin)
                slice_var_access = TokenVariableAccess(slice_var_name, del_origin, False, slice_var_def)
                self.current_scope.add_variable(slice_var_def)
                # для индексации
                index_var_name = self.current_scope.get_unique_name(f'expanded_deinitializer_index_{self.NAMES_COUNT}')
                index_var_def = TokenOperatorVariableDefinition(index_var_name, types.int64, del_origin)
                index_var_access = TokenVariableAccess(index_var_name, del_origin, False, index_var_def)
                self.current_scope.add_variable(index_var_def)
                self.NAMES_COUNT += 1

                # заменим del на получение среза
                expr.first = TokenOperatorAssignment(
                    slice_var_def, thing_to_del, del_origin, type_to_del_slice
                )
                # теперь перед выражением засунем объявление счётчика
                self.current_block.block_parts.insert(
                    self._get_index(expr) + 1,
                    ControlExpression(
                        TokenOperatorAssignment(
                            index_var_def, TokenLiteral.from_raw(TokenRawLiteral('0', del_origin)),
                            del_origin, types.int64
                        ), del_origin
                    )
                )
                # и собственно сам цикл
                while_ = ControlWhile(
                    TokenOperatorBinary(
                        TokenOperatorBinaryTypes.ComprLessOrEq,
                        index_var_access,
                        TokenOperatorLenof(slice_var_access, del_origin, types.int64),
                        del_origin, types.bool
                    ),
                    ControlCodeBlock([
                        ControlExpression(
                            TokenOperatorFunctionCall(
                                TokenOperatorFieldAccess(
                                    TokenVariableAccess(cls.name, del_origin, False, cls.class_var)
                                    , '__del__', del_origin, Type(Type.SimpleTypeFunc([type_to_del], []), []),
                                    cls.find_class_field('__del__')
                                ), [
                                    TokenOperatorIndex(
                                        slice_var_access, index_var_access, del_origin, type_to_del
                                    )
                                ], del_origin, None
                            ), del_origin
                        )
                    ], del_origin
                    ), del_origin
                )
                self.current_block.block_parts.insert(
                    self._get_index(expr) + 2, while_
                )
                while_scope = Scope(Scope.Types.Cycle, while_, self.current_scope)
                self.current_scope.add_child(while_scope)


def expand_deinitializers(code: ControlCodeBlock, scope: Scope):
    ItCont().start(code, scope)
