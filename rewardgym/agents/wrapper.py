from typing import Tuple

import numpy as np


class RTWrapper:
    def __init__(self, agent, *args, **kwargs):
        self.agent = agent(*args, **kwargs)

    def __getattr__(self, name):
        """
        Delegate attribute access to the wrapped class instance.
        This will be called if the attribute is not found in the wrapper itself.
        """
        return getattr(self.agent, name)


class EAMWrapper(RTWrapper):
    """
    Wraps the action selection process of an agent with an evidence accumulation
    process, returning both RTs and action. RL-EAM, following
    Miletić, S., Boag, R. J., Trutti, A. C., Stevenson, N., Forstmann, B. U., & Heathcote, A. (2021).
    A new model of decision processing in instrumental learning tasks. eLife, 10, e63055. https://doi.org/10.7554/eLife.63055
    """

    def __init__(
        self,
        agent,
        *args,
        eam_sd: float = 0.1,
        eam_a: float = 1,
        eam_dt: float = 0.01,
        eam_v0: float = 0,
        eam_w: float = 1.0,
        add_error_process: bool = False,
        **kwargs,
    ):
        self.agent = agent(*args, **kwargs)
        self.eam_sd = eam_sd
        self.eam_a = eam_a
        self.eam_dt = eam_dt
        self.eam_v0 = eam_v0
        self.eam_w = eam_w
        self.add_error_process = add_error_process

    def get_rt_action(
        self, obs: Tuple[int, int, bool], avail_actions: list = None
    ) -> int:
        """
        Uses an evidence accumulation process to simulate reaction times and actions for a
        given task. Creates a race-model where the agent's q-values determine the drift rate
        of the evidence accumulation process.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The agent's observation of the environment.
        avail_actions : list, optional
            List of available actions, by default None

        Returns
        -------
        Tuple[int, float]
            Returns the action and a reaction time.
        """
        if avail_actions is None:
            avail_actions = np.arange(len(self.q_values[obs]))

        qval = self.q_values[obs][avail_actions]

        if self.add_error_process:
            qval = np.hstack([qval, np.mean(qval)])

        evidence = np.zeros_like(qval)
        rts = 0

        while all(evidence < self.eam_a):
            evidence = self._accumulate(qval, evidence)
            rts += self.eam_dt

        a = np.argmax(evidence)

        if a == len(qval) - 1 and self.add_error_process:
            a = self.agent.rng.choice(len(avail_actions))

        return a, rts

    def _accumulate(self, q, evidence):
        noise = self.agent.rng.normal(0, self.eam_sd, len(q))
        evidence += (self.eam_v0 + self.eam_w * q) * self.eam_dt + noise * np.sqrt(
            self.eam_dt
        )

        return evidence


class SimpleWrapper(RTWrapper):
    def __init__(self, agent, *args, rt_extra=0.0, env_name=None, **kwargs):
        self.agent = agent(*args, **kwargs)
        self.rt_extra = rt_extra
        self.env_name = env_name

    def get_rt_action(
        self, obs: Tuple[int, int, bool], avail_actions: list = None
    ) -> Tuple[int, float]:
        """
        Get's the softmax probability and uses it to chose an action, also using the
        probability as a proxy for reaction times.

        Parameters
        ----------
        obs : Tuple[int, int, bool]
            The agent's observation of the environment.
        avail_actions : list, optional
            List of available actions, by default None

        Returns
        -------
        Tuple[int, float]
            Returns the action and a reaction time.
        """

        a = self.get_action(obs, avail_actions)
        p = self.get_probs(obs, avail_actions)

        if self.env_name == "gonogo":
            rt_extra = a * self.rt_extra
        else:
            rt_extra = 0

        rt = (1 - p[a]) / 2 + rt_extra

        return a, rt
