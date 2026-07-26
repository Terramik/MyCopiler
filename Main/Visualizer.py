from ..Definitions.Scopes import *
from ..Definitions.Tokens import *
import networkx as nx
import matplotlib.pyplot as plt
import uuid
import os
from functools import singledispatch
import pydot


@singledispatch
def write(node: TokenOperatorABC | ControlABC | Type, graph, parent_id=None):
    raise NotImplementedError('Что-то пошло не так')


def pre_op(node: TokenOperatorABC | ControlABC | Type, graph, label: str, parent_id=None) -> int:
    node_id = id(node)
    graph.add_node(node_id, label=label)
    if parent_id is not None:
        graph.add_edge(parent_id, node_id)
    return node_id


# --- Управляющие конструкции ---

@write.register(ControlFunctionDefinition)
def _(node: ControlFunctionDefinition, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Function.value, parent_id)
    # имя функции
    name_id = uuid.uuid4()
    graph.add_node(name_id, label=node.name)
    graph.add_edge(node_id, name_id)

    # параметры
    pars_id = uuid.uuid4()
    graph.add_node(pars_id, label='par')
    graph.add_edge(node_id, pars_id)
    for tok in node.parameters:
        write(tok, graph, pars_id)

    # результаты
    res_id = uuid.uuid4()
    graph.add_node(res_id, label='res')
    graph.add_edge(node_id, res_id)
    for tok in node.results:
        write(tok, graph, res_id)

    # её блок кода
    write(node.code_block, graph, node_id)


@write.register(ControlCodeBlock)
def _(node: ControlCodeBlock, graph, parent_id=None):
    node_id = pre_op(node, graph, '{ ... }', parent_id)

    for control in node.block_parts:
        write(control, graph, node_id)


@write.register(ControlExpression)
def _(node: ControlExpression, graph, parent_id=None):
    node_id = pre_op(node, graph, '... ;', parent_id)
    write(node.first, graph, node_id)


@write.register(ControlReturn)
def _(node: ControlReturn, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Return.value, parent_id)

    for expr in node.results:
        write(expr, graph, node_id)


@write.register(ControlMassAssignment)
def _(node: ControlMassAssignment, graph, parent_id=None):
    node_id = pre_op(node, graph, 'mass', parent_id)

    if node.processed:
        for expr in node.left:
            write(expr, graph, node_id)
        eq_sing_id = uuid.uuid4()
        graph.add_node(eq_sing_id, label='=')
        graph.add_edge(node_id, eq_sing_id)

        for procsd in node.processed:
            # добавляем первую штуку
            tmp_id = uuid.uuid4()
            graph.add_node(tmp_id, label='...' if procsd.t_need[0] is None else procsd.t_need[0])
            graph.add_edge(node_id, tmp_id)
            write(procsd.rvalue, graph, tmp_id)

            # добавляем все остальные
            rv_id = id(procsd.rvalue)
            for t in (procsd.t_need[i] for i in range(1, len(procsd.t_need))):
                tmp_id = uuid.uuid4()
                graph.add_node(tmp_id, label='...' if t is None else t)
                graph.add_edge(node_id, tmp_id)
                graph.add_edge(tmp_id, rv_id)
    else:
        for tok in node.left:
            write(tok, graph, node_id)
        eq_sing_id = uuid.uuid4()
        graph.add_node(eq_sing_id, label='=')
        graph.add_edge(node_id, eq_sing_id)
        for tok in node.right:
            write(tok, graph, node_id)


@write.register(ControlConditional)
def _(node: ControlConditional, graph, parent_id=None):
    node_id = pre_op(node, graph, f'if/elif/else', parent_id)
    # if
    if_id = uuid.uuid4()
    graph.add_node(if_id, label=KeyWords.ConditionalStart.value)
    graph.add_edge(node_id, if_id)
    write(node.start.condition, graph, if_id)
    write(node.start.code_block, graph, if_id)
    # elif
    for mid in node.middle:
        elif_id = uuid.uuid4()
        graph.add_node(elif_id, label=KeyWords.ConditionalMiddle.value)
        graph.add_edge(node_id, elif_id)
        write(mid.condition, graph, elif_id)
        write(mid.code_block, graph, elif_id)
    # else
    if node.end is not None:
        else_id = uuid.uuid4()
        graph.add_node(else_id, label=KeyWords.ConditionalEnd.value)
        graph.add_edge(node_id, else_id)
        write(node.end.code_block, graph, else_id)


