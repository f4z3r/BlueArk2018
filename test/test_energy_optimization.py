#!/usr/bin/env python3

"""Tests for the optimizer."""

import unittest

import numpy as np
from blueark.optmization.ScipyMinimizer import ScipySolver


class TestOptimizer(unittest.TestCase):

    def test_scipy_optimizer(self):
        """Performs a test on a simple predictible network."""

        constraint_matrix = [[-1.0, -1.0, 0.0, 0.0],
                             [0.0, 1.0, -1.0, 0.0],
                             [1.0, 0.0, 1.0, -1.0]]

        lower_bounds = [0., 0., 50., 150.]
        upper_bounds = [80., 100., 100., 200.]

        rhs_vector = [100., 50., 0., 80., 100.]

        equalities = [1, 1, 0]

        init_guess = [40, 50, 50, 140]

        turbine_params = [0.9, 0.0, 0.0, 0.0]

        solver = ScipySolver(turbine_params, constraint_matrix,
                             lower_bounds, upper_bounds,
                             rhs_vector, equalities, init_guess)

        ret = solver.solve()

        print(70 * '=')
        print('\tOptimization results:')
        print(ret)
        print(70 * '=')

        # self.assertEqual(ret.value, 80, 0.5)


if __name__ == '__main__':
    tester = TestOptimizer()
    # tester.test_scipy_optimizer()
    tester.test_scipy_optimizer()
