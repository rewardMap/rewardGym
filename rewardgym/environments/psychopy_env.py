from collections import defaultdict
from typing import Union

import numpy as np

try:
    from psychopy.visual import Window
except ModuleNotFoundError:
    from ..psychopy_render.psychopy_stubs import Window

from typing import Dict, Tuple

from .. import psychopy_render as psrender
from ..psychopy_render.logger import MinimalLogger
from .base_env import BaseEnv


class PsychopyEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = "psychopy",
        info_dict: dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
        name: str = None,
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

        super().__init__(
            environment_graph,
            reward_locations,
            render_mode,
            info_dict,
            seed,
            name,
            n_actions,
            reduced_actions=reduced_actions,
        )

        self.is_setup = False
        self.action = False

    def setup(self, window=None, logger=None, expose_last_stim=False):
        if self.render_mode == "psychopy-simulate":
            self._setup_simulation(window, logger, expose_last_stim=expose_last_stim)
        elif self.render_mode == "psychopy":
            self._setup_render(window, logger)

    def _setup_render(self, window=None, logger=None):
        if window is None:
            self.window = Window(
                size=[1680, 1050],
                fullscr=False,
                color=[-0.5, -0.5, -0.5],
                colorSpace="rgb",
                units="pix",
            )
        else:
            self.window = window

        if logger is None:
            self.logger = MinimalLogger(global_clock=psrender.psychopy_stubs.Clock())
        else:
            self.logger = logger

        for node in self.graph.keys():
            if "psychopy" in self.info_dict[node].keys():
                [
                    stim.setup(self.window)
                    for stim in self.info_dict[node]["psychopy"]
                    if not stim.is_setup
                ]

        self.is_setup = True

    def _setup_simulation(self, window=None, logger=None, expose_last_stim=False):
        self.expose_last_stim = expose_last_stim
        self.reaction_time = None

        if window is None:
            self.window = psrender.psychopy_stubs.Window()
        else:
            self.window = window

        if logger is None:
            self.logger = MinimalLogger(global_clock=psrender.psychopy_stubs.Clock())
        else:
            self.logger = logger

        self.sim_setup = True

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
        out = None

        self.logger.update_trial_info(
            current_location=self.agent_location, avail_actions=info["avail-actions"]
        )

        if self.render_mode == "psychopy" and "psychopy" in info.keys():
            if not self.is_setup:
                raise RuntimeError(
                    "You have to setup the environment first, using env.setup_render()"
                )

            for disp in info["psychopy"]:
                out = disp.display(
                    win=self.window,
                    logger=self.logger,
                    condition=self.condition,
                    total_reward=self.cumulative_reward,
                    reward=self.reward,
                    location=self.agent_location,
                    action=self.previous_action,
                    info=info,
                )

                self._check_output(out, info, remap=True)

        elif self.render_mode == "psychopy-simulate" and "psychopy" in info.keys():
            if not self.sim_setup:
                raise RuntimeError(
                    "You have to setup the environment first, using env.setup_simulation()"
                )

            for disp in info["psychopy"]:
                if disp.entity != "action" or not self.expose_last_stim:
                    disp.simulate(
                        win=self.window,
                        logger=self.logger,
                        condition=self.condition,
                        total_reward=self.cumulative_reward,
                        reward=self.reward,
                        location=self.agent_location,
                        key=self.previous_action,
                        rt=self.reaction_time,
                        info=info,
                    )

            if not self.expose_last_stim:
                self.simulate_action(info, self.previous_action, self.reaction_time)

        elif "psychopy" not in info.keys():
            pass
        else:
            raise NotImplementedError(
                "Render needs to be psychopy or psychopy-simulate."
            )

    def simulate_action(self, info, action, reaction_time):
        out = info["psychopy"][-1].simulate(
            win=self.window,
            logger=self.logger,
            condition=self.condition,
            total_reward=self.cumulative_reward,
            reward=self.reward,
            location=self.agent_location,
            key=action,
            rt=reaction_time,
            info=info,
        )

        self._check_output(out, info)

    def _check_output(self, out, info, remap=False):
        if out is not None:
            if remap:
                tmp_action = info["avail-actions"][out[0]]
            else:
                tmp_action = out[0]

            if tmp_action in info["avail-actions"]:
                self.action = tmp_action

            if out[1] is not None:
                self.remainder = self.remainder + out[1]
        else:
            self.action = None

    def close(self) -> None:
        """
        Closes the pygame display and quits pygame.
        """
        if self.window is not None:
            self.logger.close()
            self.window.close()

    def reset(
        self,
        agent_location: int = 0,
        condition: int = None,
    ) -> Tuple[Union[int, np.array], Dict]:
        self.action = None
        self.remap_action = None
        self.remainder = 0

        observation, info = super().reset(agent_location, condition)
        return observation, info
