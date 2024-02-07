import argparse
from typing import Literal

import pygame

from ..environments.render_env import RenderEnv, RenderEnvMultiChoice
from ..pygame_render.stimuli import BaseAction, BaseText
from ..utils import unpack_conditions
from .utils import get_task


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

    if task_name == "risk-sensitive":
        env = RenderEnvMultiChoice(
            environment_graph=environment_graph,
            condition_dict=condition_out[1],
            reward_locations=reward_structure,
            render_mode="human",
            info_dict=info_dict,
            window_size=window_size,
            window=window,
            clock=clock,
        )
        condition_out = condition_out[0]
    else:
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

    text(window=window, clock=clock)
    click(window=window, clock=clock)

    actions = []
    observations = []
    rewards = []

    for episode in range(n_episodes):

        condition, starting_position = unpack_conditions(condition_out, episode)

        obs, info = env.reset(starting_position, condition=condition)
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


def play_cli():
    parser = argparse.ArgumentParser(description="Run one of the rewardmap games.")
    parser.add_argument(
        "task",
        type=str,
        help="The task, choose one of:"
        + "'hcp', 'mid', 'two-step', 'risk-sensitive', 'posner', 'gonogo'",
        default="hcp",
    )

    parser.add_argument("--window", type=int, help="Window size", default=700)
    parser.add_argument("--n", type=int, help="Number of trials.", default=5)

    args = parser.parse_args()
    play_task(args.task, args.window, args.n)


if __name__ == "__main__":
    play_cli()