@write.register(ControlWhile)
def _(node: ControlWhile, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.CycleWhile.value, parent_id)
    write(node.condition, graph, node_id)
    write(node.code_block, graph, node_id)


@write.register(ControlCycleControl)
def _(node: ControlCycleControl, graph, parent_id=None):
    node_id = pre_op(node, graph, repr(node)[:-1], parent_id)


@write.register(Type)
def _(node: Type, graph, parent_id=None):
    node_id = pre_op(node, graph, repr(node), parent_id)


# --- Выражения ---

@write.register(TokenOperatorVariableDefinition)
def _(node: TokenOperatorVariableDefinition, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Variable.value, parent_id)
    write(node.type, graph, node_id)
    name_id = uuid.uuid4()
    graph.add_node(name_id, label=node.name)
    graph.add_edge(node_id, name_id)


@write.register(TokenVariableAccess)
def _(node: TokenVariableAccess, graph, parent_id=None):
    node_id = pre_op(node, graph, f'{node.name}', parent_id)


@write.register(TokenLiteral)
def _(node: TokenLiteral, graph, parent_id=None):
    node_id = pre_op(node, graph, node.value, parent_id)


@write.register(TokenOperatorAssignment)
def _(node: TokenOperatorAssignment, graph, parent_id=None):
    node_id = pre_op(node, graph, '=', parent_id)
    write(node.left, graph, node_id)
    write(node.right, graph, node_id)


@write.register(TokenOperatorFunctionCall)
def _(node: TokenOperatorFunctionCall, graph, parent_id=None):
    node_id = pre_op(node, graph, node.name, parent_id)
    for arg in node.arguments:
        write(arg, graph, node_id)


@write.register(TokenOperatorBinary)
def _(node: TokenOperatorBinary, graph, parent_id=None):
    node_id = pre_op(node, graph, node.type.value.symbol, parent_id)
    write(node.left, graph, node_id)
    write(node.right, graph, node_id)


@write.register(TokenOperatorPrefix)
def _(node: TokenOperatorPrefix, graph, parent_id=None):
    node_id = pre_op(node, graph, node.type.value.symbol, parent_id)
    write(node.operand, graph, node_id)


@write.register(TokenOperatorPostfix)
def _(node: TokenOperatorPostfix, graph, parent_id=None):
    node_id = pre_op(node, graph, node.type.value.symbol, parent_id)
    write(node.operand, graph, node_id)


@write.register(TokenOperatorCast)
def _(node: TokenOperatorCast, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Cast.value, parent_id)

    write(node.operand, graph, node_id)

    cast_to_id = uuid.uuid4()
    graph.add_node(cast_to_id, label=repr(node.cast_type))
    graph.add_edge(node_id, cast_to_id)


@write.register(TokenOperatorSizeof)
def _(node: TokenOperatorSizeof, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Sizeof.value, parent_id)
    write(node.type, graph, node_id)


@write.register(TokenOperatorLenof)
def _(node: TokenOperatorLenof, graph, parent_id=None):
    node_id = pre_op(node, graph, KeyWords.Lenof.value, parent_id)
    write(node.operand, graph, node_id)


@write.register(TokenOperatorSlize)
def _(node: TokenOperatorSlize, graph, parent_id=None):
    node_id = pre_op(node, graph, 'slice', parent_id)

    write(node.operand, graph, node_id)

    if node.position_start is None:
        none_id = uuid.uuid4()
        graph.add_node(none_id, label='-')
        graph.add_edge(node_id, none_id)
    else:
        for index in node.position_start:
            write(index, graph, node_id)

    seperator_id = uuid.uuid4()
    graph.add_node(seperator_id, label=':')
    graph.add_edge(node_id, seperator_id)

    if node.result_dimensions is None:
        none_id = uuid.uuid4()
        graph.add_node(none_id, label='-')
        graph.add_edge(node_id, none_id)
    else:
        for dim in node.result_dimensions:
            write(dim, graph, node_id)


