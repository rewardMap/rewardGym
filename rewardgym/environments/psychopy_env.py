from __future__ import annotations

from collections import defaultdict

import numpy as np

from ..protocols import InputProtocol, LoggerProtocol
from .base_env import BaseEnv
from .contexts import EnvironmentContext, StepContext


class PsychopyEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = "psychopy",
        info_dict: dict | None = None,
        random_state: int | np.random.Generator = 1000,
        name: str | None = None,
        n_actions=None,
        reduced_actions=None,
    ):
        """
        Environment to render tasks to the screen using pygame.

        Parameters
        ----------
        environment_graph : dict
            The main graph showing the association between states and actions.
        reward_locations : dict
            Which location in the graph are associated with a reward.
        render_mode : str, optional
            If using rendering or not, by default None
        info_dict : dict, optional
            Additional information, that should be associated with a node, by default defaultdict(int)
        window_size : int, optional
            Size of the window in pixel, by default 255
        seed : Union[int, np.random.Generator], optional
            The random seed associated with the environment, creates a generator, by default 1000
        window : Surface, optional
            The window / pygame surface class on which stimuli are drawn, by default None
        clock : Clock, optional
            The pygame clock for time keeping, by default None
        """

        if info_dict is None:
            info_dict = defaultdict(int)
        super().__init__(
            environment_graph=environment_graph,
            reward_locations=reward_locations,
            render_mode=render_mode,
            info_dict=info_dict,
            random_state=random_state,
            name=name,
            n_actions=n_actions,
            reduced_actions=reduced_actions,
        )

        self.is_setup = False
        self.action = False

    def setup(
        self,
        window=None,
        logger: LoggerProtocol | None = None,
        expose_last_stim: bool = False,
        input_handler: InputProtocol | None = None,
    ):
        self.context = EnvironmentContext(
            window=window,
            logger=logger,
            input_handler=input_handler,
            mode=self.render_mode,
        )

        if self.render_mode == "psychopy":
            for node in self.graph:
                if "psychopy" in self.info_dict[node]:
                    [
                        stim.setup(self.context.window)
                        for stim in self.info_dict[node]["psychopy"]
                        if not stim.is_setup
                    ]

        self.expose_last_stim = expose_last_stim
        self.reaction_time = None

        self.is_setup = True

    def _render_frame(self, info: dict) -> None:
        """
        Renders a "frame", which here means, all the stimuli that are included
        in the info_dict list associated with a given node.

        Parameters
        ----------
        info : dict
            Additional information, that should be associated with a node, by default defaultdict(int)
        """
        self.previous_action = self.action
        self.action = None

        print(self.previous_action)
        out = None

        self.context.logger.update_trial_info(
            current_location=self.agent_location, avail_actions=info["avail-actions"]
        )

        current_step = StepContext(
            env_context=self.context,
            location=self.agent_location,
            condition=self.condition,
            total_reward=self.cumulative_reward,
            reward=self.reward,
            previous_action=self.previous_action,
            reaction_time=self.reaction_time,
            info=info,
        )

        if not self.is_setup:
            raise RuntimeError(
                "You have to setup the environment first, using env.setup()"
            )

        if "psychopy" not in info:
            pass
        else:
            for disp in info["psychopy"]:
                print("Disp,", disp)
                if disp.returns_action and not self.expose_last_stim:
                    out = disp.present(current_step)
                    self._check_output(out, info, remap=True)

                elif not disp.returns_action:
                    disp.present(context=current_step)

            if not self.expose_last_stim and self.context == "psychopy-simulate":
                print("I should not run")
                self.simulate_action(info, self.previous_action, self.reaction_time)

    def simulate_action(self, info, action, reaction_time):
        action_step = StepContext(
            env_context=self.context,
            location=self.agent_location,
            condition=self.condition,
            total_reward=self.cumulative_reward,
            reward=self.reward,
            previous_action=action,
            reaction_time=reaction_time,
            info=info,
        )
        print(info["psychopy"][-1])
        out = info["psychopy"][-1].present(action_step)
        print(out)
        self._check_output(out, info)

    def _check_output(self, out, info, remap=False):
        print("checking output", out)
        if out is not None:
            if remap:
                tmp_action = info["behav_remap"][out[0]]
            else:
                tmp_action = out[0]

            if tmp_action in info["avail-actions"]:
                self.action = tmp_action
            else:
                self.action = None
                self.remainder = self.remainder

            if out[1] is not None:
                self.remainder = self.remainder + out[1]
        else:
            self.action = None

    def close(self) -> None:
        """
        Closes the pygame display and quits pygame.
        """
        if self.context.window is not None:
            self.context.window.close()

        if self.context.logger is not None:
            self.context.logger.close()

    def reset(
        self,
        agent_location: int = 0,
        condition: int | None = None,
    ) -> tuple[int | np.array, dict]:
        self.action = None
        self.remap_action = None
        self.remainder = 0

        observation, info = super().reset(agent_location, condition)
        return observation, info
