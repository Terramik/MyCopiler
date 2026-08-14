from .Simple import *
from .Expression import *
from ...Definitions.Scopes import *
from ...Definitions.Tokens import *
from ...Definitions.Exceptions import SemanticError
from ...Definitions.Enums import magic_methods
from ...Definitions import TypesShortener as types
from ..Transform import post_analyze_transforms


def analyze_expression(scope: Scope, expr: ControlExpression, errors: list[SemanticError]):
    # тут может быть 4 случая - объявление переменной, де инициализация, вызов функции с числом параметров
    # в не 1(если это не часть выражения, так делать можно), или обычное выражение

    first = expr.first
    if isinstance(first, TokenOperatorRvalueABC):
        analyze_rvalue(first, scope, expr, errors)
    #     # обработаем де инициализацию
    #     operand_type = analyze_rvalue(first.operand, scope, first)
    #     operand_type_ = operand_type.full_type
    #
    #     if not operand_type_.is_simple_class_instance:
    #         raise SemanticError('Операндом де инициализации должен быть экземпляром класса', first.operand.origin)
    #     if operand_type_.is_mod_pointer and len(operand_type_.modifiers) != 1:
    #         raise SemanticError(f'Операнд де инициализации в случае указателя требует '
    #                             f'только 1 вложенности, было дано {len(operand_type_.modifiers)}', first.operand.origin)
    #     elif operand_type_.is_mod_slize and len(operand_type_.modifiers) != 1:
    #         raise SemanticError(f'Операнд де инициализации в случае среза требует только срез(любой размерности) '
    #                             f'указывающий на экземпляр класса, было дано: {operand_type}', first.operand.origin)
    #     elif operand_type_.is_mod_array:
    #         opt = operand_type_.copy()
    #         while opt.is_mod_array:
    #             opt = opt.without_one_modifier()
    #         if not opt.is_mod_usual:
    #             raise SemanticError(f'Операнд де инициализации в случае массива(многомерного или нет) требует, '
    #                                 f'чтобы финальным элементом был экземпляр класса, дано: {operand_type}', first.operand.origin)
    #
    # elif isinstance(first, TokenOperatorVariableDefinition):
    else:
        analyze_wvalue(first, scope, expr, errors)


def analyze_return(scope: Scope, ret: ControlReturn, errors: list[SemanticError]):
    func_scope = scope.find_scope_type(scope.Types.Function)
    if func_scope is None:
        errors.append(SemanticError('return все функции', ret.origin)) # пускай это и маловероятно
        for r in ret.results: analyze_rvalue(r, scope, ret, errors)
        ret.is_bad = True
        return

    func = func_scope.creator

    if func.is_bad:
        for r in ret.results: analyze_rvalue(r, scope, ret, errors)
        ret.is_bad = True
        return

    if len(func.results) != len(ret.results):
        errors.append(SemanticError('Количество аргументов в return не соответствуют количеству результатов функции', ret.origin))
        for r in ret.results: analyze_rvalue(r, scope, ret, errors)
        ret.is_bad = True
        return

    for i, t_need, t_have in (
        ((i, func.results[i], analyze_rvalue(ret.results[i], scope, ret, errors)) for i in range(len(func.results)))
    ):
        if t_have == t_error:
            continue
        if t_need != t_have:
            _is = t_have.is_castable_implicitly(t_need)

            if not _is:
                errors.append(SemanticError(f'Тип {t_have} неприводим к типу {t_need} для возвращения из '
                                            f'функции как {i} результат', ret.results[i].origin))
                ret.is_bad = True
                continue
            cast = TokenOperatorCast(t_need, ret.results[i], ret.results[i].origin)
            ret.results[i] = cast
    ret.func = func


