import warnings
from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import DriftingReward
from ..utils import check_seed


def get_two_step(
    conditions=None, render_backend=None, window_size=None, seed=111, **kwargs
):

    seed = check_seed(seed)

    environment_graph = {
        0: ([1, 2], 0.7),
        1: [3, 4],
        2: [5, 6],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    reward_structure = {
        3: DriftingReward(seed=seed, p=None),
        4: DriftingReward(seed=seed, p=None),
        5: DriftingReward(seed=seed, p=None),
        6: DriftingReward(seed=seed, p=None),
    }

    if conditions is None:
        condition_out = (None, ([0],))
    else:
        warnings.warn("Two-step does not use conditions.")

    info_dict = defaultdict(int)

    if render_backend == "pygame":

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

        pygame_dict = {
            0: {"human": first_step("A       or       B")},
            1: {"human": first_step("C       or       D")},
            2: {"human": first_step("E       or       F")},
            3: {"human": final_display},
            4: {"human": final_display},
            5: {"human": final_display},
            6: {"human": final_display},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict


def generate_two_step_configs(set: str = "1"):

    configs = {
        "name": "two-step",
        "set": set,
        "iti": None,
        "isi": None,
        "condition": None,
        "condition_target": "condition",
        "ntrials": 160,
        "update": None,
    }

    return configs
