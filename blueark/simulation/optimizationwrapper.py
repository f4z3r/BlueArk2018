import os


import subprocess
from subprocess import check_output


def call_cpp_optimizer(exe_path, bounds_file_name,
                       matrix_file_name, data_dir_path):
    """Runs a subprocess on the cpp optimizer and gets the """

    if not os.path.exists(exe_path):
        raise IOError('Cpp executable does not exist, needs to be compiled.')

    try:
        call_str = ' '.join([exe_path, '<', bounds_file_name,
                                       '<', matrix_file_name])

        cpp_out = check_output(call_str, shell=True, cwd=data_dir_path)

        return cpp_out

    except subprocess.CalledProcessError as e:
        print("Cpp stdout output:\n"), e.output


def parse_cpp_out(cpp_stdout):

    objective_value = cpp_stdout[0]

    var_flows = {}
    for line in cpp_stdout[1:]:
        var_name, flow_val = line.split(',')

    return var_flows
