import argparse
from typing import Literal

from psylog.interfaces import SystemClock

from ..logging import ExperimentLogger
from ..runner.task_runner import run_task
from ..tasks.utils import get_env


def play_task(
    task_name: Literal[
        "hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"
    ] = "hcp",
    backend: Literal["pygame", "psychopy", "psychopy-simulate"] = "pygame",
):
    env = get_env(task_name, seed=10, render_backend=backend)

    if backend == "psychopy":
        from psychopy.core import Clock

        clock = Clock()
    else:
        clock = SystemClock()

    simlog = ExperimentLogger(
        file_name=None, task=task_name, participant_id="test-agent", clock=clock
    )

    simlog.create()

    env.setup(logger=simlog, window=None, expose_last_stim=False)

    _df, _, _ = run_task(env, logger=simlog, agent=None, random_state=10)


def play_cli():
    parser = argparse.ArgumentParser(description="Run one of the rewardmap games.")
    parser.add_argument(
        "task",
        type=str,
        help="The task, choose one of:"
        + "'hcp', 'mid', 'two-step', 'risk-sensitive', 'posner', 'gonogo'",
        default="hcp",
    )
    parser.add_argument(
        "backend",
        type=str,
        help="The backend for the task, choose one of:"
        + "'pygame', 'psychopy', 'psychopy-simulate'",
        default="pygame",
    )

    args = parser.parse_args()
    play_task(args.task, args.backend)


if __name__ == "__main__":
    play_cli()
