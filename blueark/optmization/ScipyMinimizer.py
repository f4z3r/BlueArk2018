import numpy as np

from scipy.optimize import LinearConstraint
from scipy.optimize import minimize
from scipy.optimize import Bounds


class ScipySolver:

    def __init__(self, turbine_params, matrix, low_bounds, upper_bounds,
                 rhs_vec, equ_vec, init_guess):
        self.turbine_params = turbine_params
        self.matrix = matrix
        self.rhs_vec = rhs_vec
        self.equ_vec = equ_vec
        self.init_guess = init_guess
        self.low_bounds = low_bounds
        self.upper_bounds = upper_bounds

    def define_linear_constraints(self):
        """Only usable if we get Jacobian."""
        lower_bound = []
        for idx, equ_val in enumerate(self.equ_vec):
            if equ_val == 0:
                lower_bound.append(self.rhs_vec[idx])
            else:
                lower_bound.append(-np.inf)
        upper_bound = self.rhs_vec

        return LinearConstraint(self.matrix, lower_bound, upper_bound)

    @staticmethod
    def linear_constraints_dict(flow_values, turbine_params, matrix, rhs_vec,
                                equ_vec):
        """Deprecated."""
        constraints = []
        for mat_row, equ_val in zip(matrix, equ_vec):
            constraint = 0.0
            for turb_value, flow_value, rhs_val in \
                    zip(turbine_params, flow_values, rhs_vec):
                constraint += turb_value * flow_value - rhs_val

            if equ_val == 0:
                equ_type = 'eq'
            else:
                equ_type = 'ineq'

            def constr_func():
                return constraint

            constraints.append({'type': equ_type, 'func': constr_func()})
        return constraints

    def init_constraint_list(self):
        """Returns a list of dicts representing constraints."""
        constraints = []
        for row, equ_val, rhs_val in \
                zip(self.matrix, self.equ_vec, self.rhs_vec):

            constraints.append({'type': self.get_eq_type(equ_val),
                                'fun': lambda x: rhs_val - np.dot(row, x)})

        bounds = Bounds(self.low_bounds, self.upper_bounds)

        return constraints, bounds

    def solve(self):
        """Creates list of scipy.optimize constraints and solves the system.

        Returns
        -------
        result: an OptimizedResult objects holding information about optimizer
        """

        constrains, bounds = self.init_constraint_list()
        result = minimize(self.objective_function,
                          x0=self.init_guess,
                          constraints=constrains,
                          bounds=bounds,
                          options={'disp': True})

        return result

    def objective_function(self, flow_values):
        """Objective function which will be minimized.

        The objective function is the sum of all multiplications of
        turbine efficiencies with the corresponding flows through that turbine.
        """

        objective_value = -1.0 * np.dot(self.turbine_params, flow_values)
        print(-1.0*objective_value)

        return objective_value

    @staticmethod
    def get_eq_type(equ_val):
        """TODO: Replace with hard coded dict constant after merge."""
        if equ_val == 0:
            return 'eq'
        else:
            return 'ineq'
