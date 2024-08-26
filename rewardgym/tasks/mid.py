from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward
from ..utils import check_seed


def get_mid(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed=111,
    key_dict=None,
    **kwargs,
):
    environment_graph = {
        0: {0: ([1, 2, 3, 4, 5], 0.2), "skip": True},
        1: [8, 6],  # big lose
        2: [8, 7],  # small lose
        3: [8, 8],  # control
        4: [9, 8],  # small win
        5: [10, 8],  # small lose
        6: [],  # big lose - lose
        7: [],  # small lose - lose
        8: [],  # nothing
        9: [],  # small win - win
        10: [],  # large win - win
    }

    reward_structure = {
        6: BaseReward(-5),
        7: BaseReward(-1),
        8: BaseReward(0),
        9: BaseReward(1),
        10: BaseReward(5),
    }

    info_dict = defaultdict(int)
    info_dict.update(
        {
            "position": {
                0: "large-loss",
                1: "small-loss",
                2: "neutral",
                3: "small-win",
                4: "large-win",
            }
        }
    )

    if render_backend == "pygame":
        from ..pygame_render.stimuli import BaseDisplay, BaseText, TimedAction
        from ..pygame_render.task_stims import feedback_block

        window_size = 256
        base_position = (window_size // 2, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        def first_step(stim1, stim2):
            return [
                BaseDisplay(None, 500),
                BaseText(stim1, 2000, textposition=base_position),
                BaseDisplay(None, 500),
                BaseText(stim2, 200, textposition=base_position),
                TimedAction(500),
            ]

        final_display = [
            BaseDisplay(None, 500),
            reward_disp,
            earnings_text,
        ]

        pygame_dict = {
            1: {"pygame": first_step("LL", "x")},
            2: {"pygame": first_step("LL", "x")},
            3: {"pygame": first_step("O", "o")},
            4: {"pygame": first_step("W", "+")},
            5: {"pygame": first_step("WW", "+")},
            6: {"pygame": final_display},
            7: {"pygame": final_display},
            8: {"pygame": final_display},
            9: {"pygame": final_display},
            10: {"pygame": final_display},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        if key_dict is None:
            key_dict = {"space": 0}

        psychopy_dict, _ = get_psychopy_info("mid", seed=seed, key_dict=key_dict)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_mid_configs(stimulus_set: 111):
    seed = check_seed(stimulus_set)
    # 0 & 1 = win, 2  = neutral, 3 & 4 = lose
    condition_dict = {
        "loss-large": {0: {0: 1}},
        "loss-small": {0: {0: 2}},
        "neutral": {0: {0: 3}},
        "win-small": {0: {0: 4}},
        "win-large": {0: {0: 5}},
    }

    condition_template = [
        "loss-large",
        "loss-small",
        "neutral",
        "win-small",
        "win-large",
    ]
    isi_template = [1.5, 2.125, 2.75, 3.375, 4.0]

    # n_trials_per_condition = 20
    n_trials_per_condition = 10

    conditions = seed.choice(a=condition_template, size=5, replace=False).tolist()
    isi = seed.choice(isi_template, size=5, replace=False).tolist()

    for _ in range(n_trials_per_condition - 1):
        reject = True
        while reject:
            condition_template = seed.choice(
                a=condition_template, size=5, replace=False
            ).tolist()

            if conditions[-1] != condition_template[0]:
                reject = False
                conditions.extend(condition_template)
                isi.extend(seed.choice(isi_template, size=5, replace=False).tolist())
    iti = [2] * len(conditions)

    config = {
        "name": "mid",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "reward": iti,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "reward"],
    }

    return config
