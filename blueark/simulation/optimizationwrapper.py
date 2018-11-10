import os


import subprocess
from subprocess import check_output
from subprocess import Popen, PIPE


def call_cpp_optimizer(exe_path, bounds_file_name,
                       matrix_file_name, data_dir_path):
    """Runs a subprocess on the cpp optimizer and gets the """

    if not os.path.isfile(exe_path):
        raise IOError('Cpp executable does not exist, needs to be compiled.')

    try:
        call_str = ' '.join([exe_path, '<', bounds_file_name,
                                       '<', matrix_file_name])

        print(call_str)
        p = Popen(call_str, shell=True, cwd=data_dir_path,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)

        cpp_out, err = p.communicate(
            b"input data that is passed to subprocess' stdin")
        rc = p.returncode

        # cpp_out = check_output(call_str, shell=True, cwd=data_dir_path)

        return cpp_out

    except subprocess.CalledProcessError as e:
        print("Cpp stdout output:\n"), e.output

