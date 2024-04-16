"""
    Stubs, so that environments can be used together with PsychoPy, not requiring
    any installation of other packages into the PsychoPy env.
"""
import numpy as np


class Env:
    def __init__(self):
        pass


class Discrete:
    def __init__(self, n_states):
        self.n_states = n_states


class Surface:
    pass


class Clock:
    pass
