import os
import numpy as np

EQUALITY_OPERATORS = {'equal': {'val': 0, 'symbol': ' ='},
                      'larger_than': {'val': 1, 'symbol': '>='},
                      'smaller_than': {'val': -1, 'symbol': '<='}}

CALCUlATION_OPERATORS = ['+', '*']
MINUS_SIGN = '-'


def get_equality_type(equation):
    """Parses whether equation is equal, larger than or smaller than type.

    == -> 0
    >= -> 1
    <= -> -1
    """

    potential_equality_operator = equation.split('=')[0][-1] + '='

    for equal_type, type_dict in EQUALITY_OPERATORS.items():
        if potential_equality_operator == type_dict['symbol']:
            return type_dict['val']


def get_rhs_value(equation):
    """Returns the right hand side constant of the equation."""
    return float(equation.split('=')[1])


def get_coefficients(equation):
    """Return a dictionary which holds the variable names and their values."""

    # Get only variable name side and remove potential > or < at the end.
    variable_side = equation.split('=')[0][:-1]
    variable_side = variable_side.replace(' ', '')

    parts = variable_side.split('+')

    coefficients_dict = {}

    for item in parts:
        coefficient_value, coefficient_name = item.split('*')

        coefficients_dict[coefficient_name] = float(coefficient_value)

    return coefficients_dict


def get_all_coefficients(equations):
    """Returns a list of all coefficient names along all equations."""

    coefficient_names = [get_coefficients(equ).keys() for equ in equations]
    flat_names = [name for sub_list in coefficient_names for name in sub_list]

    return sorted(set(flat_names))


def build_matrix(equations, all_coeff_names):
    """Given a list of equations build the matrix and target vector."""

    matrix = []
    rhs_vector = []
    equality_type_vector = []

    sorted_coeff_names = sorted(all_coeff_names)
    coeff_indices = {name: idx for idx, name in enumerate(sorted_coeff_names)}
    n_coefficients = len(sorted_coeff_names)

    for equ in equations:
        equality_type_vector.append(get_equality_type(equ))
        rhs_vector.append(get_rhs_value(equ))

        coefficients_dict = get_coefficients(equ)

        matrix_row = n_coefficients * [0.0]
        for name, value in coefficients_dict.items():
            matrix_row[coeff_indices[name]] = value

        matrix.append(matrix_row)

    return matrix, rhs_vector, equality_type_vector, sorted_coeff_names


def write_bounds_file(bounds_equ_dict, turbine_params, file_path):
    """Writes the parameter bounds to file.

    Format
    ------
    col1: lower_bound
    col2: upper_bound
    col3: var_name
    col4: turbine_efficiency
    rows: represent a variable
    """

    assert len(turbine_params) == len(bounds_equ_dict.keys())
    with open(file_path, 'w') as outfile:
        idx = 0
        for var, value in bounds_equ_dict.items():
            outfile.write(' '.join(['0', str(value), var, str(turbine_params[idx])]) + '\n')
            idx += 1


def write_matrix_file(matrix, equ_vec, rhs_vec, file_path):
    """Stores the constraint equation matrix, the equality and rhs vectors.

    Format
    ------
    left m x n part: constraint matrix, m equations, n variables
    then: one col representing equality vector
    then: one col representing right hand side vector
    """
    stacked = np.hstack((np.array(matrix),
                         np.array([equ_vec]).transpose(),
                         np.array([rhs_vec]).transpose()))

    with open(os.path.join(file_path), 'w') as outfile:
        np.savetxt(outfile, stacked, '%5.3f')

