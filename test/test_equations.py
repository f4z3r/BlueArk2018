#!/usr/bin/env python3

"""Tests the equations."""

import unittest

from blueark.equations import *


class TestEquations(unittest.TestCase):
    def test_symbol_generator(self):
        self.assertEqual(SymbolGenerator.gen(), "x_0")
        self.assertEqual(SymbolGenerator.gen(), "x_1")
        self.assertEqual(SymbolGenerator.gen(), "x_2")
        self.assertEqual(SymbolGenerator.gen(), "x_3")
        self.assertEqual(SymbolGenerator.gen(), "x_4")

    def test_equalities(self):
        self.assertEqual(LiteralNode(5.3), LiteralNode(5.3))
        self.assertNotEqual(LiteralNode(5.3), LiteralNode(5.4))
        self.assertEqual(SymbolicNode("-x_0"), SymbolicNode("-x_0"))
        sym1 = SymbolicNode("-x_0")
        sym2 = SymbolicNode("x_0")
        sym1.scalar_mul(-30)
        sym2.scalar_mul(30)
        self.assertEqual(sym1, sym2)
        sym1 = SymbolicNode("-x_0")
        sym2 = SymbolicNode("x_0")
        sym1.scalar_mul(-30)
        sym2.scalar_mul(-30)
        self.assertNotEqual(sym1, sym2)
        eq1 = NaryPlus(LiteralNode(-2), LiteralNode(9), SymbolicNode("-y"))
        eq2 = NaryPlus(LiteralNode(7), SymbolicNode("-y"))
        self.assertEqual(eq1, eq2)
        eq1 = NaryPlus(LiteralNode(-1), LiteralNode(9), SymbolicNode("-y"))
        eq2 = NaryPlus(LiteralNode(7), SymbolicNode("-y"))
        self.assertNotEqual(eq1, eq2)

    def test_equalities_constraints(self):
        # -2 + 9 + -2y >= z
        sym1 = SymbolicNode("-y")
        sym1.scalar_mul(2)
        lhs = NaryPlus(LiteralNode(-2), LiteralNode(9), sym1)
        rhs = NaryPlus(SymbolicNode("z"))
        constraint1 = GreaterThanConstraint(lhs, rhs)
        # 7 + -y + -z >= y
        lhs = NaryPlus(LiteralNode(7), SymbolicNode("-y"), SymbolicNode("-z"))
        rhs = NaryPlus(SymbolicNode("y"))
        constraint2 = GreaterThanConstraint(lhs, rhs)
        self.assertEqual(constraint1, constraint2)
        # -2 + 9 + -2y >= z
        sym1 = SymbolicNode("-y")
        sym1.scalar_mul(2)
        lhs = NaryPlus(LiteralNode(-2), LiteralNode(9), sym1)
        rhs = NaryPlus(SymbolicNode("z"))
        constraint1 = GreaterThanConstraint(lhs, rhs)
        # 7 + -y + z >= y
        lhs = NaryPlus(LiteralNode(7), SymbolicNode("-y"), SymbolicNode("z"))
        rhs = NaryPlus(SymbolicNode("y"))
        constraint2 = GreaterThanConstraint(lhs, rhs)
        self.assertNotEqual(constraint1, constraint2)

    def test_stringify(self):
        lit1 = LiteralNode(5)
        lit2 = LiteralNode(10)
        binaryadd = NaryPlus(lit1, lit2)
        self.assertEqual(str(binaryadd), "5.0 + 10.0")
        binaryadd.scalar_mul(2)
        self.assertEqual(str(binaryadd), "2.0(5.0 + 10.0)")

    def test_stringify_fact(self):
        lit1 = SymbolicNode("-x")
        lit1.scalar_mul(4.5)
        self.assertEqual(str(lit1), "-4.5x")

    def test_stringify_fact_2(self):
        lit1 = LiteralNode(2)
        lit1.scalar_mul(-4.5)
        self.assertEqual(str(lit1), "-9.0")
        self.assertEqual(str(lit1.evaluate()), "-9.0")

    def test_constant_propagation(self):
        """Evaluate `5 + 10 + 100`"""
        lit1 = LiteralNode(5)
        lit2 = LiteralNode(10)
        lit3 = LiteralNode(100)
        ternaryadd = NaryPlus(lit1, lit2, lit3)
        self.assertEqual(str(ternaryadd.evaluate()), "115.0")
        ternaryadd.scalar_mul(2)
        self.assertEqual(str(ternaryadd.evaluate()), "230.0")

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
        self.assertEqual(str(equation), "1.0x + 10.0 + 1.0y + 15.0")
        self.assertEqual(str(equation.evaluate()), "25.0 + 1.0x + 1.0y")
        equation.scalar_mul(3)
        self.assertEqual(str(equation.evaluate()), "75.0 + 3.0x + 3.0y")

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
        self.assertEqual(str(constraint), "1.0x + 1.0y = 75.0")

    def test_equality_constraint_2(self):
        """Test constant propagated equality output for constraint
        `-x = y`
        """
        sym1 = SymbolicNode("y")
        equation = NaryPlus(sym1)
        constraint = EqualityConstraint(NaryPlus(SymbolicNode("-x")), equation)
        self.assertEqual(str(constraint), "1.0y + 1.0x = 0.0")

    def test_geq_constraint(self):
        """Test constant propagated equality output for constraint
        `z >= y + 5`
        """
        sym1 = SymbolicNode("y")
        lit1 = LiteralNode(5)
        equation = NaryPlus(sym1, lit1)
        constraint = GreaterThanConstraint(NaryPlus(SymbolicNode("z")),
                                           equation)
        self.assertEqual(str(constraint), "1.0y + -1.0z <= -5.0")

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
        self.assertEqual(str(constraint), "1.0x + -1.0y + -1.0z <= 10.0")

    def test_symbol_merging(self):
        """Test if symbol merging works properly."""
        sym1 = SymbolicNode("z")
        sym1.scalar_mul(-45.6)
        sym2 = SymbolicNode("x")
        sym3 = SymbolicNode("z")
        sym3.scalar_mul(3)
        ternaryadd = NaryPlus(sym1, sym2, sym3)
        self.assertEqual(str(ternaryadd.evaluate()), "-42.6z + 1.0x")
