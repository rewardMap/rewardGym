from collections import defaultdict

import numpy as np
import pygame

from .base_env import BaseEnv


class RenderEnv(BaseEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        window_size: int = 255,
        seed: int | np.random.Generator = 1000,
    ):

        super().__init__(
            environment_graph,
            reward_locations,
            render_mode,
            info_dict,
            seed,
        )
        self.window_size = window_size

    def _render_frame(self, info: dict) -> None:
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
                out = disp(
                    self.window,
                    self.clock,
                    self.condition,
                    reward=self.cumulative_reward,
                )

                if disp.display_type == "action":
                    self.human_action = out

        else:
            raise NotImplementedError("Render should only be called in human mode")

    def close(self) -> None:
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