def analyze_mass_assignment(scope: Scope, mass: ControlMassAssignment, errors: list[SemanticError]):
    # проверим левые части
    types_left: list[Type] = []
    for l in mass.left:
        types_left.append(analyze_wvalue(l, scope, mass, errors))
    # и правые
    for r in mass.right:
        analyze_rvalue(r, scope, mass, errors)
    # и проверка
    if any(l.res_type == t_error for l in mass.left) or any(r.res_type == t_error for r in mass.left):
        mass.is_bad = True
        return

    # подсчитаем мощности и получим функции/типы правой части, проанализировав её
    power_left = len(mass.left)
    types_right: [Type | list[Type]] = []
    power_right = 0
    for r in mass.right:
        if isinstance(r, TokenOperatorFunctionCall):
            func = r.res_type.simple
            res_num = len(func.results)
            if res_num == 0:
                errors.append(SemanticError('Функции, не возвращающие результатов, не могут '
                                            'быть использованы в массовом присваивании', r.origin))
                mass.is_bad = True
                return
            if res_num == 1:
                r.res_type = func.results[0]
            power_right += res_num
            types_right.append(func.results)
        else:
            types_right.append(r.res_type)
            power_right += 1

    if power_left != power_right:
        errors.append(SemanticError('Мощность левой части не соответствует мощности правой', mass.origin))
        mass.is_bad = True
        return

    # сделаем Inner массового присваивания
    results = []
    cur_left_i = 0

    error_occured = False

    for i, types_have, r in (
        ((i, types_right[i], mass.right[i]) for i in range(len(mass.right)))
    ):
        if isinstance(types_have, Type):
            # это просто rvalue мощьностью в 1
            t_have = types_have
            t_need = types_left[cur_left_i]
            if t_need != t_have:
                _is = t_have.is_castable_implicitly(t_need)
                if not _is:
                    errors.append(SemanticError(f'Тип {t_have} неприводим к типу {t_need} для '
                                                f'массового присваивания к {cur_left_i}', mass.origin))
                    error_occured = True
                    continue
            # создадим штуку
            results.append(ControlMassAssignment.Inner(
                r, [cur_left_i], [None if t_need == t_have else t_need]
            ))
            cur_left_i += 1
        else:
            # это функция
            # проверим типы
            num = len(types_have)
            types_need = types_left[cur_left_i:cur_left_i + num]
            wvalues = list(range(cur_left_i, cur_left_i + num))
            types_inner = []
            for ii, h, n, in (
                ((i, types_have[i], types_need[i]) for i in range(num))
            ):
                if h != n:
                    _is = h.is_castable_implicitly(n)
                    if not _is:
                        errors.append(SemanticError(f'Тип {h} неприводим к типу {n} для массового '
                                                    f'присваивания в {cur_left_i + ii}', mass.origin))
                        continue
                    types_inner.append(n)
                else:
                    types_inner.append(None)
            cur_left_i += num
            results.append((ControlMassAssignment.Inner(
                r, wvalues, types_inner
            )))

    if error_occured:
        mass.is_bad = True
        return

    mass.processed = results


def analyze_cycle_control(scope: Scope, cont: ControlCycleControl, errors: list[SemanticError]):
    cycle_scope = scope.find_scope_type(scope.Types.Cycle)
    if cycle_scope is None:
        errors.append(SemanticError('Конструкция управления циклом вне цикла', cont.origin))
        return


def analyze_typedef(scope: Scope, typedef: ControlTypedef, errors: list[SemanticError]):
    name = typedef.typedef.name
    type = analyze_type(typedef.typedef.type, scope, typedef.typedef.type.origin, errors)
    if type == t_error:
        typedef.typedef = Type.Typedef(t_error, name)
        return
    typedef.typedef = Type.Typedef(type, name)
    if is_in_key_word(name):
        errors.append(SemanticError('Имя псевдонима не может быть ключевым словом', typedef.origin))
        return
    if scope.is_name_occupied(name, False):
        errors.append(SemanticError(f'Имя "{name}" уже занято в это области видимости для создания псевдонима', typedef.origin))
        return
    scope.add_typedef(typedef)


def analyze_import(scope: Scope, import_: ControlImport, errors: list[SemanticError]):
    if not import_.is_allowed:
        errors.append(SemanticError('Импорты разрешены только в начале файла друг за другом', import_.origin))


def analyze_export(scope: Scope, export: ControlExport, errors: list[SemanticError]):
    if scope.type != Scope.Types.Global:
        errors.append(SemanticError('Экспорты разрешены только в глобальной области видимости', export.origin))


