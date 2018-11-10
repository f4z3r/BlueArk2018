
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


def build_matrix(equations):
    """Given a list of equations build the matrix and target vector."""

    matrix = []
    rhs_vector = []
    equality_type_vector = []

    sorted_coeff_names = sorted(get_all_coefficients(equations))
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
