from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward
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

    reward_structure = {
        1: BaseReward([-0.5, 0, 1.0], p=[0.4, 0.2, 0.4]),
        2: BaseReward([-0.5, 0, 1.0], p=[0.4, 0.2, 0.4]),
    }

    info_dict = defaultdict(int)
    info_dict.update({"condition": {0: "lose", 1: "neutral", 2: "win"}})

    if render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatText, feedback_block

        base_position = (window_size // 2, window_size // 2)

        left_text = {1: [5], 2: [1, 2, 3, 4], 0: [6, 7, 8, 9]}
        right_text = {1: [5], 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]}

        reward_disp, earnings_text = feedback_block(base_position)

        pygame_dict = {
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

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy":
        pass

    return environment_graph, reward_structure, info_dict


def generate_hcp_configs(stimulus_set: str = "1"):

    seed = check_seed(987)
    condition_dict = {
        "win": {"reward": 1},
        "lose": {"reward": -0.5},
        "neutral": {"reward": 0},
    }
    # 0 = loss, 1, = neutral, 2= win 1
    lose1 = ["lose", "lose", "lose", "lose", "lose", "lose", "neutral", "neutral"]
    lose2 = ["lose", "lose", "lose", "lose", "lose", "lose", "win", "win"]
    lose3 = ["lose", "lose", "lose", "lose", "lose", "lose", "neutral", "win"]

    win1 = ["win", "win", "win", "win", "win", "win", "neutral", "neutral"]
    win2 = ["win", "win", "win", "win", "win", "win", "lose", "lose"]
    win3 = ["win", "win", "win", "win", "win", "win", "neutral", "lose"]

    conditions = []
    for block in [lose1, win1, lose2, win2, lose3, win3]:
        conditions.extend(seed.choice(block, size=8, replace=False).tolist())

    config = {
        "name": "hcp",
        "stimulus_set": stimulus_set,
        "isi": [],
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": None,
    }

    return config
