#!/usr/bin/env python3

"""Equations module."""

import abc


class EvalNode(metaclass=abc.ABCMeta):
    """Abstract base class for nodes that can be computationally evaluated."""
    @abc.abstractmethod
    def evaluate(self):
        """Evaluates the node"""
        pass

    @abc.abstractmethod
    def negate(self):
        """Negates the node"""
        pass


    @staticmethod
    def propagate_constants(iterable):
        """Propagates constant evaluations but keeps symbolic nodes intact."""
        constant = 0
        nodes = []
        for node in iterable:
            if type(node) is NaryPlus:
                sub_constant, sub_nodes = EvalNode.propagate_constants(node)
                constant += sub_constant
                nodes += sub_nodes
            elif type(node) is LiteralNode:
                constant += node.value
            elif type(node) is SymbolicNode:
                nodes += [node]
        return constant, nodes


class LiteralNode(EvalNode):
    """Node containing a numerical value"""
    def __init__(self, value):
        """Takes `value` as the numerical value contained in the node."""
        self.value = value
        self.negated = value < 0

    def evaluate(self):
        return self

    def negate(self):
        self.negated = not self.negated
        self.value = -self.value

    def __str__(self):
        return str(self.value)


class SymbolicNode(EvalNode):
    """Node containing a symbolic value"""
    def __init__(self, value):
        """Takes `value` as the symbolic value contained in the node."""
        self.negated = value.startswith("-")
        if self.negated:
            self.value = value[1:]
        else:
            self.value = value

    def evaluate(self):
        return self.value

    def negate(self):
        self.negated = not self.negated

    def __str__(self):
        result = ""
        if self.negated:
            result += "-"
        result += self.value
        return result


class NaryPlus(EvalNode):
    """A n-ary plus operation between several nodes."""
    def __init__(self, *nodes):
        self.children = nodes

    def evaluate(self):
        constant, nodes = EvalNode.propagate_constants(self.children)
        return NaryPlus(LiteralNode(constant), *nodes)

    def negate(self):
        for child in self.children:
            child.negate()

    def __str__(self):
        return " + ".join([str(child) for child in self.children])

    def __iter__(self):
        return iter(self.children)


class FactorNode(EvalNode):
    """A node multiplied by a given factor"""
    def __init__(self, node, k):
        self.node = node
        self.k = k

    def evaluate(self):
        evaluated = self.node.evaluate()
        # flatten nested factor node
        if type(evaluated) is FactorNode:
            return FactorNode(evaluated.node, evaluated.k * self.k).evaluate()
        # distribute factor nodes inside plus nodes
        elif type(evaluated) is NaryPlus:
            return NaryPlus(*list(map(lambda n: FactorNode(n, self.k).evaluate(), evaluated)))
        # evaluate constant multiplication
        elif type(evaluated) is LiteralNode:
            return LiteralNode(self.k * evaluated.value)
        else:
            return self

    def negate(self):
        self.k = -self.k

    def __str__(self):
        if type(self.node) is SymbolicNode:
            return f"{str(self.k)} {str(self.node)}"
        else:
            return f"({str(self.node)}) * {str(self.k)}"


class ConstraintNode(metaclass=abc.ABCMeta):
    """Abstract base class for constraint nodes"""
    def __init__(self, node, evalnode):
        self.node = node
        self.evalnode = evalnode

    def _get_string(self, operator):
        constant, nodes = EvalNode.propagate_constants(self.evalnode.children)
        if type(self.node) is LiteralNode:
            bound = LiteralNode(self.node.value - constant)
        else:
            nodes += [self.node.negate()]
            bound = LiteralNode(-constant)
        symbols = NaryPlus(*nodes)
        return f"{str(symbols)} {operator} {str(bound)}"


class EqualityConstraint(ConstraintNode):
    """Constraint node representing equality"""
    def __init__(self, node, evalnode):
        super().__init__(node, evalnode)

    def __str__(self):
        return self._get_string("=")


class LessThanConstraint(ConstraintNode):
    """Constraint node representing larger or equal"""
    def __init__(self, node, evalnode):
        super().__init__(node, evalnode)

    def __str__(self):
        return self._get_string(">=")


class GreaterThanConstraint(ConstraintNode):
    """Constraint node representing smaller or equal"""
    def __init__(self, node, evalnode):
        super().__init__(node, evalnode)

    def __str__(self):
        return self._get_string("<=")
