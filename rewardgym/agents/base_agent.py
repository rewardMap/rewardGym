from collections import defaultdict

import numpy as np


class SimpleQAgent:
    def __init__(
        self,
        env,
        learning_rate: float,
        epsilon: float,
        discount_factor: float = 0.95,
    ):

        self.env = env
        self.q_values = defaultdict(lambda: np.zeros(self.env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = epsilon

    def get_action(self, obs: tuple[int, int, bool]) -> int:

        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        """Updates the Q-value of an action."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
