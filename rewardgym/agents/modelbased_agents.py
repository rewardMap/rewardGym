import warnings
from typing import Tuple, Union

import numpy as np

from ..utils import check_random_state
from .base_agent import ValenceQAgent, ValenceQAgent_eligibility


class ValenceHybridAgent(ValenceQAgent):
    """
    A hybrid reinforcement learning agent combining model-based (MB) and model-free (MF) learning.
    The agent maintains a state-action transition table for model-based learning and a Q-value
    table for model-free learning. The combination is controlled by a hybrid parameter that blends
    the two approaches.
    """

    def __init__(
        self,
        learning_rate_mb: float,
        learning_rate_mf_pos: float,
        learning_rate_mf_neg: float,
        temperature: float,
        discount_factor: float = 0.99,
        eligibility_decay: float = 0.0,
        reset_traces: bool = True,
        hybrid: float = 1.0,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
        graph=None,
        use_fixed=False,
    ):
        """
        Initializes the HybridAgent with parameters for both model-based and model-free learning.
        The agent maintains both state-action Q-values and state-action-state transition probabilities.

        Parameters
        ----------
        learning_rate_mb : float
            The learning rate for updating the state-action-state transition model (model-based learning).
        learning_rate_mf : Union[float, List]
            The learning rate(s) for model-free learning. Can be a single float or a list with two values
            for positive and negative learning rates (if using valence-based Q-learning).
        temperature : float
            The softmax temperature used to control exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        eligibility_decay : float, optional
            The decay rate for eligibility traces in model-free learning, by default 0.0.
        reset_traces : bool, optional
            Whether to reset the eligibility traces after an episode, by default True.
        hybrid : float, optional
            A parameter that controls the balance between model-based (MB) and model-free (MF) learning,
            by default 1.0 (fully MB).
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
        graph : dict, optional
            A dictionary representing the environment's state-action transition graph. If None, transitions
            are initialized randomly, by default None.
        use_fixed : bool, optional
            Whether to use fixed transition probabilities (based on a given graph), by default False.
        """

        self.n_states = state_space
        self.n_actions = action_space

        self.t_values = np.zeros((self.n_states, self.n_actions, self.n_states))

        if graph is not None:
            for k in graph.keys():
                actions = list(graph[k].keys())

                for a in actions:
                    loc = graph[k][a]

                    if isinstance(graph[k][a], tuple):
                        prob = graph[k][a][1]
                        loc = graph[k][a][0]
                    else:
                        prob = None

                    loc = [loc] if isinstance(loc, int) else loc
                    ln = len(loc)

                    if use_fixed and prob is not None:
                        for n, j in enumerate(loc):
                            if n == 0:
                                self.t_values[k, a, j] = prob
                            else:
                                self.t_values[k, a, j] = (1 - prob) / max([1, ln - 1])
                    else:
                        for j in loc:
                            self.t_values[k, a, j] = 1 / max([1, ln])

        self.discount_factor = discount_factor

        self.q_agent = ValenceQAgent_eligibility(
            learning_rate_neg=learning_rate_mf_neg,
            learning_rate_pos=learning_rate_mf_pos,
            temperature=temperature,
            discount_factor=self.discount_factor,
            action_space=action_space,
            state_space=state_space,
            eligibility_decay=eligibility_decay,
            reset_traces=reset_traces,
        )

        self.q_values = np.zeros((self.n_states, self.n_actions))
        self.lr = learning_rate_mb
        self.temperature = temperature
        self.hybrid = hybrid
        self.rng = check_random_state(seed)

        self.training_error = []

    def get_probs(self, obs, avail_actions=None):
        """
        Computes the softmax probability distribution over actions based on a combination of
        model-based (MB) and model-free (MF) Q-values, controlled by the hybrid parameter.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The current state observation.
        avail_actions : list, optional
            A list of available actions. If None, all actions are considered available, by default None.

        Returns
        -------
        np.ndarray
            A probability distribution over the available actions.
        """
        prob = np.zeros_like(self.q_values[obs])

        if avail_actions is None:
            avail_actions = np.arange(len(self.q_values[obs]))

        qval_mb = self.q_values[obs][avail_actions]
        qval_mf = self.q_agent.q_values[obs][avail_actions]

        qval = qval_mb * self.hybrid + qval_mf * (1 - self.hybrid)

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
        Updates the Q-values for both model-based and model-free learning and updates
        the state-action-state transition probabilities for model-based learning.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The current state observation.
        action : int
            The action taken in the current state.
        reward : float
            The reward received after taking the action.
        terminated : bool
            Whether the episode has terminated.
        next_obs : Tuple[int, int, bool]
            The next state observation after taking the action.

        Returns
        -------
        np.ndarray
            The updated Q-value table.
        """

        self.q_agent.update(obs, action, reward, terminated, next_obs)

        state_prediction_error = 1 - self.t_values[obs][action][next_obs]

        for n in range(self.t_values.shape[-1]):
            if n == next_obs:
                self.t_values[obs][action][n] = (
                    self.t_values[obs][action][n] + self.lr * state_prediction_error
                )
            else:
                self.t_values[obs][action][n] = self.t_values[obs][action][n] * (
                    1 - self.lr
                )

        if not terminated:
            qval_mb = 0
            for s2 in range(self.t_values.shape[-1]):
                qval_mb += self.t_values[obs, action, s2] * (
                    reward + np.max(self.q_agent.q_values[s2])
                )
            self.q_values[obs][action] = qval_mb
        else:
            self.q_values[obs][action] = self.q_agent.q_values[obs][action]

        self.training_error.append(state_prediction_error)

        return self.q_values

    def reset(self):
        self.q_agent.reset()
        self.t_values = np.zeros((self.n_states, self.n_actions, self.n_states))
        self.q_values = np.zeros((self.n_states, self.n_actions))


class HybridAgent(ValenceHybridAgent):
    """
    A hybrid reinforcement learning agent combining model-based (MB) and model-free (MF) learning.
    The agent maintains a state-action transition table for model-based learning and a Q-value
    table for model-free learning. The combination is controlled by a hybrid parameter that blends
    the two approaches.
    """

    def __init__(
        self,
        learning_rate_mb: float,
        learning_rate_mf: float,
        temperature: float,
        discount_factor: float = 0.99,
        eligibility_decay: float = 0.0,
        reset_traces: bool = True,
        hybrid: float = 1.0,
        action_space: int = 2,
        state_space: int = 2,
        seed: Union[int, np.random.Generator] = 1000,
        graph=None,
        use_fixed=False,
    ):
        """
        Initializes the HybridAgent with parameters for both model-based and model-free learning.
        The agent maintains both state-action Q-values and state-action-state transition probabilities.

        Parameters
        ----------
        learning_rate_mb : float
            The learning rate for updating the state-action-state transition model (model-based learning).
        learning_rate_mf : Union[float, List]
            The learning rate(s) for model-free learning. Can be a single float or a list with two values
            for positive and negative learning rates (if using valence-based Q-learning).
        temperature : float
            The softmax temperature used to control exploration during action selection.
        discount_factor : float, optional
            The discount factor for future rewards, by default 0.99.
        eligibility_decay : float, optional
            The decay rate for eligibility traces in model-free learning, by default 0.0.
        reset_traces : bool, optional
            Whether to reset the eligibility traces after an episode, by default True.
        hybrid : float, optional
            A parameter that controls the balance between model-based (MB) and model-free (MF) learning,
            by default 1.0 (fully MB).
        action_space : int, optional
            The number of actions available in the environment, by default 2.
        state_space : int, optional
            The number of states in the environment, by default 2.
        seed : Union[int, np.random.Generator], optional
            Seed or random number generator for reproducibility, by default 1000.
        graph : dict, optional
            A dictionary representing the environment's state-action transition graph. If None, transitions
            are initialized randomly, by default None.
        use_fixed : bool, optional
            Whether to use fixed transition probabilities (based on a given graph), by default False.
        """
        super().__init__(
            learning_rate_mf_pos=learning_rate_mf,
            learning_rate_mf_neg=learning_rate_mf,
            learning_rate_mb=learning_rate_mb,
            eligibility_decay=eligibility_decay,
            reset_traces=reset_traces,
            hybrid=hybrid,
            graph=graph,
            use_fixed=use_fixed,
            temperature=temperature,
            discount_factor=discount_factor,
            action_space=action_space,
            state_space=state_space,
            seed=seed,
        )
