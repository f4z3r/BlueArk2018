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

    @abc.abstractmethod
    def get_children(self):
        """Returns the children of the node."""
        pass

    @abc.abstractmethod
    def scalar_mul(self, value):
        """Multiplies the node by a scalar."""
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
            else:
                nodes += [node]

        return constant, nodes


class LiteralNode(EvalNode):
    """Node containing a numerical value"""

    def __init__(self, value):
        """Takes `value` as the numerical value contained in the node."""
        self.value = value

    def evaluate(self):
        return self

    def negate(self):
        self.value = -self.value

    def get_sign(self):
        """Returns the sign of the node."""
        if self.value < 0:
            return "-"
        return ""

    def scalar_mul(self, value):
        self.value *= value

    def get_children(self):
        return [self]

    def __str__(self):
        return f"{float(self.value)}"


class SymbolicNode(EvalNode):
    """Node containing a symbolic value"""

    def __init__(self, value):
        """Takes `value` as the symbolic value contained in the node."""
        if value.startswith("-"):
            self.factor = -1.0
            self.value = value[1:]
        else:
            self.factor = 1.0
            self.value = value

    def evaluate(self):
        return self.value

    def negate(self):
        self.factor = -self.factor

    def get_children(self):
        return [self]

    def get_symbol(self):
        return self.value

    def scalar_mul(self, value):
        self.factor *= value

    def get_sign(self):
        """Returns the sign of the node."""
        if self.factor < 0:
            return "-"
        return ""

    def merge_symbol(self, iterable):
        """Adds its own value to a list of symbolic nodes."""
        for node in iterable:
            if type(node) is SymbolicNode:
                if node.get_symbol() == self.value:
                    node.add_symbolic(self.factor)
                    return
        iterable += [self]

    def add_symbolic(self, factor):
        """Adds adds `factor` to its own factor. This is the result of a simple
        add between two symbols."""
        self.factor += factor

    def __str__(self):
        return f"{self.factor}{self.value}"


class NaryPlus(EvalNode):
    """A n-ary plus operation between several nodes."""

    def __init__(self, *nodes):
        self.children = nodes
        self.factor = 1.0

    def evaluate(self):
        constant, nodes = EvalNode.propagate_constants(self.children)
        result = []
        for node in nodes:
            node.scalar_mul(self.factor)
            node.merge_symbol(result)
        constant *= self.factor
        if constant != 0:
            return NaryPlus(LiteralNode(constant), *result)
        return NaryPlus(*result)

    def negate(self):
        for child in self.children:
            child.negate()

    def scalar_mul(self, value):
        self.factor *= value

    def get_children(self):
        return self.children

    def __str__(self):
        result = " + ".join([str(child) for child in self.children])
        if self.factor != 1.0:
            result = f"{self.factor}({result})"
        return result

    def __iter__(self):
        return iter(self.children)


class ConstraintNode(metaclass=abc.ABCMeta):
    """Abstract base class for constraint nodes"""

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def _get_string(self, operator):
        """Gets the string based on the operator. This already simplifies the
        entire constraint."""
        lhs_constant, lhs_nodes = EvalNode.propagate_constants(
            self.lhs.get_children())
        rhs_constant, rhs_nodes = EvalNode.propagate_constants(
            self.rhs.get_children())
        constant = lhs_constant - rhs_constant
        for node in lhs_nodes:
            node.negate()
        symbols = NaryPlus(*rhs_nodes, *lhs_nodes)
        return f"{str(symbols)} {operator} {LiteralNode(constant)}"


class EqualityConstraint(ConstraintNode):
    """Constraint node representing equality"""

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def __str__(self):
        return self._get_string("=")


class GreaterThanConstraint(ConstraintNode):
    """Constraint node representing smaller or equal"""

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def __str__(self):
        return self._get_string("<=")
