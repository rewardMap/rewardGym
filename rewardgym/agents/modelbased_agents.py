import warnings
from typing import List, Tuple, Union

import numpy as np

from rewardgym.utils import check_seed

from .base_agent import QAgent_eligibility, ValenceQAgent, ValenceQAgent_eligibility


class HybridAgent(ValenceQAgent):
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
        """Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.

        Args:
            learning_rate: The learning rate
            initial_epsilon: The initial epsilon value
            epsilon_decay: The decay for epsilon
            final_epsilon: The final epsilon value
            discount_factor: The discount factor for computing the Q-value
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
