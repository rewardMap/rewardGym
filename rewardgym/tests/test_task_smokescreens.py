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


def test_smoke_screen_two_step_flip_base_init():
    get_env("two-step-flip", conditions=None, render_mode=None, render_backend=None)


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


def test_smoke_screen_two_step_flip_render_init():
    get_env(
        "two-step-flip",
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


def test_smoke_screen_run_two_step_flip_base():
    run_task_base("two-step-flip", n_episodes=10)


def test_smoke_screen_run_risk_sensitive_base():
    run_task_base("risk-sensitive", n_episodes=10)
