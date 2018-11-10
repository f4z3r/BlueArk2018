"""This module provides dynamic simulation of our system.

It will read initial conditions to set up the system,
it will receive water consumption data from consumers,
it will then iterate forward and recalculate the optimal solutions,
it will write the system state to a data file continuously.
"""

import os

import blueark.simulation.optimizationwrapper as cpp_wrapper
import blueark.equations_parsing as equ_parse
from blueark.model.sample_model import Model2

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, '..', 'data')
CPP_EXE_FILE_NAME = 'main'
CPP_EXE_FILE_PATH = os.path.join(PROJECT_ROOT,
                                 'optmization',
                                 CPP_EXE_FILE_NAME)
BOUNDS_FILE_NAME = 'bounds.dat'
MATRIX_FILE_NAME = 'matrix.dat'

OUT_FILE_NAME = 'output.dat'


class Simulator:
    def __init__(self, initial_state, consumer_data, n_steps, data_dir):
        self.system_state = initial_state
        self.n_steps = n_steps
        self.consumer_data = consumer_data
        self.data_dir = self._init_data_dir(data_dir)

    @staticmethod
    def _init_data_dir(data_dir):
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        with open(os.path.join(data_dir, OUT_FILE_NAME), 'w') as outfile:
            outfile.write('### FINAL DATA OUTPU ###' + '\n')

        return data_dir

    def execute_main_loop(self):

        model = Model2()

        for step in range(self.n_steps):
            current_consumption = self._consumation_on_day(step)

            model.set_consumer_usage(*list(current_consumption.values()))

            constr_equations, turbine_list = model.gen_constraints()

            constrains, bounds = self.filter_equations(constr_equations)

            all_var_names = equ_parse.get_all_coefficients(constr_equations)
            turbine_dict = Simulator.create_turbine_dict(turbine_list,
                                                         all_var_names)

            matrix, rhs_vec, equ_vec, sort_coeffs = \
                equ_parse.build_matrix(constr_equations)

            equ_parse.write_matrix_file(matrix, equ_vec, rhs_vec,
                                        os.path.join(DATA_DIR,
                                                     MATRIX_FILE_NAME))

<<<<<<< HEAD
            bounds_equ_dict = self.create_bounds_equ_dict(bounds, all_var_names)

            equ_parse.write_bounds_file(bounds_equ_dict, turbine_dict,
                                        os.path.join(DATA_DIR, BOUNDS_FILE_NAME),
                                        len(constrains))

            cpp_out = cpp_wrapper.call_cpp_optimizer(CPP_EXE_FILE_PATH,
                                                     BOUNDS_FILE_NAME,
                                                     MATRIX_FILE_NAME,
                                                     DATA_DIR)

            self.system_state.update(cpp_out, current_consumption,
                                     all_var_names)
=======
            bounds_equ_dict = self.create_bounds_equ_dict(bounds, all_coefficients)
            equ_parse.write_bounds_file(bounds_equ_dict, turbine_dict,
                                        os.path.join(DATA_DIR, BOUNDS_FILE_NAME))

            cpp_out = cpp_wrapper.call_cpp_optimizer(CPP_EXE_FILE_PATH,
                                                      BOUNDS_FILE_NAME,
                                                      MATRIX_FILE_NAME,
                                                      DATA_DIR)

            self.system_state.update(cpp_out, current_consumption)

    def _consumation_on_day(self, step):
        return {name: cons[step] for name, cons in self.consumer_data.items()}

    @staticmethod
    def create_turbine_dict(turbine_list, all_coefficients):

        turbine_dict = {}

        for item in turbine_list:
            value, ending = item.split('*')
            turbine_dict[ending.strip()] = float(value)

        for name in all_coefficients:
            if name not in turbine_dict.keys():
                turbine_dict[name] = 0.0

        return turbine_dict

    @staticmethod
    def parse_cpp_out(cpp_out):
        objective_value = cpp_out[0]

        var_value_dict = {}
        for line in cpp_out[1:]:
            var_name, value = line.split(',')
            var_value_dict[var_name] = value

        return objective_value, var_value_dict

    @staticmethod
    def create_bounds_equ_dict(bounds_equ, all_coefficients):
        """From raw list of bounds equations, create a bounds dict."""

        upper_bound_dict = {}

        for equ in bounds_equ:
            first_part = equ.split('=')[0][:-1].strip()
            factor = float(first_part.split('*')[0].strip())
            name = first_part.split('*')[1].strip()
            upper_bound = float(equ.split('=')[1].strip()) / factor

            upper_bound_dict[name] = upper_bound

        for name in all_coefficients:
            if name not in upper_bound_dict:
                upper_bound_dict[name] = -1.0
        return upper_bound_dict

    @staticmethod
    def filter_equations(constr_equations):
        constraints = []
        bounds = []

        for equ in constr_equations:
            if '+' not in equ:
                bounds.append(equ)
            else:
                constraints.append(equ)
        return constraints, bounds

    def update_outfile(self, parsed_cpp_out, current_consumption, all_names):
        title_names = all_names + 'object_value'


class SystemState:

    def __init__(self, current_consumption, time_step):
        self.current_consumation = current_consumption
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

        self.current_consumation = consumer_consumptions
        self.tank_levels = tank_levels
        self.pipe_through_puts = pipe_throughput
        self.drainer_outlet = drainer_outlet
        self.source_input = source_input
        self.append_state_to_file()

    def update(self, parsed_cpp_out, current_consumption, all_names):
        self.current_consumation = current_consumption


    def parse_cpp_out(self, cpp_out):
        objective_value = cpp_out[0]

        variables = {}
        for line in cpp_out[1:]:
            var_name, value = line.split(',')
            variables[var_name] = value

    def append_state_to_file(self):
        raise NotImplementedError

    def init_state_file(self):
        raise NotImplementedError
