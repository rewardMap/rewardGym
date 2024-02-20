from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward


def get_gonogo(
    starting_positions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
):

    environment_graph = {
        0: [6, 7],  # win - go (action1)
        1: [4, 5],  # punish - go (action1)
        2: [7, 6],  # win - nogo (action2)
        3: [5, 4],  # punish - nogo (action2)
        4: [],  # Punish low
        5: [],  # Punish high
        6: [],  # Win high
        7: [],  # Win low
    }

    reward_structure = {
        4: BaseReward(reward=[-1, 0], p=[0.2, 0.8], seed=seed),
        5: BaseReward(reward=[-1, 0], p=[0.8, 0.2], seed=seed),
        6: BaseReward(reward=[1, 0], p=[0.8, 0.2], seed=seed),
        7: BaseReward(reward=[1, 0], p=[0.2, 0.8], seed=seed),
    }

    if starting_positions is None:
        condition_out = (None, ([0, 1, 2, 3],))
    else:
        condition_out = (None, (starting_positions))

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        from ..pygame_render.stimuli import BaseDisplay, BaseText, TimedAction
        from ..pygame_render.task_stims import FormatText, FormatTextReward

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        base_position = (window_size // 2, window_size // 2)

        reward_disp = FormatTextReward(
            "You gain: {0}", 1000, textposition=base_position, target="reward"
        )

        earnings_text = FormatTextReward(
            "You have gained: {0}",
            500,
            textposition=base_position,
            target="total_reward",
        )

        def first_step(stim):
            return [
                BaseDisplay(None, 500),
                BaseText(stim, 1000, textposition=base_position),
                BaseDisplay(None, 500),
                BaseText("x", 100, textposition=base_position),
                TimedAction(500),
            ]

        final_disp = [
            BaseDisplay(None, 500),
            reward_disp,
            earnings_text,
        ]

        info_dict = {
            0: {"human": first_step("A")},
            1: {"human": first_step("B")},
            2: {"human": first_step("C")},
            3: {"human": first_step("D")},
            4: {"human": final_disp},
            5: {"human": final_disp},
            6: {"human": final_disp},
            7: {"human": final_disp},
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
