import warnings
from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import DriftingReward


def get_two_step(conditions=None, render_backend=None, window_size=None):

    environment_graph = {
        0: ([1, 2], 0.8),
        1: [3, 4],  # env two
        2: [5, 6],  # control
        3: [],  # small win
        4: [],  # small lose
        5: [],  # big lose - lose
        6: [],  # small lose - lose
    }

    reward_structure = {
        3: DriftingReward(seed=123),
        4: DriftingReward(seed=154),
        5: DriftingReward(seed=895),
        6: DriftingReward(seed=698),
    }

    if conditions is None:
        condition_out = (None, ([0],))
    else:
        warnings.warn("Two-step does not use conditions.")

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import feedback_block

        base_position = (window_size // 2, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        final_display = [
            BaseDisplay(None, 1),
            reward_disp,
            earnings_text,
        ]

        def first_step(text):
            return [
                BaseDisplay(None, 1),
                BaseText("+", 500, textposition=base_position),
                BaseDisplay(None, 1),
                BaseText(text, 50, textposition=base_position),
                BaseAction(),
            ]

        info_dict = {
            0: {"human": first_step("A       or       B")},
            1: {"human": first_step("C       or       D")},
            2: {"human": first_step("E       or       F")},
            3: {"human": final_display},
            4: {"human": final_display},
            5: {"human": final_display},
            6: {"human": final_display},
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
