from collections import defaultdict

import pygame

from .base_env import BaseEnv


class RenderEnv(BaseEnv):
    def __init__(
        self,
        environment_graph,
        condition_logic,
        reward_locations,
        render_mode=None,
        info_dict=defaultdict(int),
        window_size=255,
    ):

        super().__init__(
            environment_graph, condition_logic, reward_locations, render_mode, info_dict
        )
        self.window_size = window_size

    def _render_frame(self, info):
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
                print(disp)
                out = disp(self.window, self.clock, self.condition)
                print(out)

                if disp.display_type == "action":
                    self.human_action = out
        else:
            raise NotImplementedError("Render should only be called in human mode")

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
