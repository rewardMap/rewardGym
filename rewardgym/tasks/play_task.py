import argparse

from ..pygame_render import play_task


def play_cli():
    parser = argparse.ArgumentParser(description="Run one of the rewardmap games.")
    parser.add_argument(
        "task",
        type=str,
        help="The task, choose one of:"
        + "'hcp', 'mid', 'two-step', 'risk-sensitive', 'posner', 'gonogo'",
        default="hcp",
    )

    parser.add_argument("--window", type=int, help="Window size", default=700)
    parser.add_argument("--n", type=int, help="Number of trials.", default=5)

    args = parser.parse_args()
    play_task(args.task, args.window, args.n)


if __name__ == "__main__":
    play_cli()
