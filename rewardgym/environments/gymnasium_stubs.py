import numpy as np


class Env:
    def __init__(self):
        pass


class Discrete:
    def __init__(self, n_states):
        self.n_states = n_states

        return np.arange(n_states)
