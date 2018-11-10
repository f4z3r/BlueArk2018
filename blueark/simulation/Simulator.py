"""This module provides dynamic simulation of our system.

It will read initial conditions to set up the system,
it will receive water consumption data from consumers,
it will then iterate forward and recalculate the optimal solutions.
"""

import os


class Simulator:
    def __init__(self, initial_state, consumer_data, n_days, data_dir):
        self.system_state = initial_state
        self.n_days = n_days
        self.consumer_data = consumer_data
        self.data_dir = self._init_data_dir(data_dir)

    @staticmethod
    def _init_data_dir(data_dir):
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    def execute_main_loop(self):

        model = ModelBuilder()

        consumation = self.get_consumation_for_day(0)
        model.build_first_time(consumation)

        for day in range(1, self.n_days):
            system_state = None
            consumation = self.get_consumation_for_day(day)
            model.rebuild(consumation, system_state)

    def update_state(self, iter_output):
        raise NotImplementedError

    def get_consumation_for_day(self, day):
        return {name: cons[day] for name, cons in self.consumer_data.items()}

class ModelBuilder:

    def build_first_time(self, day_consumptions):
        raise NotImplementedError


class SystemState:

    def __init__(self):
        self.consumer_consumptions = {}
        self.tank_levels = {}
        self.pipe_through_puts = {}
        self.drainer_outlet = {}
        self.source_input = {}

    def set_system_state(self,
                         consumer_consumptions,
                         tank_levels,
                         pipe_throughput,
                         drainer_outlet,
                         source_input):

        self.append_state_to_file()

        self.consumer_consumptions = consumer_consumptions
        self.tank_levels = tank_levels
        self.pipe_through_puts = pipe_throughput
        self.drainer_outlet = drainer_outlet
        self.source_input = source_input

    def append_state_to_file(self):
        raise NotImplementedError

    def init_state_file(self):
        raise NotImplementedError





