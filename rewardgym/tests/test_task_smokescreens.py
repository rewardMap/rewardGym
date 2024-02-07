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
            if len(conditions[1]) == 2:
                starting_position = np.random.choice(
                    conditions[1][0], p=conditions[1][1]
                )
            else:
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


def test_smoke_screen_hcp_base_init():
    get_env("hcp", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_mid_base_init():
    get_env("mid", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_gonogo_base_init():
    get_env("gonogo", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_posner_base_init():
    get_env("posner", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_two_step_base_init():
    get_env("two-step", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_risk_sensitive_base_init():
    get_env("risk-sensitive", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_hcp_render_init():
    get_env(
        "hcp",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_mid_render_init():
    get_env(
        "mid",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_gonogo_render_init():
    get_env(
        "gonogo",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_posner_render_init():
    get_env(
        "posner",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_two_step_render_init():
    get_env(
        "two-step",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_risk_sensitive_render_init():
    get_env(
        "risk-sensitive",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_run_hcp_base():
    run_task_base("hcp", n_episodes=10)


def test_smoke_screen_run_mid_base():
    run_task_base("mid", n_episodes=10)


def test_smoke_screen_run_gonogo_base():
    run_task_base("gonogo", n_episodes=10)


def test_smoke_screen_run_posner_base():
    run_task_base("posner", n_episodes=10)


def test_smoke_screen_run_two_step_base():
    run_task_base("two-step", n_episodes=10)


def test_smoke_screen_run_risk_sensitive_base():
    run_task_base("risk-sensitive", n_episodes=10)
