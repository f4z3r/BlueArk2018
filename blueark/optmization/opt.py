import picos as pic
import cvxopt as cvx
import numpy as np

# min 0.5*x1 +  x2
#   s.t. x1 >= x2
#   [1 0      [ 3
#   1 1] x <=   4]

# P = pic.Problem()
# A = pic.new_param('A', cvx.matrix([[1, 1], [0, 1]]))
# x = P.add_variable('x', 2)
# P.add_constraint(x[0] > x[1])
# P.add_constraint(A*x < [3, 4])
# objective = 0.5 * x[0] + x[1]
# P.set_objective('max', objective)  # or directly P.maximize(objective)

# # display the problem and solve it
# P.solve(verbose=0, solver='cvxopt')
# print(P.obj_value())


class OptimizationProblem:
    def __init__(self, num_variables=0, matrix=[], rhs_vector=[],
                 equality_vector=[], objective_function=[]):
        """Wrapper class for picos optimization.

        P = Problem(n=0, A=[], b=[], rel=[], obj=[])
        if all parameters are set under construction,
            one can call solve directly.
        Otherwise, one must do:
            P = Problem()
            P.add_variables(n)
            P.add_constraints(A, b, rel)
            P.set_objective(obj)
            P.solve()
        """
        self.__status = "unsolved"
        self.__value = None
        self.__variables = None

        self.pic_problem = pic.Problem()
        self.matrix = pic.new_param('matrix', cvx.matrix(np.array(matrix)))

        self.objective_function = cvx.matrix(objective_function)
        self.equality_vector = equality_vector
        self.rhs_vector = cvx.matrix(rhs_vector)
        if num_variables > 0:
            self.add_variables(num_variables)
            if matrix and rhs_vector and equality_vector:
                self.add_constraints(self.matrix, self.rhs_vector,
                                     self.equality_vector)

                if objective_function:
                    self.set_objective(self.objective_function)

    @property
    def status(self):
        return self.__status

    @property
    def value(self):
        return self.__value

    @property
    def variables(self):
        return self.__variables

    def add_variables(self, num_vars):
        if num_vars < 1:
            return

        self.__variables = self.pic_problem.add_variable('x', num_vars)

    def add_constraints(self, matrix, rhs_vector, equality_vector):
        """Adds to constraint to the problem using the matrix.

        Arguments
        ---------

        matrix: m x n constraint matrix, where n is the number of variables
                and m is the number of constraints
        rhs_vector: list of length m, the number of constraints,
        equality_vector: list of m integers. The number rel[i] defines the
                         relation, rel[i] < 0, rel[i] == 0, rel[i] > 0
                         gives the sign of the (in)equality

        sum(matrix[i][:]) <= rhs_vector[i], if equ_vector[i] < 0
        sum(matrix[i][:]) == rhs_vector[i], if equ_vector[i] = 0
        """

        num_equ, num_vars = matrix.size
        if not (num_equ == len(rhs_vector) == len(equality_vector)) or \
                num_equ == 0 or \
                num_vars != self.variables.size[0]:

            raise ValueError('Dimensions do not match or are zero. '
                             'A: %ix%i. b: %i. rel: %i'
                             % (num_equ, num_vars,
                                len(rhs_vector), len(equality_vector)))

        rhs_vector = pic.new_param('rhs_vec', rhs_vector)
        equality_vector = np.array(equality_vector)

        # get indices of ineqs and eqs
        inequality_idx = np.where(equality_vector)[0]
        equality_vector[inequality_idx] = 1
        equality_idx = np.where(1 - equality_vector)[0]

        # add lists of constraints

        self.pic_problem.add_list_of_constraints(
            [matrix[int(idx), :] * self.variables == rhs_vector[int(idx)]
                for idx in equality_idx])
        self.pic_problem.add_list_of_constraints(
            [matrix[int(idx), :] * self.variables < rhs_vector[int(idx)]
                for idx in inequality_idx])

        self.matrix = matrix[:]

    def solve(self, verbose=0):
        objective = self.objective_function.T * self.variables
        self.pic_problem.set_objective('max', objective)
        self.pic_problem.solve(verbose=verbose, solver='cvxopt')
        self.__status = self.pic_problem.status
        self.__value = self.pic_problem.obj_value()

    def set_objective(self, coeff_indices):
        if len(coeff_indices) != self.variables.size[0]:
            raise ValueError(
                'Number of coefficients do not match the number of varibles. '
                'Expected %i but received %i'
                % (len(self.variables), len(coeff_indices)))

        for coeff_idx in coeff_indices:
            if type(coeff_idx) is not int and type(coeff_idx) is not float:
                raise ValueError("Expected a real value, got %s",
                                 type(coeff_idx))

        self.objective_function = cvx.matrix(coeff_indices)


"""
P = OptimizationProblem(2)
A = [
    [-1, 1],
    [1, 0],
    [1, 1]


]

A = np.array(A)
b = [0, 3, 4]
rel = [1, 1, 1]

P.add_constraints(A, b, rel)
c = [0.5, 1]
P.set_objective(c)
print(P.solve())
print(P.value)
print(P.status)
print(P.variables)
Q= OptimizationProblem(2, A, b, rel, c)
"""
