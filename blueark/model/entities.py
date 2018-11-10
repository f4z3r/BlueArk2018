from blueark.equations import *
import abc
from copy import deepcopy


class Entity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, children):
        """An entity is a node in the graph, it is connected
        to several downstream children entities, it has a symbolic
        demand in water
        :param children: downstream nodes in the graph
        """
        self.children = children
        # initially empty, will be filled afterwards by
        # propagate_symbols_downstream
        self.parents = set()
        self.my_symbol = SymbolicNode(SymbolGenerator.gen())

    def get_symbol(self):
        return deepcopy(self.my_symbol)

    @abc.abstractmethod
    def demand_equations(self):
        """The demand carried by this node as an EvalNode instance"""
        pass

    def propagate_symbols_downstream(self, parent_symbol=None):
        """Finishes to initialize the graph by propagating parent symbols
        to child nodes

        :param parent_symbol Symbol pushed by parent node
        """
        if parent_symbol is not None:
            self.parents.add(parent_symbol)
        for child in self.children:
            child.propagate_symbols_downstream(self.get_symbol())



class Tank(Entity):
    def __init__(self, children, capacity):
        """A tank stores water

        :param children: downstream nodes in the graph
        :param capacity: in liters
        """
        Entity.__init__(self, children)
        self.capacity = capacity

    def demand_equations(self):
        constraint_res = []
        maximizer_res = []
        for child in self.children:
            constraints, maximizers = child.demand_equations()
            constraint_res += constraints
            maximizer_res += maximizers
        # throughput constraint
        child_sum = NaryPlus(*[child.my_symbol for child in self.children])
        parent_sum = NaryPlus(*self.parents)
        constraint_res += [EqualityConstraint(child_sum, parent_sum)]
        # level constraint
        child_sum = deepcopy(child_sum)
        child_sum.scalar_mul(2)
        constraint_res += [EqualityConstraint(self.get_symbol(), child_sum)]
        # capacity constraint
        capacity = LiteralNode(self.capacity)
        constraint_res += [GreaterThanConstraint(capacity, self.get_symbol())]

        return constraint_res, maximizer_res


class Pipe(Entity):
    def __init__(self, children, max_throughput, efficiency):
        """A pipe route water from one point to another. It can
        generate electricity if it has a generator going through.
        The flow of water flowing through a pipe can be controlled.

        :param children: downstream nodes in the graph
        :param max_throughput: maximum throughput this pipe can support, in
            liters per second (e.g. 50)
        :param efficiency: efficiency of the generator to convert throughput
            into energy
        """
        Entity.__init__(self, children)
        self.max_throughput = max_throughput
        self.efficiency = efficiency

    def demand_equations(self):
        constraint_res = []
        maximizer_res = []
        for child in self.children:
            constraints, maximizers = child.demand_equations()
            constraint_res += constraints
            maximizer_res += maximizers
        # throughput constraint
        child_sum = NaryPlus(*[child.my_symbol for child in self.children])
        parent_sum = NaryPlus(*self.parents)
        constraint_res += [EqualityConstraint(child_sum, parent_sum)]
        # contraint capacity
        lhs = LiteralNode(self.max_throughput)
        constraint_res += [GreaterThanConstraint(lhs, self.get_symbol())]

        # add generator power maximizer
        if self.efficiency != 0:
            node = deepcopy(self.get_symbol())
            node.scalar_mul(self.efficiency)
            maximizer_res += [node]

        return constraint_res, maximizer_res


class Source(Entity):
    def __init__(self, child, throughput=None):
        """A source produces water.

        :param child: downstream node
        :param throughput: volume of produced water, in liters per second
            (e.g. 100)
        """
        Entity.__init__(self, [child])
        self.throughput = throughput

    def demand_equations(self):
        constraint_res = []
        maximizer_res = []
        for child in self.children:
            constraints, maximizers = child.demand_equations()
            constraint_res += constraints
            maximizer_res += maximizers
        child_sum = NaryPlus(*[child.my_symbol for child in self.children])
        constraint_res += [EqualityConstraint(self.get_symbol(), child_sum)]
        if self.throughput is not None:
            constraint_res += [EqualityConstraint(
                self.get_symbol(), LiteralNode(self.throughput))]

        return constraint_res, maximizer_res


class Consumer(Entity):
    def __init__(self, demand):
        """A consumer requires water.

        :param demand: liters of water per day (e.g. 150)
        """
        Entity.__init__(self, [])
        self.demand = demand

    def demand_equations(self):
        rhs = LiteralNode(self.demand)
        parent_sum = NaryPlus(*self.parents)
        constraint_res = [EqualityConstraint(self.get_symbol(), parent_sum)]
        constraint_res += [EqualityConstraint(rhs, self.get_symbol())]

        return constraint_res, []
