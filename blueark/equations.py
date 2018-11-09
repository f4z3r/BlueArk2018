#!/usr/bin/env python3

"""Equations module."""

import abc


class EvalNode(metaclass=abc.ABCMeta):
    """Abstract base class for nodes that can be computationally evaluated."""
    @abc.abstractmethod
    def evaluate(self):
        """Evaluates the node"""
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

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.value)


class SymbolicNode(EvalNode):
    """Node containing a symbolic value"""
    def __init__(self, value):
        """Takes `value` as the symbolic value contained in the node."""
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return self.value


class NaryPlus(EvalNode):
    """A n-ary plus operation between several nodes."""
    def __init__(self, *nodes):
        self.children = nodes

    def evaluate(self):
        constant, nodes = EvalNode.propagate_constants(self.children)
        return NaryPlus(LiteralNode(constant), *nodes)

    def __str__(self):
        return " + ".join([str(child) for child in self.children])

    def __iter__(self):
        return iter(self.children)


class ConstraintNode(metaclass=abc.ABCMeta):
    """Abstract base class for constraint nodes"""
    def __init__(self, value, evalnode):
        self.value = value
        self.evalnode = evalnode


class EqualityConstraint(ConstraintNode):
    """Constraint node representing equality"""
    def __init__(self, value, evalnode):
        super().__init__(value, evalnode)

    def __str__(self):
        return f"{self.value} == {str(self.evalnode.evaluate())}"


class LessThanConstraint(ConstraintNode):
    """Constraint node representing larger or equal"""
    def __init__(self, value, evalnode):
        super().__init__(value, evalnode)

    def __str__(self):
        return f"{self.value} <= {str(self.evalnode.evaluate())}"


class GreaterThanConstraint(ConstraintNode):
    """Constraint node representing smaller or equal"""
    def __init__(self, value, evalnode):
        super().__init__(value, evalnode)

    def __str__(self):
        return f"{self.value} >= {str(self.evalnode.evaluate())}"
