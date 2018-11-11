"""This module provides dynamic simulation of our system.

It will read initial conditions to set up the system,
it will receive water consumption data from consumers,
it will then iterate forward and recalculate the optimal solutions,
it will write the system state to a data file continuously.
"""

import os
import subprocess
import datetime
from collections import OrderedDict

import blueark.equations_parsing as equ_parse
from blueark.model.sample_model import Model2

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../../'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

CPP_EXE_FILE_NAME = 'main'
CPP_EXE_FILE_PATH = os.path.join(PROJECT_ROOT,
                                 'blueark/optmization',
                                 CPP_EXE_FILE_NAME)
BOUNDS_FILE_NAME = 'bounds.dat'
MATRIX_FILE_NAME = 'matrix.dat'
CPP_FILE_NAME = 'cpp_out.dat'

VAR_FILE_NAME = 'var_output.dat'
CONS_FILE_NAME = 'consumptions.dat'
OBJ_FILE_NAME = 'objective.dat'


class Simulator:
    def __init__(self, consumer_data, n_steps, data_dir):
        self.n_steps = n_steps
        self.consumer_data = consumer_data
        self.run_dir_path = self.init_data_files(data_dir)

    @staticmethod
    def init_data_files(data_dir):
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        run_data_dir = 'run_{}'.format(get_datetime_tag())
        run_dir_path = os.path.join(data_dir, run_data_dir)
        os.mkdir(run_dir_path)

        with open(os.path.join(run_dir_path, VAR_FILE_NAME), 'w') as outfile:
            outfile.write('\n')

        with open(os.path.join(run_dir_path, OBJ_FILE_NAME), 'w') as outfile:
            outfile.write('\n')

        with open(os.path.join(run_dir_path, CONS_FILE_NAME), 'w') as outfile:
            outfile.write('\n')

        print('Running in', run_dir_path)
        return run_dir_path

    def execute_main_loop(self):

        model = Model2()

        for step in range(self.n_steps):
            print('Running step', step, '...')

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
                                        os.path.join(self.run_dir_path,
                                                     MATRIX_FILE_NAME))
            all_coefficients = equ_parse.get_all_coefficients(constr_equations)
            bounds_equ_dict = self.create_bounds_equ_dict(bounds,
                                                          all_coefficients)
            equ_parse.write_bounds_file(bounds_equ_dict, turbine_dict,
                                        os.path.join(self.run_dir_path,
                                                     BOUNDS_FILE_NAME),
                                        len(constrains))

            call_cpp_optimizer(CPP_EXE_FILE_PATH,
                               BOUNDS_FILE_NAME,
                               MATRIX_FILE_NAME,
                               self.run_dir_path,
                               CPP_FILE_NAME)

            var_val_dict, object_val = self.parse_cpp_out(self.run_dir_path,
                                                          CPP_FILE_NAME)

            self.update_outfile(current_consumption, var_val_dict, object_val)

    @staticmethod
    def parse_cpp_out(data_dir, cpp_file_name):
        lines = []
        with open(os.path.join(data_dir, cpp_file_name), 'r') as infile:
            for line in infile:
                lines.append(line)

        objec_value = float(lines[0])

        var_val_dict = OrderedDict()
        for item in lines[1:]:
            var_name, value = item.split(',')
            var_val_dict[var_name] = float(value)

        return var_val_dict, objec_value

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
        """Separates the constraint equation into constraint and bound types.

        Bound types: equations with only ONE variable, e.g. x <= 100
        Constraint type: general equation, e.g. x + 1 = 50
        """
        constraints = []
        bounds = []

        for equ in constr_equations:
            if '+' not in equ:
                bounds.append(equ)
            else:
                constraints.append(equ)
        return constraints, bounds

    def update_outfile(self, current_consumption, var_val_dict, object_val):

        with open(os.path.join(self.run_dir_path, CONS_FILE_NAME), 'a') as out:
            values = [str(item) for item in list(current_consumption.values())]
            out.write(' '.join(values) + '\n')

        with open(os.path.join(self.run_dir_path, OBJ_FILE_NAME), 'a') as out:
            out.write(str(object_val) + '\n')

        with open(os.path.join(self.run_dir_path, VAR_FILE_NAME), 'a') as out:
            values = [str(item) for item in list(var_val_dict.values())]
            out.write(' '.join(values) + '\n')


def call_cpp_optimizer(exe_path, bounds_file_name,
                       matrix_file_name, data_dir_path, cpp_file_name):
    """Runs a subprocess on the cpp optimizer and gets the """

    if not os.path.isfile(exe_path):
        raise IOError('Cpp executable does not exist, needs to be compiled.')

    call_str = '{} {} {} {}'.format(CPP_EXE_FILE_PATH,
                                    bounds_file_name,
                                    matrix_file_name,
                                    cpp_file_name)

    subprocess.call(call_str, cwd=data_dir_path, shell=True)


def get_datetime_tag():
    """Returns a datetime string in the format SSMMHH_ddmmYY."""

    return datetime.datetime.now().strftime('%H%M%S_%d%m%Y')
