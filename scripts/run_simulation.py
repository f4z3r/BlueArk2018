import os
import sys

from blueark.simulation.data_augmentation import DataAugmenter
from blueark.simulation.simulator import Simulator

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

N_CONSUMERS = 5
N_TIME_STEPS = 1000


def main():

    data_maker = DataAugmenter(N_CONSUMERS, N_TIME_STEPS)

    all_consumptions = data_maker.generate_consumptions()

    simulation = Simulator(all_consumptions,
                           N_TIME_STEPS, DATA_DIR)

    simulation.execute_main_loop()


if __name__ == '__main__':
    main()
