import blueark.equations as equations
import abc


class Entity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, children):
        """An entity is a node in the graph, it is connected
        to several downstream children entities, it has a symbolic
        demand in water
        :param children: downstream nodes in the graph
        """
        self.children = children

    @abc.abstractmethod
    def demand_equations(self):
        """The demand carried by this node as an EvalNode instance"""
        return

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


class Pipe(Entity):
    def __init__(self, children, max_throughput, max_power, throughput):
        """A pipe route water from one point to another. It can
        generate electricity if it has a generator going through.
        The flow of water flowing through a pipe can be controlled.

        :param children: downstream nodes in the graph
        :param max_throughput: maximum throughput this pipe can support, in liters per second (e.g. 50)
        :param max_power: maximum electric power produced by the generator in kW (e.g. 225 kW)
        :param throughput: volume of water going through this pipe, in liters per second (e.g. 50). Can not be higher than max_throughput.
        """
        Entity.__init__(self, children)
        self.max_throughput = max_throughput
        self.max_power = max_power
        self.throughput = throughput

    def demand_equations(self):
        if self.max_power != 0:
            k = self.throughput * self.max_power / self.max_throughput
            eqs = []
            for child in self.children:
                eqs.extend(list(map(lambda eq: eq.scalar_mul(k), child.demand_equations())))
            return eqs
        else:
            eqs = []
            for child in self.children:
                eqs.extend(child.demand_equations())
            return eqs


class Source(Entity):
    def __init__(self, child, throughput, is_controlled):
        """A source produces water.

        :param child: downstream node
        :param throughput: volume of produced water, in liters per second (e.g. 100)
        :param is_controlled: whether this source can be controlled or is natural
        """
        Entity.__init__(self, [child])
        self.throughput = throughput
        self.is_controlled = is_controlled


class Consumer(Entity):
    def __init__(self, demand):
        """A consumer requires water.

        :param demand: liters of water per day (e.g. 150)
        """
        Entity.__init__(self, [])
        self.demand = demand

    def demand_equations(self):
        return [equations.LiteralNode(self.demand)]
