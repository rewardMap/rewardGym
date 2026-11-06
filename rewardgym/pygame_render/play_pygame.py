from typing import Literal

from psylog.interfaces import SystemClock

from ..logging import ExperimentLogger
from ..runner.task_runner import run_task
from ..tasks.utils import get_env


def play_task(
    task_name: Literal[
        "hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"
    ] = "hcp",
):
    env = get_env(task_name, seed=10, render_backend="pygame")

    simlog = ExperimentLogger(
        file_name=None, task=task_name, participant_id="test-agent", clock=SystemClock()
    )

    simlog.create()

    env.setup(logger=simlog, window=None, expose_last_stim=False)

    _df, _, _ = run_task(env, logger=simlog, agent=None, random_state=10)
