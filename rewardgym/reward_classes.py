import numpy as np


class BaseReward:
    def __init__(self, reward, p=1, seed=1234):
        self.reward = reward
        self.p = p

        if isinstance(seed, np.random.Generator):
            self.rng = seed
        else:
            self.rng = np.random.default_rng(seed)

    def _reward_function(self, condition=None):
        reward = self.rng.choice(self.reward, p=self.p)
        return reward

    def __call__(self, condition=None):
        return self._reward_function(condition)
