import pytest

from rewardgym import ENVIRONMENTS
from rewardgym.tasks import get_env


def run_task_base(task, n_episodes=10):
    env = get_env(task, render_mode=None)

    for _ in range(n_episodes):
        _, _ = env.reset(agent_location=0, condition=None)
        done = False

        # play one episode
        while not done:
            action = env.action_space.sample()
            _, _, terminated, truncated, _ = env.step(action)

            done = terminated or truncated


@pytest.mark.parametrize("env", ENVIRONMENTS)
def test_smoke_screen_base_init(env):
    get_env(env, conditions=None, render_mode=None, render_backend=None)


@pytest.mark.parametrize("env", ENVIRONMENTS)
def test_smoke_screen_render_init(env):
    get_env(
        env,
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


@pytest.mark.parametrize("env", ENVIRONMENTS)
def test_smoke_screen_run_base(env):
    run_task_base(env, n_episodes=10)
