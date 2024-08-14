import warnings
from collections import defaultdict
from typing import List, Tuple, Union

import numpy as np

from ..utils import check_seed


class ValenceQAgent:
    def __init__(
        self,
        learning_rate_pos: float,
        learning_rate_neg: float,
        temperature: float,
        discount_factor: float = 0.99,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
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

        self.n_states = state_space
        self.n_actions = action_space
        self.lr_neg = learning_rate_neg
        self.lr_pos = learning_rate_pos

        self.temperature = temperature
        self.discount_factor = discount_factor

        self.rng = check_seed(seed)

        self.training_error = []

    def get_action(self, obs: Tuple[int, int, bool], avail_actions: list = None) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment

        prob = self.get_probs(obs, avail_actions)

        a = self.rng.choice(np.arange(len(prob)), p=prob)

        return a

    def get_probs(self, obs, avail_actions=None):

        prob = np.zeros_like(self.q_values[obs])

        if avail_actions is None:
            avail_actions = np.arange(len(self.q_values[obs]))

        qval = self.q_values[obs][avail_actions]
        qval = qval - np.mean(qval)
        qs = np.exp(qval * self.temperature)

        if any(~np.isfinite(qs)):
            warnings.warn("Overflow in softmax, replacing with max / min value.")
            qs[np.isposinf(qs)] = np.finfo(float).max
            qs[np.isneginf(qs)] = np.finfo(float).min

        prob[avail_actions] = qs / np.sum(qs)

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
        if temporal_difference > 0:
            q_update = self.lr_pos * temporal_difference
        elif temporal_difference <= 0:
            q_update = self.lr_neg * temporal_difference

        self.q_values[obs][action] = self.q_values[obs][action] + q_update
        self.training_error.append(temporal_difference)

        return self.q_values


class QAgent(ValenceQAgent):
    def __init__(
        self,
        learning_rate: float,
        temperature: float,
        discount_factor: float = 0.99,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
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

        super().__init__(
            learning_rate_pos=learning_rate,
            learning_rate_neg=learning_rate,
            temperature=temperature,
            discount_factor=discount_factor,
            action_space=action_space,
            state_space=state_space,
            seed=seed,
        )


class RandomAgent(QAgent):
    def __init__(
        self,
        bias: float = None,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
    ) -> None:

        self.bias = bias

        self.action_space = action_space
        self.state_space = state_space
        self.rng = check_seed(seed)

    def update(self, *args, **kwargs):

        return None

    def get_probs(self, obs, avail_actions=None):

        if avail_actions is None:
            avail_actions = np.arange(self.action_space)

        action_probs = np.zeros(self.action_space)

        if len(avail_actions) > 1:
            action_probs[avail_actions[0]] = self.bias
            action_probs[avail_actions[1:]] = (1 - self.bias) / (len(avail_actions) - 1)
        else:
            action_probs[avail_actions] = 1

        prob = action_probs

        return prob


class ValenceQAgent_eligibility(ValenceQAgent):
    def __init__(
        self,
        learning_rate_pos: float,
        learning_rate_neg: float,
        temperature: float,
        discount_factor: float = 0.99,
        eligibility_decay: float = 0.0,
        reset_traces: bool = True,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
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

        super().__init__(
            learning_rate_pos=learning_rate_pos,
            learning_rate_neg=learning_rate_neg,
            temperature=temperature,
            discount_factor=discount_factor,
            action_space=action_space,
            state_space=state_space,
            seed=seed,
        )

        self.eligibility_traces = np.zeros((state_space, action_space))
        self.eligibility_decay = eligibility_decay
        self.reset_traces = reset_traces

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

        if temporal_difference > 0:
            q_update = self.lr_pos * temporal_difference
        elif temporal_difference <= 0:
            q_update = self.lr_neg * temporal_difference
        else:
            q_update = np.nan

        self.eligibility_traces[obs][action] = self.eligibility_traces[obs][action] + 1

        self.q_values = self.q_values + q_update * self.eligibility_traces

        self.eligibility_traces = (
            self.eligibility_traces * self.discount_factor * self.eligibility_decay
        )

        if terminated and self.reset_traces:
            self.eligibility_traces = np.zeros_like(self.eligibility_traces)

        self.training_error.append(temporal_difference)

        return self.q_values


class QAgent_eligibility(ValenceQAgent_eligibility):
    def __init__(
        self,
        learning_rate: float,
        temperature: float,
        discount_factor: float = 0.99,
        eligibility_decay: float = 0.0,
        reset_traces: bool = True,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
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

        super().__init__(
            learning_rate_pos=learning_rate,
            learning_rate_neg=learning_rate,
            temperature=temperature,
            discount_factor=discount_factor,
            action_space=action_space,
            state_space=state_space,
            seed=seed,
            eligibility_decay=eligibility_decay,
            reset_traces=reset_traces,
        )
