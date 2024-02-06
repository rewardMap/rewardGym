from collections import defaultdict

import numpy as np
import pygame

from .base_env import BaseEnv, MultiChoiceEnv


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


class RenderEnvMultiChoice(MultiChoiceEnv, RenderEnv):
    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        condition_dict: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        seed: int | np.random.Generator = 1000,
        window_size: int = 255,
    ):

        super(MultiChoiceEnv).__init__(
            environment_graph=environment_graph,
            reward_locations=reward_locations,
            condition_dict=condition_dict,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
        )
        super(RenderEnv).__init__(window_size)
