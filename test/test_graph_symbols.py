#!/usr/bin/env python3

"""Tests the equations."""

import unittest

from blueark.model.entities import *
from blueark.equations import *


class TestGraphSymbols(unittest.TestCase):
    def test_source_alone(self):
        SymbolGenerator.reset()
        consumer = Consumer(50)
        src = Source(consumer, 100, False)
        src.propagate_symbols_downstream()
        self.assertEqual(consumer.parents, {SymbolicNode("x_1")})

    def test_source_tank_consumer(self):
        SymbolGenerator.reset()
        consumer = Consumer(50)
        left = Pipe([consumer], 100, 0, 100)
        right = Pipe([consumer], 100, 0, 100)
        tank = Tank([left, right], 1000, 500)
        tank_to_source = Pipe([tank], 100, 0, 100)
        src = Source(tank_to_source, 60, True)
        src.propagate_symbols_downstream()
        self.assertEqual(consumer.parents,
                         {SymbolicNode("x_1"), SymbolicNode("x_2")})

    def test_equation_generation(self):
        SymbolGenerator.reset()
        consumer = Consumer(50)
        left = Pipe([consumer], 100, 0, 100)
        right = Pipe([consumer], 100, 0, 100)
        tank = Tank([left, right], 1000, 500)
        tank_to_source = Pipe([tank], 100, 0, 100)
        src = Source(tank_to_source, 60, True)
        src.propagate_symbols_downstream()
        constraints, maximisers = src.demand_equations()
        self.assertFalse(maximisers)
        lhs = NaryPlus(LiteralNode(0))
        rhs = NaryPlus(SymbolicNode("x_1"), SymbolicNode("x_2"),
                       SymbolicNode("-x_0"))
        expected = EqualityConstraint(lhs, rhs)
        self.assertEqual(constraints[0], expected)
        self.assertEqual(str(constraints[1]), "1.0x_0 = 50.0")
