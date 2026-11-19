from __future__ import annotations

from collections import defaultdict

import numpy as np

from ..protocols import InputProtocol, LoggerProtocol
from ..render import EnvironmentContext, StepContext
from .base_env import BaseEnv
from .env_parts import ResponsePending


class RenderEnv(BaseEnv):
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
        self.action = None
        self.pending = None
        self.reaction_time = None
        self.previous_action = None
        self.remainder = 0
        self.context = None

    def setup(
        self,
        window=None,
        logger: LoggerProtocol | None = None,
        input_handler: InputProtocol | None = None,
    ):
        self.context = EnvironmentContext(
            window=window,
            logger=logger,
            input_handler=input_handler,
            mode=self.render_mode,
            random_state=self.random_state,
        )

        for node in self.graph:
            if "render" in self.info_dict[node]:
                for stim in self.info_dict[node]["render"]:
                    if not stim.is_setup:
                        stim.setup(self.context)

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
        self.pending = None

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
            tracker=self.tracker,
        )

        if not self.is_setup:
            raise RuntimeError(
                "You have to setup the environment first, using env.setup()"
            )

        if "render" not in info:
            pass
        else:
            for n, disp in enumerate(info["render"]):
                if not disp.returns_action:
                    disp.present(current_step)
                elif disp.requires_response:
                    self.pending = ResponsePending(index=n, step=current_step)
                    break
                else:
                    out = disp.present(current_step)
                    action, add_remainder = self._check_output(out, info)
                    self.action = action
                    self.remainder += add_remainder

    def get_pending_action(self):
        if self.pending is None:
            return self.action, self.remainder

        info = self.pending.step.info

        for disp in info["render"][self.pending.index :]:
            if disp.returns_action:
                out = disp.present(self.pending.step)
                action, add_remainder = self._check_output(out, info)
                self.action = action
                self.remainder += add_remainder
            else:
                disp.present(self.pending.step)

        self.pending = None

        return self.action, self.remainder

    @staticmethod
    def _check_output(out, info):
        if out is None:
            return None, 0

        action, remainder = out

        add_remainder = 0 if remainder is None else remainder

        if action is None:
            return None, add_remainder

        graph_action = info["action-layout"].action_to_graph[action]

        if graph_action not in info["avail-actions"]:
            return None, add_remainder

        return action, add_remainder

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
        self.remainder = 0

        observation, info = super().reset(agent_location, condition)
        return observation, info

    def simulate_response(self, action, rt):
        if not hasattr(self.context.input_handler, "add_response"):
            return False

        if self.pending is None:
            return False

        routine = self.pending_routine

        if rt > routine.duration:
            return False

        layout = self.pending.step.info["action-layout"]
        layout.add_keys(routine.key_dict)

        if layout.graph_to_key[action]:
            key = layout.graph_to_key[action][0]
            self.context.input_handler.add_response(key, rt)
            return True

    @property
    def pending_routine(self):
        if self.pending is None:
            return None

        return self.pending.step.info["render"][self.pending.index]
