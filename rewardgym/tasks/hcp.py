from collections import defaultdict
from typing import Literal

from ..reward_classes import ConditionReward
from ..utils import check_seed


def get_hcp(
    conditions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    **kwargs
):

    environment_graph = {
        0: [1, 2],  # go - win
        1: [],  # no go win
        2: [],  # go - no punish
    }

    reward = ConditionReward()

    reward_structure = {1: reward, 2: reward}

    if conditions is None:
        condition_out = (([0, 1, 2], [0.45, 0.1, 0.45]), ([0],))
    else:
        condition_out = (conditions, ([0],))

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatText, feedback_block

        base_position = (window_size // 2, window_size // 2)

        left_text = {1: [5], 2: [1, 2, 3, 4], 0: [6, 7, 8, 9]}
        right_text = {1: [5], 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]}

        reward_disp, earnings_text = feedback_block(base_position)

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("< or >", 500, textposition=base_position),
                    BaseAction(),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("<", 1000, textposition=base_position),
                    FormatText(
                        "Card: {0}",
                        1000,
                        condition_text=left_text,
                        textposition=base_position,
                    ),
                    reward_disp,
                    earnings_text,
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText(">", 1000, textposition=base_position),
                    FormatText(
                        "Card: {0}",
                        1000,
                        condition_text=right_text,
                        textposition=base_position,
                    ),
                    reward_disp,
                    earnings_text,
                ]
            },
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict


def generate_hcp_configs(stimulus_set: str = "1"):

    seed = check_seed(987)
    # 0 = loss, 1, = neutral, 2= win 1
    lose1 = [0, 0, 0, 0, 0, 0, 1, 1]
    lose2 = [0, 0, 0, 0, 0, 0, 2, 2]
    lose3 = [0, 0, 0, 0, 0, 0, 1, 2]

    win1 = [2, 2, 2, 2, 2, 2, 1, 1]
    win2 = [2, 2, 2, 2, 2, 2, 0, 0]
    win3 = [2, 2, 2, 2, 2, 2, 1, 0]

    conditions = []
    for block in [lose1, win1, lose2, win2, lose3, win3]:
        conditions.extend(seed.choice(block, size=8, replace=False).tolist())

    config = {
        "name": "hcp",
        "stimulus_set": stimulus_set,
        "isi": [],
        "condition": conditions,
        "condition_target": "condition",
        "ntrials": len(conditions),
        "update": None,
    }

    return config
