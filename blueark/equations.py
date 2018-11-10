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
        self.negated = value < 0

    def evaluate(self):
        return self

    def negate(self):
        self.negated = not self.negated
        self.value = -self.value

    def get_sign(self):
        """Returns the sign of the node."""
        if self.negated:
            return "-"
        return ""

    def get_children(self):
        return [self]

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

    def get_children(self):
        return [self]

    def get_symbol(self):
        return self.value

    def get_sign(self):
        """Returns the sign of the node."""
        if self.negated:
            return "-"
        return ""

    def __str__(self):
        result = ""
        if self.negated:
            result += "-"
        result += f"{float(1)}{self.value}"
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

    def get_children(self):
        return self.children

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
            return NaryPlus(*list(map(
                lambda n: FactorNode(n, self.k).evaluate(),
                evaluated)))
        # evaluate constant multiplication
        elif type(evaluated) is LiteralNode:
            return LiteralNode(self.k * evaluated.value)
        else:
            return self

    def get_children(self):
        return [self]

    def negate(self):
        self.k = -self.k

    def __str__(self):
        if type(self.node) is SymbolicNode:
            return f"{self.node.get_sign()}{float(self.k)}" +\
                   f"{str(self.node.get_symbol())}"
        else:
            return f"{float(self.k)}({str(self.node)})"


class ConstraintNode(metaclass=abc.ABCMeta):
    """Abstract base class for constraint nodes"""
    def __init__(self, node, evalnode):
        self.node = node
        self.k = k

    def evaluate(self):
        # flatten nested factor node
        if type(self.node) is FactorNode:
            return FactorNode(self.node.node, self.node.k * self.k).evaluate()
        # distribute factor nodes inside plus nodes
        elif type(self.node) is NaryPlus:
            return NaryPlus(*list(map(
                lambda n: FactorNode(n, self.k).evaluate(),
                self.node))).evaluate()
        # evaluate constant multiplication
        elif type(self.node) is LiteralNode:
            return LiteralNode(self.k * self.node.evaluate())
        else:
            return self

    def get_children(self):
        return [self]

    def negate(self):
        self.k = -self.k

    def __str__(self):
        return f"({str(self.node)}) * {str(self.k)}"


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
        return f"{str(symbols)} {operator} {constant}"


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
