import os


import subprocess


def call_cpp_optimizer(exe_path, bounds_file_name,
                       matrix_file_name, data_dir_path):
    """Runs a subprocess on the cpp optimizer and gets the """

    if not os.path.isfile(exe_path):
        raise IOError('Cpp executable does not exist, needs to be compiled.')

    try:
        call_str = ' '.join([exe_path, '<', bounds_file_name,
                                       '<', matrix_file_name])

        print(call_str)

        # cpp_out = check_output(call_str, shell=True, cwd=data_dir_path)

        output = subprocess.check_output(call_str.split(), stderr=subprocess.STDOUT)


        #print(cpp_out.decode("ascii"))
        return output

    except subprocess.CalledProcessError as e:
        print("Cpp stdout output:\n"), e.output

