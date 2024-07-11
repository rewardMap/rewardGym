import pytest

from rewardgym import ENVIRONMENTS, get_configs, get_env, unpack_conditions
from rewardgym.psychopy_render import SimulationLogger, get_psychopy_info
from rewardgym.psychopy_render.psychopy_stubs import Clock, Window
from rewardgym.utils import get_condition_meaning


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
    info_dict = get_psychopy_info(task)
    env, conditions = get_env(task)

    try:
        settings = get_configs(task)()
        if settings["condition_target"] == "location":
            conditions = (conditions[0], settings["condition"])
        elif settings["condition_target"] == "condition":
            conditions = (settings["condition"], conditions[1])

        n_episodes = settings["ntrials"]

    except NotImplementedError:
        settings = None
        n_episodes = 5

    if task == "risk-sensitive":
        action_map = env.condition_dict
    else:
        action_map = None

    if task == "mid":
        win_trials = 0

    env.info_dict.update(info_dict)

    actions = []

    for episode in range(n_episodes):

        condition, starting_position = unpack_conditions(conditions, episode)

        # Update timings
        if settings["update"] is not None and len(settings["update"]) > 0:
            for k in settings["update"]:
                for jj in info_dict.keys():
                    for ii in info_dict[jj]["psychopy"]:
                        if ii.name == k:
                            ii.duration = settings[k][episode]

        obs, info = env.reset(starting_position, condition=condition)
        Logger.trial = episode
        Logger.set_trial_time()
        Logger.trial_type = get_condition_meaning(
            env.info_dict, starting_position=starting_position, condition=condition
        )
        Logger.start_position = starting_position
        Logger.current_location = env.agent_location

        Logger.update_trial_info(
            start_position=starting_position,
            current_location=env.agent_location,
            trial=episode,
            condition=condition,
        )

        reward = None
        action = None

        for ii in info["psychopy"]:
            out = ii.simulate(
                win=win,
                logger=Logger,
                reward=env.reward,
                condition=condition,
                starting_position=starting_position,
                action=None,
                total_reward=env.cumulative_reward,
                key=0,
                rt=0.100,
            )

        if out is not None:
            action = out[0]
            done = False
            actions.append(action)

        else:
            done = True

        while not done:
            next_obs, reward, terminated, truncated, info = env.step(action)
            Logger.current_location = env.agent_location
            for ii in info["psychopy"]:
                out = ii.simulate(
                    win=win,
                    logger=Logger,
                    reward=env.reward,
                    condition=condition,
                    starting_position=starting_position,
                    action=action,
                    total_reward=env.cumulative_reward,
                    key=0,
                    rt=0.1,
                )

            done = terminated or truncated

            if out is None and not done and task == "two-step":
                done = True

            elif out is not None:
                action = out[0]

        if task == "mid":

            win_trials += 1 if starting_position in [3, 4] else 0

            if (sum(actions) / (episode + 1)) < 0.4 and (win_trials % 3) == 0:
                info_dict[0]["psychopy"][-1].duration -= 0.025
            elif (win_trials % 3) == 0:
                info_dict[0]["psychopy"][-1].duration += 0.25

        Logger.log_event(
            {"event_type": "TrialEnd", "total_reward": env.cumulative_reward},
            reward=env.reward,
        )

    Logger.close()
    win.close()


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
