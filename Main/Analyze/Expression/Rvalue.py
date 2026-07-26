from ..Simple import *
from ..Types import *
from ....Definitions.Scopes import *
from ....Definitions.Tokens import *
from ....Definitions.Exceptions import SemanticError
from ....Definitions import TypesShortener as types
from .Utils import *


__all__ = ('analyze_rvalue',)


@analyze_rvalue.register(TokenVariableAccess)
def _(node: TokenVariableAccess, scope: Scope, parent: TypeExpressionParent) -> Type:
    r = scope.find_variable(node.name, True)
    if r is None:
        raise SemanticError(f'Попытка чтения из необъявленной переменной "{node.name}"', node.origin)
    var, is_nonlocal = r
    node.is_nonlocal = is_nonlocal
    node.var_def = var
    return var.type


@analyze_rvalue.register(TokenLiteral)
def _(node: TokenLiteral, scope: Scope, parent: TypeExpressionParent) -> Type:
    return node.res_type


@analyze_rvalue.register(TokenOperatorAssignment)
def _(node: TokenOperatorAssignment, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_have = analyze_rvalue(node.right, scope, node)
    type_need = analyze_wvalue(node.left, scope, node)
    if type_have != type_need and not type_have.is_castable_implicitly(type_need):
        raise SemanticError(
            f'Тип {type_have} не может быть неявно приведён к типу {type_need} для присваивания.',
            node.left.origin + node.right.origin
        )
    node.right = cast_if_need(node.right, type_need)
    node.res_type = type_need
    return type_need


@analyze_rvalue.register(TokenOperatorFunctionCall)
def analyze_fcall(node: TokenOperatorFunctionCall, scope: Scope, parent: TypeExpressionParent) -> Type:
    func_type = analyze_rvalue(node.func, scope, node)
    _func_type = func_type.full_type

    # это вызов класса(то есть, создание экзепляра)
    if _func_type.is_simple_class and _func_type.is_mod_usual:
        # меняем класс на обращение к полю "__init__" класса
        cls = _func_type.cls
        init = cls.find_class_field('__init__')
        if init is None:
            raise SemanticError(f'Класс {cls.name} не имеет метода __init__', cls.origin)
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
            raise SemanticError('Попытка вызова экзепляра класса без определённого метода __call__', node.func.origin)
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
        raise SemanticError(f'Для использовании в вызове функции тип вызываемого должен '
                            f'быть функцией, дано {func_type}', node.func.origin)

    if not _func_type.is_mod_usual:
        raise SemanticError(f'Для использовании в вызове функции тип вызываемого должен '
                            f'быть чистой функцией без модификаторов, дана {func_type}', node.func.origin)

    # проверим, вызывается ли это нечто от экземпляра класса
    skip_check_first_arg = False
    if isinstance(node.func, (TokenOperatorFieldAccess, TokenOperatorFieldAccessPointer)):
        if node.func.operand.res_type.is_simple_class_instance:
            skip_check_first_arg = True
            # если это не указатель, а нам нужен указатель, то мы возьмём адрес
            if node.func.operand.res_type.is_mod_usual and \
                    len(_func_type.simple.arguments) >= 1 and \
                    not _func_type.simple.arguments[0].is_mod_usual and \
                    _func_type.simple.arguments[0].without_one_modifier() == node.func.operand.res_type:
                # проверка, что это wvalue(хотя, она немного вызывает сомнения)
                if not isinstance(node.func.operand, TokenOperatorWvalueABC):
                    raise SemanticError('Ожидалось wvalue(для неявной передачи указателя на экземпляр)', node.func.operand.origin)
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
            raise SemanticError('Функции, не возвращающие значения, могут быть только в начале '
                                'обычного выражения(управляющей конструкции)', node.origin)
    # функции со множественным результатом могут быть только в выражениях и множественных присваиваниях
    if res_num > 1:
        raise SemanticError('Функции, возвращающие больше 1 значения, могут быть только в начале '
                            'обычных выражений и массовых присваиваниях', node.origin)

    # проверка параметров
    args_num = len(func.arguments)
    if len(node.arguments) != args_num:
        raise SemanticError(f"Функция типа {func_type} ожидает {args_num} аргументов, "
                            f"передано {len(node.arguments)}", node.origin)

    # сама поэлементная проверка
    for i, (arg, type_need) in enumerate(zip(node.arguments, func.arguments)):
        if skip_check_first_arg and i == 0:
            type_have = arg.res_type # чтобы не анализировать 2 раза и добавлять штуки по 2 раза
        else:
            type_have = analyze_rvalue(arg, scope, node)
        arg = node.arguments[i]

        if type_need != type_have and not type_have.is_castable_implicitly(type_need):
            raise SemanticError(
                f'Тип {type_have} неявно неприводим к типу {type_need} для передачи '
                f'как {i} аргумент функции типа {func_type}', arg.origin
            )
        node.arguments[i] = cast_if_need(arg, type_need)

    if res_num == 1:
        node.res_type = func.results[0]
        return node.res_type
    else:
        # хотя, это нужно для обработки массового присваивания
        node.res_type = _func_type
        return _func_type


NESTED_VARS_COUNTER = 0


def _process_nested_comparison(node: TokenOperatorBinary, scope: Scope, parent: TypeExpressionParent) -> Type:
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
    analyze_rvalue(node.left.right, scope, node.right)

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
        analyze_rvalue(node.right.right, scope, node.right)
    analyze_binary(node.right, scope, node, False)

    # а теперь левая
    # если эта штука сравнение, и node.left - сравнение, то мы запускаем _process_nested_comparison ещё раз.
    if isinstance(node.left.left, TokenOperatorBinary) and \
        node.left.left.type in TokenOperatorsTypes.Comparison:
        _process_nested_comparison(node.left, scope, node)
    else:
        # просто анализ
        # анализируем left.left (так как left.right уже с анализирована)
        analyze_rvalue(node.left.left, scope, node.left)
        analyze_binary(node.left, scope, node, False)

    # всё
    return t_bool


@analyze_rvalue.register(TokenOperatorBinary)
def analyze_binary(node: TokenOperatorBinary, scope: Scope, parent: TypeExpressionParent, analyze_things: bool = True) -> Type:
    # особый случай для цепочек сравнений
    if node.type in TokenOperatorsTypes.Comparison and \
            isinstance(node.left, TokenOperatorBinary) and \
            node.left.type in TokenOperatorsTypes.Comparison:
        return _process_nested_comparison(node, scope, parent)

    # для _process_nested_comparison и не повторения кода
    if analyze_things:
        type_left = analyze_rvalue(node.left, scope, node)
        type_right = analyze_rvalue(node.right, scope, node)
    else:
        type_left = node.left.res_type
        type_right = node.right.res_type
        assert type_left is not None and type_right is not None
    type_need_left, type_need_right = get_common_type_binary(node.type, type_left, type_right, node.origin)

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
def _(node: TokenOperatorPrefix, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node)
    type_need = get_common_type_prefix(node.type, type_have, node.origin)
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
def _(node: TokenOperatorPostfix, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node)
    type_need = get_common_type_postfix(node.type, type_have, node.origin)
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
def _(node: TokenOperatorCast, scope: Scope, parent: TypeExpressionParent) -> Type:
    analyze_type(node.cast_type, scope, node.origin)
    type_have = analyze_rvalue(node.operand, scope, node)
    type_to = node.cast_type
    if type_have != type_to and not type_have.is_castable_explicitly(type_to):
        raise SemanticError(f'Тип {type_have} неприводим к типу {type_to}',
                            node.operand.origin + node.cast_type.origin)
    return type_to


@analyze_rvalue.register(TokenOperatorSizeof)
def _(node: TokenOperatorSizeof, scope: Scope, parent: TypeExpressionParent) -> Type:
    analyze_type(node.type, scope, node.origin)
    node.res_type = Type(Type.SimpleTypeBase(BaseTypes.int64), [])
    return node.res_type


@analyze_rvalue.register(TokenOperatorLenof)
def _(node: TokenOperatorLenof, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_have = analyze_rvalue(node.operand, scope, node)
    if not (type_have.is_mod_array or type_have.is_mod_slize):
        raise SemanticError(f'В lenof могут быть только массивы и срезы, дано: {type_have}', node.operand.origin)
    node.res_type = Type(Type.SimpleTypeBase(BaseTypes.int64), [])
    return node.res_type


@analyze_rvalue.register(TokenOperatorSlize)
def _(node: TokenOperatorSlize, scope: Scope, parent: TypeExpressionParent) -> Type:
    # операнд
    type_operand = analyze_rvalue(node.operand, scope, node)
    if type_operand.is_mod_usual:
        raise SemanticError('Взять срез можно только от указателя|массива|среза', node.operand.origin)

    # позиция старта среза
    if node.position_start is not None:
        # проверка размерности
        n = len(node.position_start)
        if type_operand.is_mod_pointer:
            n_need = 1
        else:
            n_need = type_operand.get_dims()
        if n != n_need:
            raise SemanticError('Размерности позиции старта должны совпадать с размерностями срезаемого', node.origin)
        # проверка значений
        for i, index in enumerate(node.position_start):
            t_index = analyze_rvalue(index, scope, node)
            t_index_need = t_index.turn_into_int()
            if t_index_need is None:
                raise SemanticError('Индексы в позиции старта среза должны быть целыми беззнаковыми числами',
                                    node.position_start[i].origin)
            node.position_start[i] = cast_if_need(index, t_index_need)
    else:
        if type_operand.is_mod_pointer:
            n = 1
        else:
            n = type_operand.get_dims()
        node.position_start = [
            TokenOperatorCast(Type(Type.SimpleTypeBase(BaseTypes.uint64), []),
                              TokenLiteral.from_raw(TokenRawLiteral('0', zero_origin)), zero_origin)
            for _ in range(n)
        ]

    # размерности среза
    if node.result_dimensions is not None:
        # проверка значений
        for i, index in enumerate(node.result_dimensions):
            t_index = analyze_rvalue(index, scope, node)
            t_index_need = t_index.turn_into_int()
            if t_index_need is None:
                raise SemanticError('Размерности среза должны быть целыми беззнаковыми числами',
                                    node.result_dimensions[i].origin)
            node.result_dimensions[i] = cast_if_need(index, t_index_need)
    else:
        if type_operand.is_mod_pointer:
            raise SemanticError('Не указывать размерности при срезе указателя нельзя', node.origin)
        else:
            dims = type_operand.get_dims()
            # делаем лесенку из lenof, чтобы скопировать размерности
            def get_nth_index(n: int, _type: Type):
                if n == 0:
                    return node.operand
                return TokenOperatorIndex(
                    get_nth_index(n-1, type_operand.without_one_dimension()),
                    TokenOperatorCast(Type(Type.SimpleTypeBase(BaseTypes.uint64), []),
                                      TokenLiteral.from_raw(TokenRawLiteral('0', zero_origin)), zero_origin),
                    zero_origin,
                    type_operand # тип указываем сами
                )
            node.result_dimensions = [
                TokenOperatorLenof(get_nth_index(n, type_operand.without_one_dimension()), zero_origin, types.int64)
                for n in range(dims)
            ]

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
def _(node: TokenOperatorIndex, scope: Scope, parent: TypeExpressionParent) -> Type:
    if not isinstance(node.operand, TokenOperatorRvalueABC):
        raise SemanticError('Для индекса, ожидаемого быть rvalue операнд тоже должен быть rvalue', node.operand.origin)
    type_operand = analyze_rvalue(node.operand, scope, node)
    if not (type_operand.is_mod_array or type_operand.is_mod_slize):
        raise SemanticError(f'Индексировать можно только массивы и срезы, дано: {type_operand}', node.operand.origin)
    type_index = analyze_rvalue(node.index, scope, node)
    type_index_need = type_index.turn_into_int()
    if type_index_need is None:
        raise SemanticError('Как индекс могут быть только целые положительные числа', node.index.origin)
    node.index = cast_if_need(node.index, type_index_need)
    node.res_type = type_operand.without_one_dimension()
    return node.res_type


@analyze_rvalue.register(TokenOperatorArrayCreation)
def _(node: TokenOperatorArrayCreation, scope: Scope, parent: TypeExpressionParent) -> Type:
    # берём все типы
    types = [analyze_rvalue(opr, scope, node) for opr in node.operands]
    # ищём самый общий тип
    type_general = types[0]
    for i, t in zip(range(1, len(types)), types[1:]):
        type_general = get_common_type_array_creation(type_general, t, node.origin)
        if type_general is None:
            raise SemanticError('Элементы в создании массива должны быть приводимы друг к '
                                'другу неявно', node.operands[i].origin)
    # добавляем касты
    for i, t in enumerate(types):
        node.operands[i] = cast_if_need(node.operands[i], type_general)
    # тип результата
    node.res_type = type_general.add_modifier(Type.ModifierArray(len(types)))
    return node.res_type


@analyze_rvalue.register(TokenOperatorReferencing)
def _(node: TokenOperatorReferencing, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_operand = analyze_wvalue(node.operand, scope, node)
    node.res_type = type_operand.add_modifier(Type.ModifierPointer())
    return node.res_type


@analyze_rvalue.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node)
    if not type_operand.is_mod_pointer:
        raise SemanticError('Операнд разыменования должен быть указателем', node.operand.origin)
    node.res_type = type_operand.without_one_modifier()
    return node.res_type


def find_class_name(type: Type, class_: ControlClass, name: str, origin: TokenOrigin
                    ) -> TokenOperatorVariableDefinition | ControlFunctionDefinition:
    if type.is_simple_class:
        field_ = class_.find_class_field(name)
        if field_ is None:
            raise SemanticError(f'Имени "{name}" нет в классе "{class_.name}"', origin)
    else:
        field_ = class_.find_instance_field(name)
        if field_ is None:
            field_ = class_.find_class_field(name)
            if field_ is None:
                raise SemanticError(f'Имени "{name}" нет ни в полях экзепляра '
                                    f'класса "{class_.name}", ни в его полях', origin)

    return field_


@analyze_rvalue.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node)
    _type_operand = type_operand.full_type
    
    # ветка перечисления
    if _type_operand.is_simple_enum:
        enum: ControlEnum = _type_operand.enum
        status = enum.find_var(node.name)
        if status is None:
            raise SemanticError(f'Статуса и именем "{node.name}" не обнаружено.', node.origin)
        node.res_type = status.type
        node.field = status
        return node.res_type

    # ветка класса
    if not ((_type_operand.is_simple_class_instance or _type_operand.is_simple_class) and _type_operand.is_mod_usual):
        raise SemanticError(f'Операнд доступа к полю должен быть или классом, или его экземпляром, или перечислением дано {type_operand}', node.operand.origin)
    
    class_ = _type_operand.cls
    assert isinstance(class_, ControlClass)

    field_ = find_class_name(_type_operand, class_, node.name, node.origin)

    if isinstance(field_, ControlFunctionDefinition):
        node.res_type = field_.var.type
        node.field = field_.var
        return field_.var.type
    node.res_type = field_.type
    node.field = field_
    return field_.type


@analyze_rvalue.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, scope: Scope, parent: TypeExpressionParent) -> Type:
    type_operand = analyze_rvalue(node.operand, scope, node)
    _type_operand = type_operand.full_type

    if not ((_type_operand.is_simple_class_instance or _type_operand.is_simple_class) and _type_operand.is_mod_pointer and len(_type_operand.modifiers) == 1):
        raise SemanticError(f'Операнд доступа к полю указателя должен быть указателем на классом, или его экземпляр, дано {type_operand}', node.operand.origin)
    class_ = _type_operand.cls
    assert isinstance(class_, ControlClass)

    field_ = find_class_name(_type_operand, class_, node.name, node.origin)

    if isinstance(field_, ControlFunctionDefinition):
        node.res_type = field_.var.type
        node.field = field_.var
        return field_.var.type
    node.res_type = field_.type
    node.field = field_
    return field_.type


