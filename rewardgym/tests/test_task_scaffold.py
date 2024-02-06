import numpy as np
import pytest

from rewardgym.tasks import get_env

from ..tasks import get_env


def run_task_base(task, n_episodes=10):

    env, conditions = get_env(task, render_mode=None)

    for _ in range(n_episodes):

        if conditions[0] is not None:
            if len(conditions[0]) == 2:
                condition = np.random.choice(conditions[0][0], p=conditions[0][1])
            else:
                condition = np.random.choice(conditions[0])
        else:
            condition = None

        if conditions[1] is not None:
            starting_position = np.random.choice(conditions[1])
        else:
            starting_position = None

        obs, info = env.reset(starting_position, condition=condition)
        done = False

        # play one episode
        while not done:
            action = env.action_space.sample()
            next_obs, reward, terminated, truncated, info = env.step(action)

            done = terminated or truncated
            obs = next_obs


def test_smoke_screen_task_base_init():
    for task in ["hcp", "mid", "two-step"]:
        get_env(task, conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_task_render_init():
    for task in ["hcp", "mid"]:
        get_env(
            task,
            conditions=None,
            render_mode="human",
            render_backend="pygame",
            window_size=10,
        )


def test_smoke_screen_run_base():
    for task in ["hcp", "mid", "two-step"]:
        run_task_base(task, n_episodes=10)
