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
            child.propagate_symbols_downstream(self.my_symbol)


class Tank(Entity):
    def __init__(self, children, capacity, load):
        """A tank stores water

        :param children: downstream nodes in the graph
        :param capacity: in liters
        :param load: number of liters of water in the tank
        """
        Entity.__init__(self, children)
        self.capacity = capacity
        self.load = load

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
        lhs = NaryPlus(self.my_symbol)
        child_sum = deepcopy(child_sum)
        child_sum.scalar_mul(2)
        constraint_res += [EqualityConstraint(lhs, child_sum)]
        # capacity constraint
        capacity = NaryPlus(LiteralNode(self.capacity))
        constraint_res += [GreaterThanConstraint(capacity, lhs)]

        return constraint_res, maximizer_res


class Pipe(Entity):
    def __init__(self, children, max_throughput, efficiency, throughput):
        """A pipe route water from one point to another. It can
        generate electricity if it has a generator going through.
        The flow of water flowing through a pipe can be controlled.

        :param children: downstream nodes in the graph
        :param max_throughput: maximum throughput this pipe can support, in
            liters per second (e.g. 50)
        :param efficiency: efficiency of the generator to convert throughput
            into energy
        :param throughput: volume of water going through this pipe, in liters
            per second (e.g. 50). Can not be higher than max_throughput.
        """
        Entity.__init__(self, children)
        self.max_throughput = max_throughput
        self.efficiency = efficiency
        self.throughput = throughput

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
        # self throughput should be sum of child throughputs
        lhs = NaryPlus(self.my_symbol)
        constraint_res += [EqualityConstraint(lhs, child_sum)]
        # contraint capacity
        lhs = NaryPlus(LiteralNode(self.max_throughput))
        rhs = NaryPlus(self.my_symbol)
        constraint_res += [GreaterThanConstraint(lhs, rhs)]

        # add generator power maximizer
        if self.efficiency != 0:
            node = deepcopy(self.my_symbol)
            node.scalar_mul(self.efficiency)
            maximizer_res += [node]

        return constraint_res, maximizer_res


class Source(Entity):
    def __init__(self, child, throughput, is_controlled):
        """A source produces water.

        :param child: downstream node
        :param throughput: volume of produced water, in liters per second
            (e.g. 100)
        :param is_controlled: whether this source can be controlled or is
            natural
        """
        Entity.__init__(self, [child])
        self.throughput = throughput
        self.is_controlled = is_controlled

    def demand_equations(self):
        constraint_res = []
        maximizer_res = []
        for child in self.children:
            constraints, maximizers = child.demand_equations()
            constraint_res += constraints
            maximizer_res += maximizers
        child_sum = NaryPlus(*[child.my_symbol for child in self.children])
        lhs = NaryPlus(self.my_symbol)
        constraint_res += [EqualityConstraint(lhs, child_sum)]

        return constraint_res, maximizer_res


class Consumer(Entity):
    def __init__(self, demand):
        """A consumer requires water.

        :param demand: liters of water per day (e.g. 150)
        """
        Entity.__init__(self, [])
        self.demand = demand

    def demand_equations(self):
        lhs = NaryPlus(self.my_symbol)
        rhs = NaryPlus(LiteralNode(self.demand))
        parent_sum = NaryPlus(*self.parents)
        constraint_res = [EqualityConstraint(lhs, parent_sum)]
        constraint_res += [EqualityConstraint(rhs, lhs)]

        return constraint_res, []
