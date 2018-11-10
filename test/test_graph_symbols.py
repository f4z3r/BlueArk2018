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
        self.assertEqual(consumer.parents, {SymbolicNode("x_6")})

    def test_source_tank_consumer(self):
        SymbolGenerator.reset()
        consumer = Consumer(50)
        left = Pipe([consumer], 100, 0, 100)
        right = Pipe([consumer], 100, 0, 100)
        tank = Tank([left, right], 1000, 500)
        tank_to_source = Pipe([tank], 100, 0, 100)
        src = Source(tank_to_source, 60, True)
        src.propagate_symbols_downstream()
        self.assertEqual(consumer.parents, {SymbolicNode("x_8"), SymbolicNode("x_9")})