def analyze_code_block(scope: Scope, block: ControlCodeBlock, errors: list[SemanticError]):
    raise NotImplemented('')


def analyze_function(scope: Scope, func: ControlFunctionDefinition, errors: list[SemanticError]):
    error_occured = False

    # свободно ли имя
    name = func.name
    if is_in_key_word(func.name):
        errors.append(SemanticError(f'Имя функции "{func.name}" не может быть ключевым словом', func.origin))
        error_occured = True
    else:
        if scope.is_name_occupied(name, False):
            errors.append(SemanticError(f'Имя для функции "{func.name}" уже занято в данной области видимости', func.origin))
            error_occured = True

    # делаем вложенный скоп и добавляем штуки
    child_scope = Scope(Scope.Types.Function, func, scope)
    scope.add_child(child_scope)
    scope.add_function(func)

    # проверяем и анализируем
    for par in func.parameters:
        assert isinstance(par, TokenOperatorVariableDefinition)
        analyze_wvalue(par, child_scope, func, errors)
        child_scope.add_variable(par)

    func.results = [
        analyze_type(t, scope, t.origin, errors)
        for t in func.results
    ]

    if any(par.res_type == t_error for par in func.parameters) or any(t == t_error for t in func.results):
        error_occured = True
    # добавим переменную, в которой лежит собственно наша функция
    func_var = TokenOperatorVariableDefinition(name, Type(Type.SimpleTypeFunc(
        [arg.type for arg in func.parameters],
        func.results[::]
    ),
        []), func.origin)
    scope.add_variable(func_var)
    func.var = func_var
    # проверяем остальные штуки
    analyze_code_block(child_scope, func.code_block, errors)
    if error_occured:
        func.is_bad = True


def analyze_if(scope: Scope, if_: ControlIf, errors: list[SemanticError]):
    # условия
    condition_t = analyze_rvalue(if_.condition, scope, if_, errors)
    # если не bool, то пытаемся привести к нему
    if condition_t != t_bool:
        if condition_t == t_error:
            if_.is_bad = True
        elif not condition_t.is_castable_implicitly(t_bool):
            errors.append(SemanticError('Условие не является типом bool и не может быть '
                                        'неявно к нему приведено', if_.origin))
            if_.is_bad = True
        else:
            if_.condition = TokenOperatorCast(
                t_bool, if_.condition, zero_origin
            )

    # сами блоки if/else
    child_scope_if = Scope(Scope.Types.Conditional, (if_, if_.block_if), scope)
    scope.add_child(child_scope_if)
    analyze_code_block(child_scope_if, if_.block_if, errors)

    child_scope_else = Scope(Scope.Types.Conditional, (if_, if_.block_else), scope)
    scope.add_child(child_scope_else)
    analyze_code_block(child_scope_else, if_.block_else, errors)


def analyze_while(scope: Scope, _while: ControlWhile, errors: list[SemanticError]):
    # проверяем условие
    _type = analyze_rvalue(_while.condition, scope, _while, errors)
    if _type != t_bool:
        if _type == t_error:
            _while.is_bad = True
        elif not _type.is_castable_implicitly(t_bool):
            errors.append(SemanticError('Условие не является типом bool и не может быть '
                                        'неявно к нему приведено', _while.condition.origin))
            _while.is_bad = True
        else:
            c = TokenOperatorCast(t_bool, _while.condition, zero_origin)
            _while.condition = c
    # делаем скоп и проверяем блок
    child_scope = Scope(Scope.Types.Cycle, _while, scope)
    scope.add_child(child_scope)
    analyze_code_block(child_scope, _while.code_block, errors)


