"""This module provides dynamic simulation of our system.

It will read initial conditions to set up the system,
it will receive water consumption data from consumers,
it will then iterate forward and recalculate the optimal solutions,
it will write the system state to a data file continuously.
"""

import os

import blueark.simulation.optimizationwrapper as cpp_wrapper

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CPP_EXE_FILE_NAME = 'main'
BOUNDS_FILE_NAME = 'bounds.dat'
MATRIX_FILE_NAME = 'matrix.dat'


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

        # TODO: In creation.s
        model = None

        consumation = self.get_consumation_for_day(0)
        model.build_first_time(consumation)

        model.get_equations()

        for day in range(1, self.n_days):
            cpp_out = self.run_optimization()
            consumation = self.get_consumation_for_day(day)
            model.rebuild(consumation, None)

    def run_optimization(self):

        exe_path = os.path.join(self.data_dir, CPP_EXE_FILE_NAME)
        cpp_out = cpp_wrapper.call_cpp_optimizer(exe_path, BOUNDS_FILE_NAME,
                                                 MATRIX_FILE_NAME, DATA_DIR)
        pass

    def update_state(self, iter_output):
        raise NotImplementedError

    def get_consumation_for_day(self, day):
        return {name: cons[day] for name, cons in self.consumer_data.items()}


class SystemState:

    def __init__(self, all_consumptions, time_step):
        self.all_consumptions = all_consumptions
        self.time_step = time_step
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

        self.consumptions_one_day = consumer_consumptions
        self.tank_levels = tank_levels
        self.pipe_through_puts = pipe_throughput
        self.drainer_outlet = drainer_outlet
        self.source_input = source_input

    def append_state_to_file(self):
        raise NotImplementedError

    def init_state_file(self):
        raise NotImplementedError
