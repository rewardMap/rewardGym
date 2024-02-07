import itertools
from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward


def get_risk_sensitive(
    conditions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
):

    environment_graph = {
        0: [1, 2, 3],  # win - go (action1)
        1: [],  # punish - go (action1)
        2: [],  # win - nogo (action2)
        3: [],  # punish - nogo (action2)
    }

    reward_structure = {
        1: BaseReward(reward=[1, 0], p=[0.2, 0.8]),
        2: BaseReward(reward=[1, 0], p=[0.5, 0.5]),
        3: BaseReward(reward=[1, 0], p=[0.8, 0.2]),
    }

    action_space = list(reward_structure.keys())
    action_map = {}
    condition_space = action_space + list(itertools.permutations(action_space, 2))
    for n, ii in enumerate(condition_space):
        if isinstance(ii, tuple):
            action_map[n] = {0: ii[0] - 1, 1: ii[1] - 1}
        else:
            action_map[n] = {0: ii - 1}

    if conditions is None:
        condition_out = (((list(action_map.keys()),), ([0],)), action_map)
    else:
        condition_out = ((conditions, ([0],)), action_map)

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import (
            FormatText,
            FormatTextReward,
            FormatTextRiskSensitive,
        )

        base_postion = (window_size // 2, window_size // 2)

        reward_disp = FormatTextReward("You gain: {0}", 1000, textposition=base_postion)

        earnings_text = FormatText(
            "You have gained: {0}", 500, condition_text=None, textposition=base_postion
        )

        stim = FormatTextRiskSensitive(
            "{0} --------- {1}",
            50,
            condition_text=action_map,
            textposition=base_postion,
        )

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 500, textposition=base_postion),
                    BaseDisplay(None, 1),
                    stim,
                    BaseAction(),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 1),
                    reward_disp,
                    earnings_text,
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 1),
                    reward_disp,
                    earnings_text,
                ]
            },
            3: {
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
