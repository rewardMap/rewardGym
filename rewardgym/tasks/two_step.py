from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import BaseReward


class DriftingReward(BaseReward):
    def __init__(
        self,
        reward: Union[list, int] = [1, 0],
        p: float = None,
        borders: list = [0.25, 0.75],
        gauss_sd: float = 0.025,
        seed: int = 1234,
    ):

        if not isinstance(reward, (list, tuple, np.ndarray)):
            reward = [reward]

        if isinstance(seed, np.random.Generator):
            self.rng = seed
        else:
            self.rng = np.random.default_rng(seed)

        if p is None:
            p = self.rng.uniform(*borders)

        self.p = p
        self.reward = reward
        self.gauss_sd = gauss_sd
        self.borders = borders

    def _reward_function(self, condition=None):
        reward = self.rng.choice(self.reward, p=[self.p, 1 - self.p])

        step = self.rng.normal(0, self.gauss_sd)

        if (self.p + step >= self.borders[1]) or (self.p + step <= self.borders[0]):
            self.p -= step
        else:
            self.p += step

        return reward

    def __call__(self, condition=None):
        return self._reward_function(condition)


def get_two_step(conditions=None, render_backend=None, window_size=None):

    environment_graph = {
        0: ([1, 2], 0.8),
        1: [3, 4],  # env two
        2: [5, 6],  # control
        3: [],  # small win
        4: [],  # small lose
        5: [],  # big lose - lose
        6: [],  # small lose - lose
    }

    reward_structure = {
        3: DriftingReward(seed=123),
        4: DriftingReward(seed=154),
        5: DriftingReward(seed=895),
        6: DriftingReward(seed=698),
    }

    if conditions is None:
        condition_out = (None, ([0]))

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        raise NotImplementedError("Pygame implementation still ongoing")

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
