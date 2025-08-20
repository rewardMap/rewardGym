import warnings
from typing import List, Tuple, Union

import numpy as np

from ..utils import check_random_state


class ValenceQAgent:
    """
    A reinforcement learning agent implementing a Valence-based Q-learning algorithm.
    The agent maintains state-action values (Q-values) and updates them using different
    learning rates for positive and negative temporal differences.
    """

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
        """
        Initializes the ValenceQAgent with parameters for learning, exploration, and environment size.

        Parameters
        ----------
        learning_rate_pos : float
            The learning rate used for updating Q-values when the temporal difference is positive.
        learning_rate_neg : float
            The learning rate used for updating Q-values when the temporal difference is negative.
        temperature : float
            The softmax temperature controlling exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
        """

        self.n_states = state_space
        self.n_actions = action_space
        self.q_values = np.zeros((self.n_states, self.n_actions)) + 1 / self.n_actions

        self.lr_neg = learning_rate_neg
        self.lr_pos = learning_rate_pos

        self.temperature = temperature
        self.discount_factor = discount_factor

        self.rng = check_random_state(seed)

        self.training_error = []

    def get_action(self, obs: Tuple[int, int, bool], avail_actions: List = None) -> int:
        """
        Selects an action based on the current state observation using a softmax policy.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The current state observation represented as a tuple.
        avail_actions : list, optional
            A list of available actions. If None, all actions are assumed available, by default None.

        Returns
        -------
        int
            The selected action index.
        """

        prob = self.get_probs(obs, avail_actions)

        a = self.rng.choice(np.arange(len(prob)), p=prob)

        return a

    def get_probs(self, obs: Tuple[int, int, bool], avail_actions: List = None):
        """
        Computes the softmax probability distribution over actions based on Q-values.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The current state observation represented as a tuple.
        avail_actions : list, optional
            A list of available actions. If None, all actions are assumed available, by default None.

        Returns
        -------
        np.ndarray
            A probability distribution over the available actions.
        """

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
        **kwargs,
    ):
        """
        Updates the Q-value for a given action taken in a particular state using a
        valence-based learning rate (positive or negative) depending on the temporal difference.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The current state observation represented as a tuple.
        action : int
            The action taken in the current state.
        reward : float
            The reward received after taking the action.
        terminated : bool
            Whether the episode has ended after this action.
        next_obs : Tuple[int, int, bool]
            The next state observation after taking the action.

        Returns
        -------
        np.ndarray
            The updated Q-value table.
        """

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

    def reset(self):
        self.q_values = (
            np.zeros((self.state_space, self.action_space)) + 1 / self.action_space
        )
        self.training_error = []


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
        """
        Initializes a QAgents with parameters for learning, exploration, and environment size.

        Parameters
        ----------
        learning_rate : float
            The learning rate used for updating Q-values.
        temperature : float
            The softmax temperature controlling exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
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
        self.rng = check_random_state(seed)

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

    def reset(self):
        pass


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
        """
        Initializes the ValenceQAgent with eligibility traces, and
        parameters for learning, exploration, and environment size.

        Parameters
        ----------
        learning_rate_pos : float
            The learning rate used for updating Q-values when the temporal difference is positive.
        learning_rate_neg : float
            The learning rate used for updating Q-values when the temporal difference is negative.
        temperature : float
            The softmax temperature controlling exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        eligibility_decay : float, optional
            The decay rate of the eligibility traces, by default 0.0.
        reset_traces : bool, optional
            Whether to reset the eligibility traces each episode or not, by default True.
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
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

        self.eligibility_traces = np.zeros((self.state_space, self.action_space))
        self.eligibility_decay = eligibility_decay
        self.reset_traces = reset_traces

    def update(
        self,
        obs: Tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: Tuple[int, int, bool],
        **kwargs,
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

    def reset(self):
        super().reset()
        self.eligibility_traces = np.zeros((self.state_space, self.action_space))


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
        """
        Initializes the QAgent with eligibility traces, and
        parameters for learning, exploration, and environment size.

        Parameters
        ----------
        learning_rate : float
            The learning rate used for updating Q-values.
        temperature : float
            The softmax temperature controlling exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        eligibility_decay : float, optional
            The decay rate of the eligibility traces, by default 0.0.
        reset_traces : bool, optional
            Whether to reset the eligibility traces each episode or not, by default True.
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
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