def analyze_class(scope: Scope, cls: ControlClass, errors: list[SemanticError]):
    # свободно ли имя
    name = cls.name
    if is_in_key_word(name):
        errors.append(SemanticError(f'Имя для класса "{cls.name}" не может быть ключевым словом', cls.origin))
        cls.is_bad = True
    else:
        if scope.is_name_occupied(name, False):
            errors.append(SemanticError(f'Имя для класса "{cls.name}" уже занято в данной области видимости', cls.origin))
            cls.is_bad = True

    # делаем вложенный скоп и добавляем штуки
    child_scope = Scope(Scope.Types.Class, cls, scope)
    scope.add_child(child_scope)
    scope.add_class(cls)
    # классовая переменная, чтобы работал MyClass(), Myclass.class_var и т.д.
    cls.class_var = TokenOperatorVariableDefinition(
        cls.name, Type(Type.SimpleTypeClass(cls), []), cls.origin
    )
    scope.add_variable(cls.class_var)
    cls.scope = child_scope

    # проверим поля экземпляра
    zero_scope = Scope(Scope.Types.Global, cls, scope) # у полей экзепляра своя собственная область видимости
    for field_ in cls.instance_field:
        analyze_wvalue(field_, zero_scope, cls, errors)
    if any(field_.res_type == t_error for field_ in cls.instance_field):
        cls.is_bad = True

    class_instance_type = Type(
        Type.SimpleTypeClassInstance(cls), []
    )
    # проверим все штуки в классе
    for control in cls.rest.block_parts:
        match control:
            case ControlFunctionDefinition():
                assert isinstance(control, ControlFunctionDefinition)
                analyze_function(child_scope, control, errors)
                if control.is_bad:
                    continue

                # магический, его тип должен соответствовать особому
                if control.name in magic_methods:
                    if len(cls.instance_field) == 0:
                        errors.append(SemanticError('Экземпляр класса без полей не может существовать, следовательно, '
                                                    'магические методы для них существовать тоже не могут.', control.origin))
                        continue
                    f_type = control.var.type.simple
                    assert isinstance(f_type, Type.SimpleTypeFunc)
                    match control.name:
                        case '__init__':
                            if not (
                                len(f_type.results) == 1 and
                                f_type.results[0] == class_instance_type and
                                len(f_type.arguments) >= 1 and
                                f_type.arguments[0] == class_instance_type
                            ):
                                errors.append(SemanticError(f'Тип магического метода __init__ должен соответствовать '
                                                            f'func(Class, <любые прочие аргументы>) -> (Class). Было дано: {f_type}', control.origin))
                                continue
                            # добавим имя в функцию
                            control.is_class_init = control.parameters[0].name
                            # теперь, уберём self из аргументов, так как это скорее для нотации
                            control.parameters = control.parameters[1:]
                            control.var.type = Type(
                                Type.SimpleTypeFunc(
                                    f_type.arguments[1:], f_type.results
                                ), control.var.type.modifiers
                            )

                        case '__add__' | '__sub__' | '__mul__' | '__div__' | '__mod__':
                            if not f_type == types.func([class_instance_type, class_instance_type], [class_instance_type]).simple:
                                errors.append(SemanticError(f'Тип магического метода {control.name} должен соответствовать '
                                                    f'func(Class, Class) -> (Class). Было дано: {f_type}', control.origin))
                                continue
                        case '__neg__':
                            if not f_type == types.func([class_instance_type], [class_instance_type]).simple:
                                errors.append(SemanticError(f'Тип магического метода __neg__ должен соответствовать '
                                                    f'func(Class) -> (Class). Было дано: {f_type}', control.origin))
                                continue
                        case '__eq__' | '__ne__' | '__lt__' | '__le__' | '__gt__' | '__ge__':
                            if not f_type == types.func([class_instance_type, class_instance_type], [t_bool]).simple:
                                errors.append(SemanticError(f'Тип магического метода {control.name} должен соответствовать '
                                                    f'func(Class, Class) -> (bool). Было дано: {f_type}', control.origin))
                                continue
                        case '__del__':
                            if not f_type == types.func([class_instance_type], []).simple:
                                errors.append(SemanticError(f'Тип магического метода __del__ должен соответствовать '
                                                    f'func(Class) -> (). Было дано: {f_type}', control.origin))
                                continue
                        case '__call__':
                            if not (
                                len(f_type.arguments) > 1 and
                                f_type.arguments[0] == class_instance_type
                            ):
                                errors.append(SemanticError('Тип магического метода __call__ должен соответствовать '
                                                           f'func(Class, <прочее>) -> (). Было дано: {f_type}', control.origin))
                                continue
                    cls.magic_methods[control.name] = control

                cls.class_field.append(control.var)
            # остальное всё такое же
            case ControlExpression():
                assert isinstance(control, ControlExpression)
                # а теперь займёмся костылями
                # все переменные до этого выражения
                vars_before = set(v.name for v in child_scope.variables)
                analyze_expression(child_scope, control, errors)
                # все переменные после
                vars_after = set(v.name for v in child_scope.variables)
                # переменные, полученные в этом выражении
                new_vars = vars_after - vars_before
                # и добавляем их сюда
                for new in new_vars:
                    var = child_scope.find_variable_in_cur_scope(new)
                    assert var is not None
                    cls.class_field.append(var)

            case ControlTypedef():
                analyze_typedef(child_scope, control, errors)
            case ControlClass():
                # assert isinstance(control, ControlClass)
                analyze_class(child_scope, control, errors)
                cls.class_field.append(control.class_var)
            case _:
                raise ValueError('')

    if len(cls.instance_field) != 0:
        cls.find_class_field('__init__') # сгенерируем __init__ если нужно


