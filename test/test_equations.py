#!/usr/bin/env python3

"""Tests the equations."""

import unittest

from blueark.equations import *


class TestEquations(unittest.TestCase):
    def test_stringify(self):
        lit1 = LiteralNode(5)
        lit2 = LiteralNode(10)
        binaryadd = NaryPlus(lit1, lit2)
        self.assertEqual(str(binaryadd), "5 + 10")
        fact = FactorNode(binaryadd, 2)
        self.assertEqual(str(fact), "(5 + 10) * 2")

    def test_constant_propagation(self):
        """Evaluate `5 + 10 + 100`"""
        lit1 = LiteralNode(5)
        lit2 = LiteralNode(10)
        lit3 = LiteralNode(100)
        ternaryadd = NaryPlus(lit1, lit2, lit3)
        self.assertEqual(str(ternaryadd.evaluate()), "115")
        fact = FactorNode(ternaryadd, 2)
        self.assertEqual(str(fact.evaluate()), "230")

    def test_symbolic_evaluation(self):
        """Evaluate symbolic constant propagated equation
        `(x + 10) + (y + 15)`
        """
        sym1 = SymbolicNode("x")
        lit1 = LiteralNode(10)
        binaryadd1 = NaryPlus(sym1, lit1)
        sym2 = SymbolicNode("y")
        lit2 = LiteralNode(15)
        binaryadd2 = NaryPlus(sym2, lit2)
        equation = NaryPlus(binaryadd1, binaryadd2)
        self.assertEqual(str(equation), "x + 10 + y + 15")
        self.assertEqual(str(equation.evaluate()), "25 + x + y")
        fact = FactorNode(equation, 3)
        self.assertEqual(str(fact.evaluate()), "75 + (x) * 3 + (y) * 3")

    def test_equality_constraint(self):
        """Test constant propagated equality output for constraint
        `100 = (x + 10) + (y + 15)`
        """
        sym1 = SymbolicNode("x")
        lit1 = LiteralNode(10)
        binaryadd1 = NaryPlus(sym1, lit1)
        sym2 = SymbolicNode("y")
        lit2 = LiteralNode(15)
        binaryadd2 = NaryPlus(sym2, lit2)
        equation = NaryPlus(binaryadd1, binaryadd2)
        constraint = EqualityConstraint(NaryPlus(LiteralNode(100)), equation)
        self.assertEqual(str(constraint), "x + y = 75")

    def test_equality_constraint_2(self):
        """Test constant propagated equality output for constraint
        `-x = y`
        """
        sym1 = SymbolicNode("y")
        equation = NaryPlus(sym1)
        constraint = EqualityConstraint(NaryPlus(SymbolicNode("-x")), equation)
        self.assertEqual(str(constraint), "y + x = 0")

    def test_geq_constraint(self):
        """Test constant propagated equality output for constraint
        `z >= y + 5`
        """
        sym1 = SymbolicNode("y")
        lit1 = LiteralNode(5)
        equation = NaryPlus(sym1, lit1)
        constraint = GreaterThanConstraint(NaryPlus(SymbolicNode("z")), equation)
        self.assertEqual(str(constraint), "y + -z <= -5")

    def test_geq_constraint_2(self):
        """Test constant propagated equality output for constraint
        `z + 10 + 5>= x + -y + 5`
        """
        sym1 = SymbolicNode("z")
        lit1 = LiteralNode(10)
        lit2 = LiteralNode(5)
        ternaryadd1 = NaryPlus(sym1, lit1, lit2)
        sym2 = SymbolicNode("x")
        sym3 = SymbolicNode("-y")
        lit3 = LiteralNode(5)
        ternaryadd2 = NaryPlus(sym2, sym3, lit3)
        constraint = GreaterThanConstraint(ternaryadd1, ternaryadd2)
        self.assertEqual(str(constraint), "x + -y + -z <= 10")
