import itertools
from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward


def get_risk_sensitive(
    conditions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
    **kwargs
):

    environment_graph = {
        0: [1, 2, 3, 4, 5],  # win - go (action1)
        1: [],  # Deterministic 0
        2: [],  # Deterministic 20
        3: [],  # Deterministic 40
        4: [],  # Probabilistic 0 / 40
        5: [],  # Probabilistic 0 / 80
    }

    reward_structure = {
        1: BaseReward(reward=[0], seed=seed),
        2: BaseReward(reward=[20], seed=seed),
        3: BaseReward(reward=[40], seed=seed),
        4: BaseReward(reward=[40, 0], p=[0.5, 0.5], seed=seed),
        5: BaseReward(reward=[80, 0], p=[0.5, 0.5], seed=seed),
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

    # Conditions of importance: 0, 1, 2, 3, 4 = single display
    # Risky trials, with same EV:
    # 20 vs 0 / 40 = 11 and 18
    # 40 vs 0 / 80 = 16 and 23
    # 20 vs 0 / 80 = 12 and 22
    # Dominated
    # 40 vs 0 / 40 = 15 and 9
    # 20 vs 0 = 5 and 9
    # 40 vs 0 = 6 and 13
    # 0 vs 0 / 20 = 7 and 17
    # 0 vs 0 / 40 = 12 and 21

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatTextRiskSensitive, feedback_block

        base_position = (window_size // 2, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        stim = FormatTextRiskSensitive(
            "{0} --------- {1}",
            50,
            condition_text=action_map,
            textposition=base_position,
        )

        final_display = [
            BaseDisplay(None, 1),
            reward_disp,
            earnings_text,
        ]

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    stim,
                    BaseAction(),
                ]
            },
            1: {"human": final_display},
            2: {"human": final_display},
            3: {"human": final_display},
            4: {"human": final_display},
            5: {"human": final_display},
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict


def generate_risk_senistive_configs(stimulus_set: str = "1"):
    raise NotImplementedError
