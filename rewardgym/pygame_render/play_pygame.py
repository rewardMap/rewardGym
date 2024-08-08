from typing import Literal

import pygame

from ..environments.render_env import RenderEnv
from ..pygame_render.stimuli import BaseAction, BaseText
from ..tasks.utils import get_task
from ..utils import unpack_conditions


def play_task(
    task_name: Literal[
        "hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"
    ] = "hcp",
    window_size: int = 500,
    n_episodes: int = 5,
):

    pygame.init()
    pygame.display.init()
    window = pygame.display.set_mode((window_size, window_size))
    clock = pygame.time.Clock()

    environment_graph, reward_structure, condition_out, info_dict = get_task(
        task_name, None, render_backend="pygame", window_size=window_size
    )
    env = RenderEnv(
        environment_graph=environment_graph,
        reward_locations=reward_structure,
        render_mode="human",
        info_dict=info_dict,
        window_size=window_size,
        window=window,
        clock=clock,
    )

    base_position = (window_size // 2, window_size // 2)

    text = BaseText("Instruction", 1, textposition=base_position)
    click = BaseAction()

    text.display(window=window, clock=clock)
    click.display(window=window, clock=clock)

    actions = []
    observations = []
    rewards = []

    for episode in range(n_episodes):

        obs, info = env.reset(0, condition=None)
        done = False
        observations.append(obs)
        # play one episode
        while not done:
            action = env.human_action
            next_obs, reward, terminated, truncated, info = env.step(action)
            actions.append(action)
            rewards.append(reward)

            done = terminated or truncated
            obs = next_obs
            observations.append(obs)

    env.close()
