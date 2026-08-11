from ....Definitions.Scopes import *
from ....Definitions.Tokens import *
from ....Definitions.Exceptions import SemanticError
from ....Definitions import TypesShortener as types
from ..Types import *
from ..Simple import *
from .Utils import *


__all__ = ('analyze_rvalue',)


@analyze_rvalue.register(TokenVariableAccess)
def _(node: TokenVariableAccess, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    r = scope.find_variable(node.name, True)
    if r is None:
        errors.append(SemanticError(f'Попытка чтения из необъявленной переменной "{node.name}"', node.origin))
        # сделаем такую переменную, чтобы не кидать больше таких ошибок(2)
        err_var = TokenOperatorVariableDefinition(node.name, t_error, node.origin)
        node.is_nonlocal = False
        node.var_def = err_var
        scope.add_variable(err_var)
        return t_error

    var, is_nonlocal = r
    node.is_nonlocal = is_nonlocal
    node.var_def = var
    return var.type


@analyze_rvalue.register(TokenLiteral)
def _(node: TokenLiteral, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return node.res_type


@analyze_rvalue.register(TokenOperatorAssignment)
def _(node: TokenOperatorAssignment, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_have = analyze_rvalue(node.right, scope, node, errors)
    type_need = analyze_wvalue(node.left, scope, node, errors)

    if type_have == t_error or type_need == t_error:
        return err(node)

    assert type_need

    if type_have != type_need and not type_have.is_castable_implicitly(type_need):
        errors.append(SemanticError(
            f'Тип {type_have} не может быть неявно приведён к типу {type_need} для присваивания.',
            node.left.origin + node.right.origin
        ))
        return err(node)
    node.right = cast_if_need(node.right, type_need)
    node.res_type = type_need
    return type_need


@analyze_rvalue.register(TokenOperatorFunctionCall)
def analyze_fcall(node: TokenOperatorFunctionCall, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    func_type = analyze_rvalue(node.func, scope, node, errors)

    # просто проанализируем параметры, чтобы дать им данные
    if func_type == t_error:
        for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
        return err(node)

    _func_type = func_type.full_type

    # это вызов класса(то есть, создание экзепляра)
    if _func_type.is_simple_class and _func_type.is_mod_usual:
        # меняем класс на обращение к полю "__init__" класса
        cls = _func_type.cls
        init = cls.find_class_field('__init__')
        if init is None:
            errors.append(SemanticError(f'Класс {cls.name} не имеет метода __init__', cls.origin))
            for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
            return err(node)
        node.func = TokenOperatorFieldAccess(
            node.func, '__init__', node.func.origin, init.type, init
        )
        func_type = init.type

    # это вызов экзепляра класса(то есть, вызов __call__)
    if _func_type.is_simple_class_instance and \
            (_func_type.is_mod_usual or _func_type.is_mod_pointer and len(_func_type.modifiers)):
        # меняем объект на обращение к полю "__call__" объекта
        cls = _func_type.cls
        call = cls.find_class_field('__call__')
        if call is None:
            errors.append(SemanticError('Попытка вызова экзепляра класса без определённого метода __call__', node.func.origin))
            for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
            return err(node)
        # для обычного и указателя
        if _func_type.is_mod_:
            new_func = TokenOperatorFieldAccess(
                node.func, '__call__', node.func.origin, call.type, call
            )
        else:
            new_func = TokenOperatorFieldAccessPointer(
                node.func, '__call__', node.func.origin, call.type, call
            )
        node.func = new_func

    _func_type = func_type.full_type

    # проверяем, что это чистая функций
    if not _func_type.is_simple_func:
        errors.append(SemanticError(f'Для использовании в вызове функции тип вызываемого должен '
                                    f'быть функцией, дано {func_type}', node.func.origin))
        for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
        return err(node)

    if not _func_type.is_mod_usual:
        errors.append(SemanticError(f'Для использовании в вызове функции тип вызываемого должен '
                                    f'быть чистой функцией без модификаторов, дана {func_type}', node.func.origin))
        for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
        return err(node)

    # проверим, вызывается ли это нечто от экземпляра класса
    skip_check_first_arg = False
    if isinstance(node.func, (TokenOperatorFieldAccess, TokenOperatorFieldAccessPointer)):
        if node.func.operand.res_type.is_simple_class_instance:
            skip_check_first_arg = True
            # если это не указатель, а нам нужен указатель, то мы возьмём адрес
            if (node.func.operand.res_type.is_mod_usual and
                    len(_func_type.simple.arguments) >= 1 and
                    not _func_type.simple.arguments[0].is_mod_usual and
                    _func_type.simple.arguments[0].without_one_modifier() == node.func.operand.res_type
            ):
                # проверка, что это wvalue(хотя, она немного вызывает сомнения)
                if not isinstance(node.func.operand, TokenOperatorWvalueABC):
                    errors.append(SemanticError('Ожидалось wvalue(для неявной передачи указателя на экземпляр)', node.func.operand.origin))
                    for arg in node.arguments: analyze_rvalue(arg, scope, node, errors)
                    return err(node)
                # засунем взятие адреса
                node.arguments.insert(0, TokenOperatorReferencing(
                    node.func.operand, node.func.operand.origin, _func_type.simple.arguments[0]
                ))
            else:
                # засунем просто
                node.arguments.insert(0, node.func.operand)

    func = _func_type.simple
    assert isinstance(func, Type.SimpleTypeFunc)

    # проверка результатов
    res_num = len(func.results)
    # функции без результатов можно применить только в начале обычного выражения
    if res_num == 0:
        if not isinstance(parent, ControlExpression):
            errors.append(SemanticError('Функции, не возвращающие значения, могут быть только в начале '
                                        'обычного выражения(управляющей конструкции)', node.origin))
            for arg in node.arguments[1:] if skip_check_first_arg else node.arguments: analyze_rvalue(arg, scope, node, errors)
            return err(node)
    # функции со множественным результатом могут быть только в выражениях и множественных присваиваниях
    if res_num > 1:
        if not isinstance(parent, (ControlExpression, ControlMassAssignment)):
            errors.append(SemanticError('Функции, возвращающие больше 1 значения, могут быть только в начале '
                                        'обычных выражений и массовых присваиваниях', node.origin))
            for arg in node.arguments[1:] if skip_check_first_arg else node.arguments: analyze_rvalue(arg, scope, node, errors)
            return err(node)

    # проверка параметров
    args_num = len(func.arguments)
    if len(node.arguments) != args_num:
        errors.append(SemanticError(f"Функция типа {func_type} ожидает {args_num} аргументов, "
                                    f"передано {len(node.arguments)}", node.origin))
        for arg in node.arguments[1:] if skip_check_first_arg else node.arguments: analyze_rvalue(arg, scope, node, errors)
        return err(node)

    error_occurred = False
    # сама поэлементная проверка
    for i, (arg, type_need) in enumerate(zip(node.arguments, func.arguments)):
        if skip_check_first_arg and i == 0:
            type_have = arg.res_type # чтобы не анализировать 2 раза и добавлять штуки по 2 раза
        else:
            type_have = analyze_rvalue(arg, scope, node, errors)

        if type_have == t_error:
            error_occurred = True
            continue

        arg = node.arguments[i]

        if type_need != type_have and not type_have.is_castable_implicitly(type_need):
            errors.append(SemanticError(
                f'Тип {type_have} неявно неприводим к типу {type_need} для передачи '
                f'как {i} аргумент функции типа {func_type}', arg.origin
            ))
            error_occurred = True
            continue
        node.arguments[i] = cast_if_need(arg, type_need)

    if error_occurred:
        return err(node)

    if res_num == 1:
        node.res_type = func.results[0]
        return node.res_type
    else:
        # хотя, это нужно для обработки массового присваивания
        node.res_type = _func_type
        return _func_type


NESTED_VARS_COUNTER = 0


def _process_nested_comparison(node: TokenOperatorBinary, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    """Обработка цепочек вида a < b < c → a < b and b < c с созданием временной переменной."""
    #
    global NESTED_VARS_COUNTER
    assert isinstance(node.left, TokenOperatorBinary)
    # наша новая вершина(and)
    node_ = TokenOperatorBinary(
        TokenOperatorBinaryTypes.LogAnd,
        node.left, node, node.origin, t_bool
    )
    change_child(parent, node, node_)
    node = node_
    # теперь возьмём правую часть левого сравнения, и запишем её во временную переменную
    analyze_rvalue(node.left.right, scope, node.right, errors)

    # временная переменная
    temp_var_def = TokenOperatorVariableDefinition(
        scope.get_unique_name(f'nested_compression_temp_var_{NESTED_VARS_COUNTER}'), node.left.right.res_type, node.origin
    )
    scope.add_variable(temp_var_def)
    temp_var_access = TokenVariableAccess(temp_var_def.name, node.origin, False, temp_var_def)
    NESTED_VARS_COUNTER += 1

    # собственно заменяем
    node.left.right = TokenOperatorAssignment(
        temp_var_def, node.left.right, node.origin, node.left.right.res_type
    )
    # теперь заменим левую часть правой части на доступ к временной переменной
    assert isinstance(node.right, TokenOperatorBinary)
    node.right.left = temp_var_access

    # теперь, проверим правую часть
    if node.right.right.res_type is None:  # это штуку может быть уже с анализирована(из-за прошлого _process_nested_comparison)
        analyze_rvalue(node.right.right, scope, node.right, errors)
    analyze_binary(node.right, scope, node, errors, False)

    # а теперь левая
    # если эта штука сравнение, и node.left - сравнение, то мы запускаем _process_nested_comparison ещё раз.
    if isinstance(node.left.left, TokenOperatorBinary) and \
        node.left.left.type in TokenOperatorsTypes.Comparison:
        _process_nested_comparison(node.left, scope, node, errors)
    else:
        # просто анализ
        # анализируем left.left (так как left.right уже с анализирована)
        analyze_rvalue(node.left.left, scope, node.left, errors)
        analyze_binary(node.left, scope, node, errors, False)

    # всё
    return t_bool


@analyze_rvalue.register(TokenOperatorBinary)
def analyze_binary(node: TokenOperatorBinary, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError],
                   analyze_things: bool = True) -> Type:
    # особый случай для цепочек сравнений
    if node.type in TokenOperatorsTypes.Comparison and \
            isinstance(node.left, TokenOperatorBinary) and \
            node.left.type in TokenOperatorsTypes.Comparison:
        return _process_nested_comparison(node, scope, parent, errors)

    # для _process_nested_comparison и не повторения кода
    if analyze_things:
        type_left = analyze_rvalue(node.left, scope, node, errors)
        type_right = analyze_rvalue(node.right, scope, node, errors)
        if type_left == t_error or type_right == t_error:
            return err(node)
    else:
        type_left = node.left.res_type
        type_right = node.right.res_type
        assert type_left is not None and type_right is not None

    type_need_left, type_need_right = get_common_type_binary(node.type, type_left, type_right, node.origin, errors)
    if type_need_left == t_error:
        return err(node)

    # обычная операция, кастим если нужно и всё
    if not type_left.is_simple_class_instance:
        node.left = cast_if_need(node.left, type_need_left)
        node.right = cast_if_need(node.right, type_need_right)
        node.res_type = get_result_type_binary(node.type, type_need_left, type_need_right)
        return node.res_type
    # если это класс, то мы используем один из его магических методов, так что заменим это всё на вызов
    else:
        cls = type_left.cls
        assert isinstance(cls, ControlClass)
        # получаем штуки
        magic_name, f_type, res_type = get_magic_thing_binary(node.type, type_left, type_right)
        # делаем новый код(вызов соответствующего метода)
        new_node = TokenOperatorFunctionCall(
            TokenOperatorFieldAccess(
                TokenVariableAccess(cls.name, node.origin, False, cls.class_var), magic_name,
                node.origin, f_type, cls.find_class_field(magic_name)
            ),
            [
                node.left, node.right
            ],
            node.origin, res_type
        )
        # меняем местами
        change_child(parent, node, new_node)
        return res_type


@analyze_rvalue.register(TokenOperatorPrefix)
def _(node: TokenOperatorPrefix, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node, errors)
    if type_have == t_error:
        return err(node)

    type_need = get_common_type_prefix(node.type, type_have, node.origin, errors)
    if type_need == t_error:
        return err(node)

    if not type_have.is_simple_class_instance:
        node.operand = cast_if_need(node.operand, type_need)
        node.res_type = get_result_type_prefix(node.type, type_need)
        return node.res_type
    else:
        cls = type_have.cls
        assert isinstance(cls, ControlClass)
        magic_name, f_type, res_type = get_magic_thing_prefix(node.type, type_have)
        new_node = TokenOperatorFunctionCall(
            TokenOperatorFieldAccess(
                TokenVariableAccess(cls.name, node.origin, False, cls.class_var), magic_name,
                node.origin, f_type, cls.find_class_field(magic_name)
            ),
            [node.operand],
            node.origin, res_type
        )
        change_child(parent, node, new_node)
        return res_type


@analyze_rvalue.register(TokenOperatorPostfix)
def _(node: TokenOperatorPostfix, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node, errors)
    if type_have == t_error:
        return err(node)

    type_need = get_common_type_postfix(node.type, type_have, node.origin)
    if type_need == t_error:
        return err(node)

    if not type_have.is_simple_class_instance:
        node.operand = cast_if_need(node.operand, type_need)
        node.res_type = get_result_type_postfix(node.type, type_need)
        return node.res_type
    else:
        cls = type_have.cls
        assert isinstance(cls, ControlClass)
        magic_name, f_type, res_type = get_magic_thing_prefix(node.type, type_have)
        new_node = TokenOperatorFunctionCall(
            TokenOperatorFieldAccess(
                TokenVariableAccess(cls.name, node.origin, False, cls.class_var),
                magic_name, node.origin, f_type, cls.find_class_field(magic_name)
            ),
            [node.operand],
            node.origin, res_type
        )
        change_child(parent, node, new_node)
        return res_type


@analyze_rvalue.register(TokenOperatorCast)
def _(node: TokenOperatorCast, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    node.cast_type = analyze_type(node.cast_type, scope, node.origin, errors)
    type_have = analyze_rvalue(node.operand, scope, node, errors)
    type_to = node.cast_type
    if type_have != type_to and not type_have.is_castable_explicitly(type_to):
        raise SemanticError(f'Тип {type_have} неприводим к типу {type_to}',
                            node.operand.origin + node.cast_type.origin)
    return type_to


@analyze_rvalue.register(TokenOperatorSizeof)
def _(node: TokenOperatorSizeof, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    node.type = analyze_type(node.type, scope, node.origin, errors)
    if node.type == t_error:
        return err(node)
    node.res_type = Type(Type.SimpleTypeBase(BaseTypes.int64), [])
    return node.res_type


@analyze_rvalue.register(TokenOperatorLenof)
def _(node: TokenOperatorLenof, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node, errors)
    if type_have == t_error:
        return err(node)

    if not (type_have.is_mod_array or type_have.is_mod_slize):
        errors.append(SemanticError(f'В lenof могут быть только массивы и срезы, дано: {type_have}', node.operand.origin))
        return err(node)
    node.res_type = Type(Type.SimpleTypeBase(BaseTypes.int64), [])
    return node.res_type


@analyze_rvalue.register(TokenOperatorSlize)
def _(node: TokenOperatorSlize, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    # операнд
    type_operand = analyze_rvalue(node.operand, scope, node, errors)
    if type_operand == t_error or type_operand.is_mod_usual:
        if type_operand != t_error:
            errors.append(SemanticError('Взять срез можно только от указателя|массива|среза', node.operand.origin))
        if node.position_start: 
            for i in node.position_start: 
                analyze_rvalue(i, scope, node, errors)
        if node.result_dimensions:
            for d in node.result_dimensions: 
                analyze_rvalue(d, scope, node, errors)
        return err(node)
    
    # позиция старта среза
    if node.position_start is not None:
        # проверка значений
        error_occurred = False
        for i, index in enumerate(node.position_start):
            t_index = analyze_rvalue(index, scope, node, errors)
            if t_index == t_error:
                error_occurred = True
                continue
            t_index_need = t_index.turn_into_int()

            if t_index_need is None:
                errors.append(SemanticError('Индексы в позиции старта среза должны быть целыми беззнаковыми числами',
                                            node.position_start[i].origin))
                error_occurred = True
                continue
            node.position_start[i] = cast_if_need(index, t_index_need)
            
        if error_occurred:
            if node.result_dimensions:
                for d in node.result_dimensions: 
                    analyze_rvalue(d, scope, node, errors)
            return err(node)
            
        # проверка размерности
        n = len(node.position_start)
        if type_operand.is_mod_pointer:
            n_need = 1
        else:
            n_need = type_operand.get_dims()
        if n != n_need:
            errors.append(SemanticError('Размерности позиции старта должны совпадать с размерностями срезаемого', node.origin))
            if node.result_dimensions:
                for d in node.result_dimensions: 
                    analyze_rvalue(d, scope, node, errors)
            return err(node)
    else:
        if type_operand.is_mod_pointer:
            n = 1
        else:
            n = type_operand.get_dims()
        # всё просто нули
        node.position_start = [
            TokenOperatorCast(Type(Type.SimpleTypeBase(BaseTypes.uint64), []),
                              TokenLiteral.from_raw(TokenRawLiteral('0', zero_origin)), zero_origin)
            for _ in range(n)
        ]

    # размерности среза
    if node.result_dimensions is not None:
        # проверка значений
        error_occurred = False
        for i, index in enumerate(node.result_dimensions):
            t_index = analyze_rvalue(index, scope, node, errors)
            if t_index == t_error:
                error_occurred = True
                continue
            t_index_need = t_index.turn_into_int()

            if t_index_need is None:
                errors.append(SemanticError('Размерности среза должны быть целыми беззнаковыми числами',
                                            node.result_dimensions[i].origin))
                error_occurred = True
                continue
            node.result_dimensions[i] = cast_if_need(index, t_index_need)
        if error_occurred:
            return err(node)
    else:
        if type_operand.is_mod_pointer:
            errors.append(SemanticError('Не указывать размерности при срезе указателя нельзя', node.origin))
            return err(node)
        else:
            dims = type_operand.get_dims()
            # делаем лесенку из lenof, чтобы скопировать размерности

            result_dimensions = [node.operand]
            # добавляем n_i = n_{i-1}[0]
            for _ in range(dims - 1):
                result_dimensions.append(
                    TokenOperatorIndex(
                        result_dimensions[-1],
                        TokenOperatorCast(Type(Type.SimpleTypeBase(BaseTypes.uint64), []),
                                          TokenLiteral.from_raw(TokenRawLiteral('0', zero_origin)), zero_origin),
                        node.origin,
                        result_dimensions[-1].res_type.without_one_dimension()
                    )
                )

            # и теперь всё в lenof(и в обратном порядке, чтобы lenof thing была последней размерностью, как и должно быть)
            result_dimensions = [
                TokenOperatorLenof(t, node.origin, types.int64) for t in result_dimensions[::-1]
            ]

            node.result_dimensions = result_dimensions

    # результат
    # срезаем модификатор
    res_type = type_operand
    if type_operand.is_mod_pointer or type_operand.is_mod_slize:
        res_type = res_type.without_one_modifier()
    elif type_operand.is_mod_array:
        while res_type.is_mod_array:
            res_type = res_type.without_one_modifier()
    # ставим свой
    node.res_type = res_type.add_modifier(Type.ModifierSlise(len(node.result_dimensions)))
    return node.res_type


@analyze_rvalue.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    if not isinstance(node.operand, TokenOperatorRvalueABC):
        errors.append(SemanticError('Для индекса, ожидаемого быть rvalue операнд тоже должен быть rvalue', node.operand.origin))
        analyze_wvalue(node.operand, scope, node, errors)
        analyze_rvalue(node.index, scope, node, errors)
        return err(node)

    type_operand = analyze_rvalue(node.operand, scope, node, errors)
    if type_operand == t_error or not (type_operand.is_mod_array or type_operand.is_mod_slize):
        if type_operand != t_error:
            errors.append(SemanticError(f'Индексировать можно только массивы и срезы, дано: {type_operand}', node.operand.origin))
        analyze_rvalue(node.index, scope, node, errors)
        return err(node)

    type_index = analyze_rvalue(node.index, scope, node, errors)
    type_index_need = type_index.turn_into_int()
    if type_index == t_error or type_index_need is None:
        if type_index != t_error:
            errors.append(SemanticError('Как индекс могут быть только целые положительные числа', node.index.origin))
        return err(node)

    node.index = cast_if_need(node.index, type_index_need)
    node.res_type = type_operand.without_one_dimension()
    return node.res_type


@analyze_rvalue.register(TokenOperatorArrayCreation)
def _(node: TokenOperatorArrayCreation, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    # берём все типы
    types = [analyze_rvalue(opr, scope, node, errors) for opr in node.operands]
    if any(t == t_error for t in types):
        return err(node)

    # ищём самый общий тип
    type_general = types[0]
    for i, t in zip(range(1, len(types)), types[1:]):
        type_general = get_common_type_array_creation(type_general, t, node.origin)
        if type_general is None:
            errors.append(SemanticError(f'Элементы в создании массива({type_general} и {t}) '
                                        f'должны быть приводимы друг к другу неявно', node.operands[i].origin))
            return err(node)

    # добавляем касты
    for i, t in enumerate(types):
        node.operands[i] = cast_if_need(node.operands[i], type_general)
    # тип результата
    node.res_type = type_general.add_modifier(Type.ModifierArray(len(types)))
    return node.res_type


@analyze_rvalue.register(TokenOperatorReferencing)
def _(node: TokenOperatorReferencing, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_operand = analyze_wvalue(node.operand, scope, node, errors)
    if type_operand == t_error:
        return err(node)
    node.res_type = type_operand.add_modifier(Type.ModifierPointer())
    return node.res_type


@analyze_rvalue.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node, errors)
    if type_operand == t_error:
        return err(node)
    if not type_operand.is_mod_pointer:
        errors.append(SemanticError('Операнд разыменования должен быть указателем', node.operand.origin))
        return err(node)
    node.res_type = type_operand.without_one_modifier()
    return node.res_type


def find_class_name(type: Type, class_: ControlClass, name: str, origin: TokenOrigin, errors: list[SemanticError]) -> \
        TokenOperatorVariableDefinition | ControlFunctionDefinition | None:
    if type.is_simple_class:
        field_ = class_.find_class_field(name)
        if field_ is None:
            errors.append(SemanticError(f'Имени "{name}" нет в классе "{class_.name}"', origin))
            return
    else:
        field_ = class_.find_instance_field(name)
        if field_ is None:
            field_ = class_.find_class_field(name)
            if field_ is None:
                errors.append(SemanticError(f'Имени "{name}" нет ни в полях экзепляра '
                                            f'класса "{class_.name}", ни в его полях', origin))
                return

    return field_


@analyze_rvalue.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node, errors)
    _type_operand = type_operand.full_type
    
    # ветка перечисления
    if _type_operand.is_simple_enum:
        enum: ControlEnum = _type_operand.enum
        status = enum.find_var(node.name)
        if status is None:
            errors.append(SemanticError(f'Статуса и именем "{node.name}" не обнаружено.', node.origin))
            return err(node)
        node.res_type = status.type
        node.field = status
        return node.res_type

    # ветка класса
    if not ((_type_operand.is_simple_class_instance or _type_operand.is_simple_class) and _type_operand.is_mod_usual):
        errors.append(SemanticError(f'Операнд доступа к полю должен быть или классом, или его экземпляром, или перечислением. Дано {type_operand}', node.operand.origin))
        return err(node)

    class_ = _type_operand.cls
    assert isinstance(class_, ControlClass)

    field_ = find_class_name(_type_operand, class_, node.name, node.origin, errors)
    if field_ is None:
        return err(node)

    if isinstance(field_, ControlFunctionDefinition):
        node.res_type = field_.var.type
        node.field = field_.var
        return field_.var.type
    node.res_type = field_.type
    node.field = field_
    return field_.type


@analyze_rvalue.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node, errors)
    _type_operand = type_operand.full_type

    if not ((_type_operand.is_simple_class_instance or _type_operand.is_simple_class) and _type_operand.is_mod_pointer and len(_type_operand.modifiers) == 1):
        errors.append(SemanticError(f'Операнд доступа к полю указателя должен быть указателем на '
                                    f'классом, или его экземпляр, дано {type_operand}', node.operand.origin))
        return err(node)

    class_ = _type_operand.cls
    assert isinstance(class_, ControlClass)

    field_ = find_class_name(_type_operand, class_, node.name, node.origin, errors)
    if field_ is None:
        return err(node)

    if isinstance(field_, ControlFunctionDefinition):
        node.res_type = field_.var.type
        node.field = field_.var
        return field_.var.type
    node.res_type = field_.type
    node.field = field_
    return field_.type


@analyze_rvalue.register(TokenOperatorDeInitializer)
def _(node: TokenOperatorDeInitializer, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    if not isinstance(parent, ControlExpression):
        errors.append(SemanticError('Оператор де инициализации может быть только в начале обычных '
                                    'выражений(управляющих конструкций) т.к. ничего не возвращает', node.origin))
        return err(node)

    # обработаем де инициализацию
    operand_type = analyze_rvalue(node.operand, scope, node, errors)
    if operand_type == t_error:
        return err(node)
    operand_type_ = operand_type.full_type

    if not operand_type_.is_simple_class_instance:
        errors.append(SemanticError('Операндом де инициализации должен быть экземпляром класса', node.operand.origin))
        return err(node)
    if operand_type_.is_mod_pointer and len(operand_type_.modifiers) != 1:
        errors.append(SemanticError(f'Операнд де инициализации в случае указателя требует '
                            f'только 1 вложенности, было дано {len(operand_type_.modifiers)}', node.operand.origin))
        return err(node)
    elif operand_type_.is_mod_slize and len(operand_type_.modifiers) != 1:
        errors.append(SemanticError(f'Операнд де инициализации в случае среза требует только срез(любой размерности) '
                            f'указывающий на экземпляр класса, было дано: {operand_type}', node.operand.origin))
        return err(node)
    elif operand_type_.is_mod_array:
        opt = operand_type_.copy()
        while opt.is_mod_array:
            opt = opt.without_one_modifier()
        if not opt.is_mod_usual:
            errors.append(SemanticError(f'Операнд де инициализации в случае массива(многомерного или нет) требует, '
                                f'чтобы финальным элементом был экземпляр класса, дано: {operand_type}',
                                node.operand.origin))
            return err(node)

    node.res_type = operand_type
    return operand_type


@analyze_rvalue.register(TokenOperatorError)
def _(node: TokenOperatorError, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return t_error