@analyze_rvalue.register(TokenOperatorDeInitializer)
def _(node: TokenOperatorDeInitializer, scope: Scope, parent: TypeExpressionParent) -> Type:
    if not isinstance(parent, ControlExpression):
        raise SemanticError('Оператор де инициализации может быть только в начале обычных '
                            'выражений(управляющих конструкций) т.к. ничего не возвращает', node.origin)

    # обработаем де инициализацию
    operand_type = analyze_rvalue(node.operand, scope, node)
    operand_type_ = operand_type.full_type

    if not operand_type_.is_simple_class_instance:
        raise SemanticError('Операндом де инициализации должен быть экземпляром класса', node.operand.origin)
    if operand_type_.is_mod_pointer and len(operand_type_.modifiers) != 1:
        raise SemanticError(f'Операнд де инициализации в случае указателя требует '
                            f'только 1 вложенности, было дано {len(operand_type_.modifiers)}', node.operand.origin)
    elif operand_type_.is_mod_slize and len(operand_type_.modifiers) != 1:
        raise SemanticError(f'Операнд де инициализации в случае среза требует только срез(любой размерности) '
                            f'указывающий на экземпляр класса, было дано: {operand_type}', node.operand.origin)
    elif operand_type_.is_mod_array:
        opt = operand_type_.copy()
        while opt.is_mod_array:
            opt = opt.without_one_modifier()
        if not opt.is_mod_usual:
            raise SemanticError(f'Операнд де инициализации в случае массива(многомерного или нет) требует, '
                                f'чтобы финальным элементом был экземпляр класса, дано: {operand_type}',
                                node.operand.origin)

    node.res_type = operand_type
    return operand_type


