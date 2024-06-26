from collections import defaultdict
from typing import Tuple

import numpy as np


class QAgent:
    def __init__(
        self,
        learning_rate: float,
        temperature: float,
        discount_factor: float,
        action_space: int = 2,
        state_space: int = 2,
    ):
        """Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.

        Args:
            learning_rate: The learning rate
            initial_epsilon: The initial epsilon value
            epsilon_decay: The decay for epsilon
            final_epsilon: The final epsilon value
            discount_factor: The discount factor for computing the Q-value
        """
        self.q_values = np.zeros((state_space, action_space))

        self.lr = learning_rate
        self.temperature = temperature
        self.discount_factor = discount_factor

        self.training_error = []

    def get_action(self, obs: Tuple[int, int, bool], avail_actions: list = None) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment

        prob = self.get_probs(obs, avail_actions)

        a = np.random.choice(np.arange(len(prob)), p=prob)

        return a

    def get_probs(self, obs, avail_actions=None):
        if avail_actions is None:
            avail_actions = np.arange(len(self.q_values[obs]))

        qval = self.q_values[obs][avail_actions]

        qs = np.exp(qval * self.temperature)

        prob = qs / np.sum(qs)

        return prob

    def update(
        self,
        obs: Tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: Tuple[int, int, bool],
    ):
        """Updates the Q-value of an action."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

        return self.q_values
