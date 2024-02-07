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
