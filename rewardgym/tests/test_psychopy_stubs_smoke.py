import pytest

from rewardgym import get_env
from rewardgym.psychopy_render import SimulationLogger
from rewardgym.psychopy_render.psychopy_stubs import Clock, Window
from rewardgym.runner import pspy_run_task


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
    env.setup(logger=Logger, window=win, expose_last_stim=True)

    pspy_run_task(env=env, win=win, logger=Logger)

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
