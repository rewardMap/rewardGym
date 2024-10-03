import importlib.util
from collections import defaultdict
from typing import Union

import numpy as np

if importlib.util.find_spec("pygame") is not None:
    import pygame
else:
    # Handle the absence of pygame
    pass

from .base_env import BaseEnv


class RenderEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
        name: str = None,
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
        seed : Union[int, np.random.Generator], optional
            The random seed associated with the environment, creates a generator, by default 1000
        """

        super().__init__(
            environment_graph, reward_locations, render_mode, info_dict, seed, name
        )

        self.setup = False

    def setup_render(self, window_size, window=None, clock=None):
        if window_size is None:
            self.window_size = 256
        else:
            self.window_size = window_size

        if window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        else:
            self.window = window

        if clock is None:
            self.clock = pygame.time.Clock()
        else:
            self.clock = clock

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

        self.human_action = None
        self.human_reward_modifier = 1

        if self.render_mode == "pygame" and "pygame" in info.keys():
            if not self.setup:
                raise RuntimeError(
                    "You have to setup the environment first, using env.setup()"
                )

            for disp in info["pygame"]:
                out = disp.display(
                    window=self.window,
                    clock=self.clock,
                    condition=self.condition,
                    total_reward=self.cumulative_reward,
                    reward=self.reward,
                    location=self.agent_location,
                )

                if disp.display_type == "action":
                    self.human_action = out

        elif "pygame" not in info.keys():
            pass
        else:
            raise NotImplementedError("Render should only be called in pygame mode")

    def close(self) -> None:
        """
        Closes the pygame display and quits pygame.
        """
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
