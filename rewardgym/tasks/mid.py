from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward


def get_mid(
    starting_positions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    **kwargs
):

    environment_graph = {
        0: [7, 5],  # big lose
        1: [7, 6],  # small lose
        2: [7, 7],  # control
        3: [8, 7],  # small win
        4: [9, 7],  # small lose
        5: [],  # big lose - lose
        6: [],  # small lose - lose
        7: [],  # nothing
        8: [],  # small win - win
        9: [],  # large win - win
    }

    reward_structure = {
        5: BaseReward(-5),
        6: BaseReward(-1),
        7: BaseReward(0),
        8: BaseReward(1),
        9: BaseReward(5),
    }

    if starting_positions is None:
        condition_out = (None, ([0, 1, 2, 3, 4], [0.225, 0.225, 0.1, 0.225, 0.225]))
    else:
        condition_out = (None, starting_positions)

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseDisplay, BaseText, TimedAction
        from ..pygame_render.task_stims import feedback_block

        base_position = (window_size // 2, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        def first_step(stim1, stim2):
            return [
                BaseDisplay(None, 500),
                BaseText(stim1, 1000, textposition=base_position),
                BaseDisplay(None, 500),
                BaseText(stim2, 200, textposition=base_position),
                TimedAction(500),
            ]

        final_display = [
            BaseDisplay(None, 500),
            reward_disp,
            earnings_text,
        ]

        info_dict = {
            0: {"human": first_step("LL", "x")},
            1: {"human": first_step("LL", "x")},
            2: {"human": first_step("O", "o")},
            3: {"human": first_step("W", "+")},
            4: {"human": first_step("WW", "+")},
            5: {"human": final_display},
            6: {"human": final_display},
            7: {"human": final_display},
            8: {"human": final_display},
            9: {"human": final_display},
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
