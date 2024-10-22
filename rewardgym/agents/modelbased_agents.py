import warnings
from typing import List, Tuple, Union

import numpy as np

from rewardgym.utils import check_seed

from .base_agent import QAgent_eligibility, ValenceQAgent, ValenceQAgent_eligibility


class HybridAgent(ValenceQAgent):
    """
    A hybrid reinforcement learning agent combining model-based (MB) and model-free (MF) learning.
    The agent maintains a state-action transition table for model-based learning and a Q-value
    table for model-free learning. The combination is controlled by a hybrid parameter that blends
    the two approaches.
    """

    def __init__(
        self,
        learning_rate_mb: float,
        learning_rate_mf: Union[float, List],
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
        self.t_values = np.zeros((state_space, action_space, state_space))

        if graph is not None:
            for k in graph.keys():
                if isinstance(graph[k], tuple):
                    locations = [graph[k][0]] * action_space
                    prob = graph[k][1]
                else:
                    locations = graph[k]
                    prob = None

                for n, loc in zip(np.arange(action_space), locations):
                    ln = len(loc) if not isinstance(loc, int) else 1

                    if use_fixed and prob is not None:
                        loc = [loc] if isinstance(loc, int) else loc
                        for j in loc:
                            if j == loc[n]:
                                self.t_values[k, n, j] = prob
                            else:
                                self.t_values[k, n, j] = (1 - prob) / max([1, ln - 1])
                    else:
                        self.t_values[k, n, loc] = 1 / max([1, ln])

        self.discount_factor = discount_factor

        if isinstance(learning_rate_mf, float):
            self.q_agent = QAgent_eligibility(
                learning_rate=learning_rate_mf,
                temperature=temperature,
                discount_factor=self.discount_factor,
                action_space=action_space,
                state_space=state_space,
                eligibility_decay=eligibility_decay,
                reset_traces=reset_traces,
            )

        elif len(learning_rate_mf) == 2:
            self.q_agent = ValenceQAgent_eligibility(
                learning_rate_neg=learning_rate_mf[0],
                learning_rate_pos=learning_rate_mf[1],
                temperature=temperature,
                discount_factor=self.discount_factor,
                action_space=action_space,
                state_space=state_space,
                eligibility_decay=eligibility_decay,
                reset_traces=reset_traces,
            )
        else:
            raise ValueError(
                f"learning_rate_mf has to be float or Sequence of two floats, it is {learning_rate_mf}"
            )

        self.q_values = np.zeros((state_space, action_space))
        self.lr = learning_rate_mb
        self.action_space = action_space
        self.temperature = temperature
        self.hybrid = hybrid
        self.rng = check_seed(seed)

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

        if not terminated:
            for act in range(self.action_space):
                qval_mb = 0
                for s2 in range(self.t_values.shape[-1]):
                    qval_mb += self.t_values[obs, act, s2] * np.max(
                        self.q_agent.q_values[s2]
                    )
                self.q_values[obs][act] = qval_mb
        else:
            self.q_values[obs][action] = self.q_agent.q_values[obs][action]

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

        self.training_error.append(state_prediction_error)

        return self.q_values
