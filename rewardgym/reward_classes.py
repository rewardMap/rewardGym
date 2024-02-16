from typing import Union

import numpy as np

from .utils import check_seed


class BaseReward:
    def __init__(self, reward, p=1, seed=1234):

        if not isinstance(reward, (list, tuple, np.ndarray)):
            reward = [reward]

        if not isinstance(p, (list, tuple, np.ndarray)):
            p = [p]

        self.reward = reward
        self.p = p

        self.rng = check_seed(seed)

    def _reward_function(self, condition=None):
        reward = self.rng.choice(self.reward, p=self.p)
        return reward

    def __call__(self, condition=None):
        return self._reward_function(condition)


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

        self.rng = check_seed(seed)

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
