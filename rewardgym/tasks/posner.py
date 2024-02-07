from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward


def get_posner(
    starting_position: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
):

    environment_graph = {
        0: [4, 5],  # left left
        1: [5, 4],  # left right
        2: [4, 5],  # right left
        3: [5, 4],  # right right
        4: [],  # Win
        5: [],  # Lose
    }

    reward_structure = {
        4: BaseReward([1]),
        5: BaseReward([0]),
    }

    if starting_position is None:
        condition_out = (None, ([0, 1, 2, 3], [0.4, 0.1, 0.1, 0.4]))
    else:
        condition_out = (None, starting_position)

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatText, FormatTextReward

        base_position = (window_size // 2, window_size // 2)
        left_position = (window_size // 2 - window_size // 4, window_size // 2)
        right_position = (window_size // 2 + window_size // 4, window_size // 2)

        reward_disp = FormatTextReward(
            "You gain: {0}", 1000, textposition=base_position
        )

        earnings_text = FormatText(
            "You have gained: {0}", 500, condition_text=None, textposition=base_position
        )

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("<", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("x", 500, textposition=left_position),
                    BaseAction(),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("<", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("x", 500, textposition=right_position),
                    BaseAction(),
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText(">", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("x", 500, textposition=left_position),
                    BaseAction(),
                ]
            },
            3: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText(">", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("x", 500, textposition=right_position),
                    BaseAction(),
                ]
            },
            4: {
                "human": [
                    BaseDisplay(None, 1),
                    reward_disp,
                    earnings_text,
                ]
            },
            5: {
                "human": [
                    BaseDisplay(None, 1),
                    reward_disp,
                    earnings_text,
                ]
            },
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
