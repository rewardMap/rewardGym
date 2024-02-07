from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward


def get_mid(
    starting_positions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
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

        from ..pygame_render.stimuli import BaseDisplay, TimedAction
        from ..pygame_render.task_stims import FormatText, FormatTextMid

        base_postion = (window_size // 2, window_size // 2)

        reward_text = {5: [-5], 6: [-1], 7: [0], 8: [1], 9: [5]}
        reward_disp = FormatTextMid(
            "You gain: {0}", 1000, condition_text=reward_text, textposition=base_postion
        )

        earnings_text = FormatText(
            "You have gained: {0}", 500, condition_text=None, textposition=base_postion
        )

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/LoseBig.BMP", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/LoseProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/LoseSmall.BMP", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/LoseProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/Neutral.BMP", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/NeutralProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            3: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinSmall.BMP", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
                ]
            },
            4: {
                "human": [
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinBig.BMP", 1000),
                    BaseDisplay(None, 500),
                    BaseDisplay("stimuli/WinProbe.BMP", 200),
                    TimedAction(500),
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
            8: {
                "human": [
                    BaseDisplay(None, 500),
                    reward_disp,
                    earnings_text,
                ]
            },
            9: {
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
