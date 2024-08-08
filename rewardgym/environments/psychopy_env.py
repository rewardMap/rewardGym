from collections import defaultdict
from typing import Union

import numpy as np

try:
    from psychopy.visual import Window
except ModuleNotFoundError:
    from ..psychopy_render.psychopy_stubs import Window

from typing import Dict, Tuple, Union

from ..psychopy_render.logger import ExperimentLogger, MinimalLogger
from .base_env import BaseEnv


class PsychopyEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = "human",
        info_dict: dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
        window: Window = None,
        logger: ExperimentLogger = None,
        name: str = None,
        n_actions=2,
    ):
        """
        Environment to render tasks to the screen using pygame.

        Parameters
        ----------
        environment_graph : dict
            The main graph showing the asssociation between states and actions.
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
            The pygame clock for time kepping, by default None
        """

        super().__init__(
            environment_graph,
            reward_locations,
            render_mode,
            info_dict,
            seed,
            name,
            n_actions,
        )

        self.window = window
        self.logger = logger
        self.setup = False

    def setup_render(self, action_map=None):

        if self.window is None:
            self.window = Window(
                size=[1680, 1050],
                fullscr=False,
                color=[-0.5, -0.5, -0.5],
                colorSpace="rgb",
                units="pix",
            )
        if self.logger is None:
            self.logger = MinimalLogger()

        for node in self.graph.keys():
            if "psychopy" in self.info_dict[node].keys():
                [
                    stim.setup(self.window, action_map=action_map)
                    for stim in self.info_dict[node]["psychopy"]
                ]

        self.setup = True

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
        self.remap_action = None

        if self.render_mode == "human" and "psychopy" in info.keys():

            out = None

            for disp in info["psychopy"]:
                out = disp.display(
                    win=self.window,
                    logger=self.logger,
                    condition=self.condition,
                    total_reward=self.cumulative_reward,
                    reward=self.reward,
                    location=self.agent_location,
                    action=self.previous_action,
                )

            if out is not None:

                self.action = out[0]
                if "remap-actions" in info.keys():
                    self.remap_action = info["remap-actions"][self.action]

                if out[1] is not None:
                    self.remainder + out[1]
            else:
                self.action = None

        elif "psychopy" not in info.keys():
            pass
        else:
            raise NotImplementedError("Render should only be called in human mode")

    def close(self) -> None:
        """
        Closes the pygame display and quits pygame.
        """
        if self.window is not None:
            self.logger.close()
            self.window.close()

    def reset(
        self, agent_location: int = 0, condition: int = None
    ) -> Tuple[Union[int, np.array], Dict]:

        self.action = None  # Add your additional reset logic here
        self.remainder = 0
        observation, info = super().reset(agent_location, condition)
        return observation, info
