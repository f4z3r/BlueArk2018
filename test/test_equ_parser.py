#!/usr/bin/env python3

"""Tests the equations parser."""

import os
import unittest
import tempfile
import csv

import numpy as np

from blueark.equations_parsing import *


class TestEquationParsing(unittest.TestCase):

    def test_get_equality_type(self):
        """Given an equality, what is the type.

        == -> 0
        >= -> 1
        <= -> -1
        """

        equ1 = '1.0 * x + 2.0 * y = 5.0'
        equ2 = '2.1 * 2.0 * z <= -10.0'
        equ3 = '1.0 * u + 1.0 * r >= 3.0'

        self.assertEqual(get_equality_type(equ1), 0)
        self.assertEqual(get_equality_type(equ2), -1)
        self.assertEqual(get_equality_type(equ3), 1)

    def test_get_coefficients(self):
        """Tests correctness of coefficients parsed from equation."""

        equ = '1.1 * x_var + 2.0 * y + 1.0 * z = 5.0'
        result = {'x_var': 1.1, 'y': 2.0, 'z': 1.0}

        self.assertEqual(get_coefficients(equ), result)

    def test_get_rhs_value(self):
        """Tests the parsing of the right hand side const of the equation."""

        equ1 = '1.0 * x + 2.5 * y = 1.0'
        equ2 = '1.0 * x + 2.5 * y = 1.5'
        equ3 = '1.0 * x + 2.5 * y = -1.0'
        equ4 = '1.0 * x + 2.5 * y = -1.5'

        self.assertEqual(get_rhs_value(equ1), 1.0)
        self.assertEqual(get_rhs_value(equ2), 1.5)
        self.assertEqual(get_rhs_value(equ3), -1.0)
        self.assertEqual(get_rhs_value(equ4), -1.5)

    def test_get_all_coefficients(self):
        equ1 = '1.1 * x_var_1 + 2.0 * y + 1.0 * z = 5.0'
        equ2 = '1.1 * u_var + 2.0 * y = 10.0'

        self.assertEqual(get_all_coefficients([equ1, equ2]),
                         sorted({'x_var_1', 'u_var', 'y', 'z'}))

    def test_build_matrix(self):
        equ1 = '1.1 * a + 2.0 * b + 1.0 * c = 5.0'
        equ2 = '2.1 * a + 2.0 * d = 10.0'

        expected_matrix = [[1.1, 2.0, 1.0, 0.0], [2.1, 0.0, 0.0, 2.0]]

        matrix, rhs_vec, equ_vec, sorted_coeffs = build_matrix([equ1, equ2])

        self.assertEqual(matrix, expected_matrix)

    def test_write_bounds_file(self):

        bounds_equ = {'x': 80, 'y': 100, 'z_val': 150}
        turbine_params = [0.8, 0.0, 0.0]

        with tempfile.TemporaryDirectory() as tmpdirpath:
            file_path = os.path.join(tmpdirpath, 'bounds.dat')
            write_bounds_file(bounds_equ, turbine_params, file_path)

            read_dict = {}
            read_turbine_params = []
            with open(file_path, 'r') as infile:
                for line in infile:
                    splitted = line.split(' ')
                    read_dict[splitted[2]] = int(splitted[1])
                    read_turbine_params.append(float(splitted[3]))

            self.assertEqual(bounds_equ, read_dict)
            self.assertEqual(read_turbine_params, turbine_params)

    def test_write_matrix_file(self):

        matrix = np.random.randint(10, size=(5, 4))
        equ_vec = np.random.randint(2, size=(5,))
        rhs_vec = np.random.randint(10, size=(5,))

        with tempfile.TemporaryDirectory() as tmpdirpath:
            file_path = os.path.join(tmpdirpath, 'matrix.dat')
            write_matrix_file(matrix, equ_vec, rhs_vec, file_path)
            
            pass


if __name__ == '__main__':
    tester = TestEquationParsing()
    tester.test_write_matrix_file()
