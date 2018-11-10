import os

from blueark.simulation.data_augmentation import DataAugmenter
from blueark.simulation.simulator import Simulator
from blueark.simulation.simulator import SystemState

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
N_CONSUMERS = 5
N_TIME_STEPS = 100


def main():

    data_maker = DataAugmenter(N_CONSUMERS, N_TIME_STEPS)

    all_consumptions = data_maker.generate_consumptions()

    initial_state = SystemState(all_consumptions, 0)

    simulation = Simulator(initial_state, all_consumptions,
                           N_TIME_STEPS, DATA_DIR)

    simulation.execute_main_loop()


if __name__ == '__main__':
    main()
