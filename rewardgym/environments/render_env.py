from collections import defaultdict
from typing import Union

import numpy as np

try:
    import pygame
    from pygame import Surface
    from pygame.time import Clock
except ModuleNotFoundError:
    from .gymnasium_stubs import Surface, Clock

from .base_env import BaseEnv, MultiChoiceEnv


class RenderEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        window_size: int = 255,
        seed: Union[int, np.random.Generator] = 1000,
        window: Surface = None,
        clock: Clock = None,
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
        )
        self.window_size = window_size
        self.window = window
        self.clock = clock

    def _render_frame(self, info: dict) -> None:
        """
        Renders a "frame", which here means, all the stimuli that are included
        in the info_dict list associated with a given node.

        Parameters
        ----------
        info : dict
            Additional information, that should be associated with a node, by default defaultdict(int)
        """
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        self.human_action = None
        self.human_reward_modifier = 1

        if self.render_mode == "human":

            for disp in info["human"]:
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

        else:
            raise NotImplementedError("Render should only be called in human mode")

    def close(self) -> None:
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


class RenderEnvMultiChoice(MultiChoiceEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        condition_dict: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        window_size: int = 255,
        seed: Union[int, np.random.Generator] = 1000,
        window: Surface = None,
        clock: Clock = None,
    ):
        """
        MultiChoice Environment to render tasks to the screen using pygame.

        Parameters
        ----------
        environment_graph : dict
            The main graph showing the asssociation between states and actions.
        reward_locations : dict
            Which location in the graph are associated with a reward.
        condition_dict : dict
            A mapping between the condition and the possible outcomes of a response. E.g. in the risk-sensitive task,
            condition_dict[1] = {0 : 4, 1: 2} would say that in condition 1, a "left" response would lead to outcome 4,
            a "right" response to outcome 2.
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
            environment_graph=environment_graph,
            reward_locations=reward_locations,
            condition_dict=condition_dict,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
        )

        self.window_size = window_size
        self.window = window
        self.clock = clock

    _render_frame = RenderEnv.__dict__["_render_frame"]
    close = RenderEnv.__dict__["close"]
