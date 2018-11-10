import numpy as np


class DataAugmenter:
    def __init__(self, n_consumer, n_days):
        self.n_consumer = n_consumer
        self.n_days = n_days

    def generate_consumptions(self):

        consumptions = {}

        for idx in range(self.n_consumer):
            consumer = Consumer()
            consumptions[idx] = consumer.create_consumption_data(self.n_days)

        return consumptions

    def store_data_consumptions(self):
        raise NotImplementedError


class Consumer:

    def __init__(self):
        self.MAX_CONSUMPTION = 300
        self.MIN_CONSUMPTION = 100

    def create_consumption_data(self, n_days):
        """Creates water consumption per day."""
        avg_daily_demand = np.random.randint(self.MIN_CONSUMPTION,
                                             self.MAX_CONSUMPTION)

        consumption = self.bounded_random_walk(n_days,
                                               self.MIN_CONSUMPTION,
                                               self.MAX_CONSUMPTION,
                                               avg_daily_demand,
                                               avg_daily_demand,
                                               5)

        return consumption

    @staticmethod
    def bounded_random_walk(length, lower_bound, upper_bound, start, end, std):
        """Creates random walk data bounded by lower and upper bound with
        spcified start and end value as well as standard deviation."""
        assert (lower_bound <= start and lower_bound <= end)
        assert (start <= upper_bound and end <= upper_bound)

        bounds = upper_bound - lower_bound

        rand = (std * (np.random.random(length) - 0.5)).cumsum()
        rand_trend = np.linspace(rand[0], rand[-1], length)
        rand_deltas = (rand - rand_trend)
        rand_deltas /= np.max(
            [1, (rand_deltas.max() - rand_deltas.min()) / bounds])

        trend_line = np.linspace(start, end, length)
        upper_bound_delta = upper_bound - trend_line
        lower_bound_delta = lower_bound - trend_line

        upper_slips_mask = (rand_deltas - upper_bound_delta) >= 0
        upper_deltas = rand_deltas - upper_bound_delta
        rand_deltas[upper_slips_mask] = (upper_bound_delta - upper_deltas)[
            upper_slips_mask]

        lower_slips_mask = (lower_bound_delta - rand_deltas) >= 0
        lower_deltas = lower_bound_delta - rand_deltas
        rand_deltas[lower_slips_mask] = (lower_bound_delta + lower_deltas)[
            lower_slips_mask]

        return trend_line + rand_deltas