def analyze_enum(scope: Scope, enum: ControlEnum, errors: list[SemanticError]):
    # имя
    if is_in_key_word(enum.name):
        errors.append(SemanticError(f'Имя для перечисления "{enum.name}" не может быть ключевым словом', enum.origin))
        enum.is_bad = True
    else:
        if scope.is_name_occupied(enum.name, False):
            errors.append(SemanticError(f'Имя для перечисления "{enum.name}" уже занято в данной области видимости', enum.origin))
            enum.is_bad = True

    # проверка на уникальность полей
    if len(set(enum.states)) != len(enum.states):
        errors.append(SemanticError('Состояний с одним именем в перечислении быть не может', enum.origin))
        enum.is_bad = True

    scope.add_enum(enum)
    enum.enum_var = TokenOperatorVariableDefinition(
        enum.name, Type(Type.SimpleTypeEnum(enum), [], zero_origin), zero_origin
    )
    scope.add_variable(enum.enum_var)
    states_vars = []
    for name in enum.states:
        states_vars.append(TokenOperatorVariableDefinition(
            name, Type(Type.SimpleTypeEnumInstance(enum), [], zero_origin), zero_origin
        ))
    enum.states_vars = states_vars


def analyze_code_block(scope: Scope, block: ControlCodeBlock, errors: list[SemanticError]):
    for control in block.block_parts:
        match control:
            case ControlCodeBlock():
                child_scope = Scope(Scope.Types.Usual, control, scope)
                scope.add_child(child_scope)
                analyze_code_block(child_scope, control, errors)
            case ControlFunctionDefinition():
                analyze_function(scope, control, errors)
            case ControlExpression():
                analyze_expression(scope, control, errors)
            case ControlReturn():
                analyze_return(scope, control, errors)
            case ControlMassAssignment():
                analyze_mass_assignment(scope, control, errors)
            case ControlIf():
                analyze_if(scope, control, errors)
            case ControlWhile():
                analyze_while(scope, control, errors)
            case ControlCycleControl():
                analyze_cycle_control(scope, control, errors)
            case ControlTypedef():
                analyze_typedef(scope, control, errors)
            case ControlImport():
                analyze_import(scope, control, errors)
            case ControlExport():
                analyze_export(scope, control, errors)
            case ControlClass():
                analyze_class(scope, control, errors)
            case ControlEnum():
                analyze_enum(scope, control, errors)


def analyze(block: ControlCodeBlock,
            add_to_global_scope: list[ControlTypedef | TokenOperatorVariableDefinition] | None = None) -> tuple[Scope, list[SemanticError]]:
    main_scope = Scope(Scope.Types.Global, block, None)
    if add_to_global_scope:
        for thing in add_to_global_scope:
            if isinstance(thing, TokenOperatorVariableDefinition):
                main_scope.add_variable(thing)
            else:
                main_scope.add_typedef(thing)

    err = []

    analyze_code_block(main_scope, block, err)

    post_analyze_transforms(block, main_scope)

    return main_scope, err


