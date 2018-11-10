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


class Problem():
    def __init__(self, n=0, A=[], b=[], rel=[], obj=[]):
        """
        P = Problem(n=0, A=[], b=[], rel=[], obj=[])
        if all parameters are set under construction, one can call solve directly.
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

        self.prob = pic.Problem()
        self.X = []  # variables
        self.A = cvx.matrix(A)
        self.obj = cvx.matrix(obj)
        self.rel = rel
        self.b = cvx.matrix(b)
        if n > 0:
            self.add_variables(n)
            if A and b and rel:
                self.add_constraints(self.A, self.b, self.rel)

                if obj:
                    self.set_objective(self.obj)

    @property
    def status(self):
        return self.__status

    @property
    def value(self):
        return self.__value

    @property
    def variables(self):
        return self.__variables

    def add_variables(self, n):
        if n < 1:
            return

        self.X = self.prob.add_variable('x', n)
        self.__variables = self.X

    def add_constraints(self, A, b, rel):
        """
        A: m x n constraint matrix, where n is the number of variables and m is the number of constraints
        b: list of length m, the number of constraints,
        rel: list of m integers. The number rel[i] defines the relation, rel[i] < 0, rel[i] == 0, rel[i] > 0 gives the sign of the (in)equality

        sum(A[i][:]) <= b[i], if rel[i] < 0
        sum(A[i][:]) == b[i], if rel[i] = 0
        sum(A[i][:]) >= b[i], if rel[i] > 0
        """

        if type(A) is not cvx.matrix:
            A = cvx.matrix(A)

        m, n = A.size
        if not (m == len(b) == len(rel)) or m == 0 or n != self.X.size[0]:
            raise ValueError('Dimensions do not match or are zero. A: %ix%i. b: %i. rel: %i' % (
                m, n, len(b), len(rel)))

        self.A = A[:]
        for i in range(m):
            # m constraints
            a = A[i, :]
            if rel[i] < 0:
                self.prob.add_constraint(a * self.X < b[i])
            elif rel[i] > 0:
                self.prob.add_constraint(a * self.X > b[i])
            else:
                self.prob.add_constraint(a * self.X == b[i])

    def solve(self, verbose=0):
        objective = self.obj.T * self.X
        self.prob.set_objective('max', objective)
        self.prob.solve(verbose=verbose, solver='cvxopt')
        self.__status = self.prob.status
        self.__value = self.prob.obj_value()
        return self.prob.objective

    def set_objective(self, coeffs):
        if len(coeffs) != self.X.size[0]:
            raise ValueError(
                'Number of coefficients do not match the number of varibles. Expected %i but received %i' % (len(self.X), len(coeffs)))

        for i in coeffs:
            if type(i) is not int and type(i) is not float:
                raise ValueError("Expected a real value, got %s", type(i))
        self.obj = cvx.matrix(coeffs)


P = Problem(2)
A = [
    [1, -1],
    [1, 0],
    [1, 1]
]

A = np.array(A)
b = [0, 3, 4]
rel = [1, -1, -1]

P.add_constraints(A, b, rel)
c = [0.5, 1]
P.set_objective(c)
print(P.solve())
print(P.value)
print(P.status)
print(P.variables)