@write.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, graph, parent_id=None):
    node_id = pre_op(node, graph, '[]', parent_id)
    write(node.operand, graph, node_id)
    write(node.index, graph, node_id)


@write.register(TokenOperatorArrayCreation)
def _(node: TokenOperatorArrayCreation, graph, parent_id=None):
    node_id = pre_op(node, graph, 'array', parent_id)

    opener_id = uuid.uuid4()
    graph.add_node(opener_id, label='[')
    graph.add_edge(node_id, opener_id)

    for expr in node.operands:
        write(expr, graph, node_id)

    closer_id = uuid.uuid4()
    graph.add_node(closer_id, label=']')
    graph.add_edge(node_id, closer_id)


@write.register(TokenOperatorReferencing)
def _(node: TokenOperatorReferencing, graph, parent_id=None):
    node_id = pre_op(node, graph, TokenOperatorPostfixTypes.Referencing.value.symbol, parent_id)
    write(node.operand, graph, node_id)


@write.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, graph, parent_id=None):
    node_id = pre_op(node, graph, TokenOperatorPostfixTypes.Dereferencing.value.symbol, parent_id)
    write(node.operand, graph, node_id)


# --- Остальное ---

def add_scope(graph, scope: Scope, parent_id=None):
    scope_id = id(scope)
    label: str
    match scope.type:
        case Scope.Types.Global:
            label = 'global'
        case Scope.Types.Function:
            label = f'func: {scope.creator.name}'
        case Scope.Types.Usual:
            label = 'usual'
        case Scope.Types.Conditional:
            label = 'conditional'
        case Scope.Types.Cycle:
            label = 'cycle'
        case _:
            raise ValueError("Что-то пошло не так, и пайчарму не нравиться, что все случаи не обработаны")

    graph.add_node(scope_id, label=label)
    if parent_id is not None:
        graph.add_edge(parent_id, scope_id)

    vars_id = uuid.uuid4()
    graph.add_node(vars_id, label='vars')
    graph.add_edge(scope_id, vars_id)
    for var in scope.variables.values():
        var_id = uuid.uuid4()  # тут не id, потому-что id используются в основном блоке
        graph.add_node(var_id, label=repr(var))
        graph.add_edge(vars_id, var_id)

    funcs_id = uuid.uuid4()
    graph.add_node(funcs_id, label='funcs')
    graph.add_edge(scope_id, funcs_id)
    for f in scope.functions.values():
        f_id = uuid.uuid4()
        graph.add_node(f_id, label=f.name)
        graph.add_edge(funcs_id, f_id)

    inner_id = uuid.uuid4()
    graph.add_node(inner_id, label='inner')
    graph.add_edge(scope_id, inner_id)

    for child in scope.children:
        add_scope(graph, child, inner_id)


def print_all(block: ControlCodeBlock, scope: Scope | None = None):
    graph = nx.DiGraph()
    # for f in block.block_parts:
    #     add_nodes(graph, f)
    write(block, graph)

    if scope is not None:
        add_scope(graph, scope)

    pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')

    labels = nx.get_node_attributes(graph, 'label')
    plt.figure(figsize=(20, 10))
    nx.draw(graph, pos, labels=labels, with_labels=True,
            node_size=2000, node_color='lightblue',
            font_size=10, font_weight='bold', arrows=False)
    plt.show()


file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'TheAST.png')


def save_as_svg(block: ControlCodeBlock, scope: Scope | None = None):
    graph = nx.DiGraph()
    write(block, graph)

    if scope is not None:
        add_scope(graph, scope)

    pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')

    labels = nx.get_node_attributes(graph, 'label')
    plt.figure(figsize=(140, 15))
    nx.draw(graph, pos, labels=labels, with_labels=True,
            node_size=2000, node_color='lightblue',
            font_size=10, font_weight='bold', arrows=False)
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
