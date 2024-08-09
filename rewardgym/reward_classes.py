from typing import List, Union

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

    def _reward_function(self, **kwargs):
        reward = self.rng.choice(self.reward, p=self.p)
        return reward

    def __call__(self, **kwargs):
        return self._reward_function(**kwargs)


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

    def _reward_function(self, **kwargs):
        reward = self.rng.choice(self.reward, p=[self.p, 1 - self.p])

        next_val = self.p + self.rng.normal(0, self.gauss_sd)

        if next_val > self.borders[1]:
            next_val = 2 * self.borders[1] - next_val
        if next_val < self.borders[0]:
            next_val = 2 * self.borders[0] - next_val

        self.p = next_val

        return reward


class PseudoRandomReward(BaseReward):
    def __init__(self, reward_list: Union[List], seed=1234):
        self.reward_list = reward_list
        self.rng = check_seed(seed)
        self._generate_sequence()

    def _reward_function(self, **kwargs):

        reward = self.rewards.pop()

        if len(self.rewards) == 0:
            self._generate_sequence()

        return reward

    def _generate_sequence(self):
        self.rewards = self.rng.choice(
            self.reward_list, size=len(self.reward_list), replace=False
        ).tolist()
