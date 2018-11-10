#!/usr/bin/env python3 -O

from blueark.model.sample_model import Model


def return_something():
    model = Model()
    model.set_consumer_usage(150, 150, 150, 150, 150, 150)
    constraints, maximisers = model.gen_constraints()
    for constraint in constraints:
        print(constraint)
    for maximiser in maximisers:
        print(maximiser)


def main():
    pass


if __name__ == "__main__":
    return_something()
