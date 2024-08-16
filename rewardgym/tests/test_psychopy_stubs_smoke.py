import pytest

from rewardgym import get_configs, get_env
from rewardgym.psychopy_render import SimulationLogger
from rewardgym.psychopy_render.psychopy_stubs import Clock, Window
from rewardgym.utils import update_psychopy_trials


def simulate_task(envname):
    exp_dict = {"participant_id": "001", "run": 1, "task": envname}

    win = Window()
    globalClock = Clock()

    Logger = SimulationLogger(
        "",
        globalClock,
        participant_id=exp_dict["participant_id"],
        run=exp_dict["run"],
        task=exp_dict["task"],
    )
    Logger.create()

    task = exp_dict["task"]

    env = get_env(task, render_backend="psychopy-simulate")
    env.setup_simulation(logger=Logger, window=win, expose_last_stim=True)

    settings = get_configs(task)(stimulus_set=55)
    n_episodes = settings["ntrials"]

    if task == "mid":
        win_trials = 0

    actions = []

    for episode in range(n_episodes):
        update_psychopy_trials(settings, env, episode)

        Logger.trial = episode
        Logger.set_trial_time()
        Logger.trial_type = settings["condition"][episode]
        Logger.start_position = env.agent_location
        Logger.current_location = env.agent_location

        obs, info = env.reset()
        env.simulate_action(info, 0, 0.1)

        Logger.update_trial_info(
            start_position=env.agent_location,
            current_location=env.agent_location,
            trial=episode,
        )

        if env.action is not None:
            action = env.action
            done = False
            actions.append(action)
        else:
            done = True

        while not done:
            next_obs, reward, terminated, truncated, info = env.step(action)
            Logger.current_location = env.agent_location

            done = terminated or truncated

            if not done:
                env.simulate_action(info, 0, 0.1)

            if env.action is None:
                done = True
            else:
                actions.append(env.action)

        if task == "mid":
            win_trials += 1 if "win" in settings["condition"] else 0

            if (sum(actions) / (episode + 1)) < 0.4 and (win_trials % 3) == 0:
                if (env.info_dict[1]["psychopy"][-1].duration - 0.025) > 0.05:
                    env.info_dict[1]["psychopy"][-1].duration -= 0.025
            elif (win_trials % 3) == 0:
                env.info_dict[1]["psychopy"][-1].duration += 0.025

        Logger.log_event(
            {"event_type": "TrialEnd", "total_reward": env.cumulative_reward},
            reward=env.reward,
        )

    win.close()

    return Logger.close()


def test_smoke_screen_simulate_hcp():
    simulate_task("hcp")


def test_smoke_screen_simulate_gonogo():
    simulate_task("gonogo")


def test_smoke_screen_simulate_two_step():
    simulate_task("two-step")


def test_smoke_screen_simulate_risk_sensitive():
    simulate_task("risk-sensitive")


def test_smoke_screen_simulate_posner():
    simulate_task("posner")


def test_smoke_screen_simulate_mid():
    simulate_task("mid")


def test_logger_error():
    Logger = SimulationLogger(
        "",
        None,
        participant_id="1",
        run=1,
        task="test",
    )
    Logger.create()

    with pytest.raises(AttributeError):
        Logger.update_trial_info(bla="bla")
