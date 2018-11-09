class Entity:
    def __init__(self, parents):
        self.parents = parents


class Tank(Entity):
    def __init__(self, parents, capacity, load):
        Entity.__init__(self, parents)
        self.capacity = capacity
        self.load = load


class Pipe(Entity):
    def __init__(self, parents, capacity, efficiency, throughput):
        Entity.__init__(self, parents)
        self.capacity = capacity
        self.efficiency = efficiency
        self.throughput = throughput


class Source(Entity):
    def __init__(self, parents, throughput, isControlled):
        Entity.__init__(self, parents)
        self.throughput = throughput
        self.isControlled = isControlled


class Consumer(Entity):
    def __init__(self, parents, demand):
        Entity.__init__(self, parents)
        self.demand = demand

