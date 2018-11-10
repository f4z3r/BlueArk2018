import numpy as np


def load_data(data_path):
    return np.genfromtxt(data_path)

def store_system_state():
    raise NotImplementedError