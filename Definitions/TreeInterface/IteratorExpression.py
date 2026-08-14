from typing import Callable
from ..Tokens import *


class IteratorExpression(ABC):
    
    # диспетчеризация
    def __call__(self, node: TokenOperatorRvalueABC | TokenOperatorWvalueABC, parent: TypeExpressionParent):
        match node:
            case TokenOperatorVariableDefinition(): self.on_var_def(node, parent)
            case TokenVariableAccess(): self.on_var_access(node, parent)
            case TokenLiteral(): self.on_literal(node, parent)
            case TokenOperatorAssignment(): self.on_assignment(node, parent)
            case TokenOperatorFunctionCall(): self.on_f_call(node, parent)
            case TokenOperatorBinary(): self.on_binary(node, parent)
            case TokenOperatorPrefix(): self.on_prefix(node, parent)
            case TokenOperatorPostfix(): self.on_postfix(node, parent)
            case TokenOperatorCast(): self.on_cast(node, parent)
            case TokenOperatorSizeof(): self.on_sizeof(node, parent)
            case TokenOperatorLenof(): self.on_lenof(node, parent)
            case TokenOperatorSlize(): self.on_slize(node, parent)
            case TokenOperatorIndex(): self.on_index(node, parent)
            case TokenOperatorArrayCreation(): self.on_array_creation(node, parent)
            case TokenOperatorReferencing(): self.on_referencing(node, parent)
            case TokenOperatorDereferencing(): self.on_dereferencing(node, parent)
            case TokenOperatorFieldAccess(): self.on_field_access(node, parent)
            case TokenOperatorFieldAccessPointer(): self.on_field_access_pointer(node, parent)
            case TokenOperatorDeInitializer(): self.on_deinitializer(node, parent)
            case TokenOperatorError(): self.on_error_node(node, parent)
            case _:
                raise NotImplementedError('Что-то пошло не так')
        
    # методы для всего

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        pass

    def on_var_access(self, node: TokenVariableAccess, parent: TypeExpressionParent):
        pass

    def on_literal(self, node: TokenLiteral, parent: TypeExpressionParent):
        pass
    
    def on_assignment(self, node: TokenOperatorAssignment, parent: TypeExpressionParent):
        self(node.left, node)
        self(node.right, node)

    def on_f_call(self, node: TokenOperatorFunctionCall, parent: TypeExpressionParent):
        self(node.func, node)
        for ar in node.arguments:
            self(ar, node)

    def on_binary(self, node: TokenOperatorBinary, parent: TypeExpressionParent):
        self(node.left, node)
        self(node.right, node)

    def on_prefix(self, node: TokenOperatorPrefix, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_postfix(self, node: TokenOperatorPostfix, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_cast(self, node: TokenOperatorCast, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_sizeof(self, node: TokenOperatorSizeof, parent: TypeExpressionParent):
        pass

    def on_lenof(self, node: TokenOperatorLenof, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_slize(self, node: TokenOperatorSlize, parent: TypeExpressionParent):
        self(node.operand, node)
        for index in node.position_start:
            self(index, node)
        for dim in node.result_dimensions:
            self(dim, node)

    def on_index(self, node: TokenOperatorIndex, parent: TypeExpressionParent):
        self(node.operand, node)
        self(node.index, node)

    def on_array_creation(self, node: TokenOperatorArrayCreation, parent: TypeExpressionParent):
        for dim in node.operands:
            self(dim, node)

    def on_referencing(self, node: TokenOperatorReferencing, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_dereferencing(self, node: TokenOperatorDereferencing, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_field_access(self, node: TokenOperatorFieldAccess, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_field_access_pointer(self, node: TokenOperatorFieldAccessPointer, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_deinitializer(self, node: TokenOperatorDeInitializer, parent: TypeExpressionParent):
        self(node.operand, node)

    def on_error_node(self, node: TokenOperatorError, parent: TypeExpressionParent):
        pass
