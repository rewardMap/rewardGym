from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward
from ..utils import check_seed


def get_hcp(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed=100,
    key_dict=None,
    **kwargs,
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
        window_size = 256
        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatText, feedback_block

        base_position = (window_size // 2, window_size // 2)

        left_text = {1: [5], 2: [1, 2, 3, 4], 0: [6, 7, 8, 9]}
        right_text = {1: [5], 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]}

        reward_disp, earnings_text = feedback_block(base_position)

        pygame_dict = {
            0: {
                "pygame": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_position),
                    BaseDisplay(None, 1),
                    BaseText("< or >", 500, textposition=base_position),
                    BaseAction(),
                ]
            },
            1: {
                "pygame": [
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
                "pygame": [
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

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info("hcp", seed=seed, key_dict=key_dict)
        info_dict.update(psychopy_dict)

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

    block_order_win = (
        seed.permutation([win1, win2, win3]).tolist()
        + seed.choice([win1, win2, win3], size=1, replace=True).tolist()
    )

    block_order_lose = (
        seed.permutation([lose1, lose2, lose3]).tolist()
        + seed.choice([lose1, lose2, lose3], size=1, replace=False).tolist()
    )

    block_order1 = seed.permutation(block_order_win[:2] + block_order_lose[:2]).tolist()
    block_order2 = seed.permutation(block_order_win[2:] + block_order_lose[2:]).tolist()

    conditions = []
    for block in block_order1 + block_order2:
        conditions.extend(seed.choice(block, size=8, replace=False).tolist())

    config = {
        "name": "hcp",
        "stimulus_set": stimulus_set,
        "isi": [],
        "wait": [0.0] * len(conditions),
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["wait"],
        "add_remainder": False,
        "breakpoints": [7, 15, 23, 31, 39, 47, 56],
        "break_duration": 15,
    }

    return config
