import argparse
from typing import Literal


from ..logging import ExperimentLogger
from ..runner.task_runner import run_task
from ..tasks.utils import get_env
from ..psychopy_render import psychopy_stubs

from ..agents import QAgent


def play_task(
    task_name: Literal[
        "hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"
    ] = "hcp",
    backend: Literal["pygame", "psychopy", "simulation"] = "pygame",
    out: str | None = None,
):
    env = get_env(task_name, seed=10, render_backend=backend)

    if backend == "psychopy":
        from psychopy.core import Clock

        clock = Clock()
    else:
        clock = psychopy_stubs.Clock()

    file_name = out

    simlog = ExperimentLogger(
        file_name=file_name, task=task_name, participant_id="test-agent", clock=clock
    )

    simlog.create()

    agent = None
    if backend == "simulation":
        agent = QAgent(
            learning_rate=0.1,
            temperature=4,
            discount_factor=0.99,
            action_space=env.n_actions,
            state_space=env.n_states,
            seed=10,
        )

    env.setup(logger=simlog, window=None, expose_last_stim=backend == "simulation")

    _df, _, _ = run_task(env, logger=simlog, agent=agent, random_state=10)


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
        + "'pygame', 'psychopy', 'simulation'",
        default="pygame",
    )

    parser.add_argument(
        "out",
        type=str,
        help="out-path",
        default=None,
    )

    args = parser.parse_args()
    play_task(args.task, args.backend, args.out)


if __name__ == "__main__":
    play_cli()
