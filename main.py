#!/usr/bin/env python3 -O

from blueark.equations import *
from blueark.model.entities import *


def return_something():
    SymbolGenerator.reset()
    consumer = Consumer(50)
    left = Pipe([consumer], 100, 0)
    right = Pipe([consumer], 100, 0)
    tank = Tank([left, right], 1000)
    tank_to_source = Pipe([tank], 100, 0)
    src = Source(tank_to_source)
    src.propagate_symbols_downstream()
    constraints, maximisers = src.demand_equations()
    for constraint in set(constraints):
        print(str(constraint))


if __name__ == "__main__":
    return_something()
