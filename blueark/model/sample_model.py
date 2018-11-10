#!/usr/env/python3 -O

"""Sample model."""

from blueark.model.entities import *

class Model:
    def __init__(self):
        self.consumers = [
            Consumer(0),           # x_0
            Consumer(0),           # x_1
            Consumer(0),           # x_2
            Consumer(0),           # x_3
            Consumer(0),           # x_4
            Consumer(0),           # x_5
        ]
        # x_6
        self.bottom_tank = Tank([self.consumers[0],
                                 self.consumers[1],
                                 self.consumers[2]], 1500)
        # x_7
        self.pipe_bottom_left = Pipe([self.bottom_tank], 600, 0)
        # x_8
        self.pipe_bottom_left = Pipe([self.bottom_tank], 400, 0)
        # x_9
        self.tank_left_bottom = Tank([self.pipe_bottom_left,
                                      self.consumers[3]], 3000)
        # x_10
        self.pipe_middle_left = Pipe([self.tank_left_bottom], 800, 60)
        # x_11
        self.tank_left_top = Tank([self.pipe_middle_left, self.consumers[4]],
                                  3000)
        # x_12
        self.pipe_top_left = Pipe([self.tank_left_top], 1000, 40)
        # x_13
        self.tank_right = Tank([self.bottom_tank, self.consumers[5]], 1000)
        # x_14
        self.pipe_right = Pipe([self.tank_right], 700, 20)
        # x_15
        self.tank_top = Tank([self.pipe_top_left, self.pipe_right], 3000)
        # x_16
        self.natural_source = Source(self.tank_top, throughput=600)
        # x_17
        self.controlled_source = Source(self.tank_top)

    def set_consumer_usage(self, *weights):
        """Sets the cunsumer usage metrics for the current day."""
        if len(weights) != 6:
            raise ValueError("Input weights should be of length 6")
        for idx, weight in enumerate(weights):
            self.consumers[idx].demand = weight

    def gen_constraints(self):
        """Retrieves the constraints on the model and the maximisation
        requirements."""
        self.natural_source.propagate_symbols_downstream()
        self.controlled_source.propagate_symbols_downstream()
        constraints1, maximizers1 = self.natural_source.demand_equations()
        constraints2, maximizers2 = self.controlled_source.demand_equations()
        constraints = set(constraints1).union(set(constraints2))
        constraints = [str(constraint) for constraint in constraints]
        maximizers = maximizers1 + maximizers2
        maximizers = [str(maximizer) for maximizer in maximizers]
        return constraints, maximizers



