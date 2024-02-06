from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import BaseReward


def get_gonogo(conditions=None, render_backend=None, window_size=None):

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
        4: BaseReward(reward=[-1, 0], p=[0.2, 0.8]),
        5: BaseReward(reward=[-1, 0], p=[0.8, 0.2]),
        6: BaseReward(reward=[1, 0], p=[0.8, 0.2]),
        7: BaseReward(reward=[1, 0], p=[0.2, 0.8]),
    }

    if conditions is None:
        condition_out = (None, ([0, 1, 2, 3]))

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        from ..pygame_render.stimuli import BaseDisplay, TimedAction
        from ..pygame_render.task_stims import FormatText, FormatTextReward

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        base_postion = (window_size // 2, window_size // 2)

        reward_disp = FormatTextReward(
            "You gain: {0}", 1000, condition_text=None, textposition=base_postion
        )

        earnings_text = FormatText(
            "You have gained: {0}", 500, condition_text=None, textposition=base_postion
        )

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("template_stimuli/F000.png", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("template_stimuli/F001.png", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("template_stimuli/F002.png", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            3: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("template_stimuli/F003.png", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            4: {
                "human": [
                    BaseDisplay(None, 500),
                    reward_disp,
                    earnings_text,
                ]
            },
            5: {
                "human": [
                    BaseDisplay(None, 500),
                    reward_disp,
                    earnings_text,
                ]
            },
            6: {
                "human": [
                    BaseDisplay(None, 500),
                    reward_disp,
                    earnings_text,
                ]
            },
            7: {
                "human": [
                    BaseDisplay(None, 500),
                    reward_disp,
                    earnings_text,
                ]
            },
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict