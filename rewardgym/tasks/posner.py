from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward
from ..utils import check_seed


def get_posner(
    render_backend: Literal["pygame", "psychopy"] = None, seed=112, **kwargs
):

    environment_graph = {
        0: ({0: ([1, 2], 0.5), "skip": True}),
        1: ({0: ([3, 4], 0.8)}),  # cue left
        2: ({0: ([4, 3], 0.8)}),  # cue right
        3: [5, 6],  # target / reward left
        4: [6, 5],  # target /reward right
        5: [],  # Win
        6: [],  # Lose
    }

    reward_structure = {
        5: BaseReward([1]),
        6: BaseReward([0]),
    }

    info_dict = defaultdict(int)
    info_dict.update(
        {
            "position": {
                0: "cue-left",
                1: "cue-right",
                2: "target-left",
                3: "target-right",
                4: "win",
                5: "lose",
            }
        }
    )

    if render_backend == "pygame":

        window_size = 256

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import feedback_block

        base_position = (window_size // 2, window_size // 2)
        left_position = (window_size // 2 - window_size // 4, window_size // 2)
        right_position = (window_size // 2 + window_size // 4, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        def first_step(img1, pos):
            return [
                BaseDisplay(None, 1),
                BaseText("+", 1000, textposition=base_position),
                BaseDisplay(None, 1),
                BaseText(img1, 500, textposition=base_position),
                BaseDisplay(None, 1),
                BaseText("x", 500, textposition=pos),
                BaseAction(),
            ]

        final_display = [
            BaseDisplay(None, 1),
            reward_disp,
            earnings_text,
        ]

        pygame_dict = {
            0: {"pygame": first_step("<", left_position)},
            1: {"pygame": first_step("<", right_position)},
            2: {"pygame": first_step(">", left_position)},
            3: {"pygame": first_step(">", right_position)},
            4: {"pygame": final_display},
            5: {"pygame": final_display},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        psychopy_dict, _ = get_psychopy_info("risk-sensitive", seed=seed)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_posner_configs(stimulus_set: str = "1"):

    seed = check_seed(222)
    condition_dict = {
        "cue-left-valid": {0: {0: 1}, 1: {0: 3}},
        "cue-left-invalid": {0: {0: 1}, 1: {0: 4}},
        "cue-right-valid": {0: {0: 2}, 2: {0: 4}},
        "cue-right-invalid": {0: {0: 2}, 2: {0: 3}},
    }

    condition_template = (
        ["cue-left-valid"] * 4
        + ["cue-left-invalid"]
        + ["cue-right-valid"] * 4
        + ["cue-right-invalid"]
    )

    iti_template = [1.5, 2.125, 2.75, 3.375, 4.0] * 2
    isi_template = [0.4, 0.6] * 5

    n_trials_per_condition = 10

    conditions = seed.choice(a=condition_template, size=10, replace=False).tolist()
    isi = seed.choice(isi_template, size=10, replace=False).tolist()
    iti = seed.choice(iti_template, size=10, replace=False).tolist()

    for _ in range(n_trials_per_condition - 1):
        reject = True
        while reject:
            condition_template = seed.choice(
                a=condition_template, size=10, replace=False
            ).tolist()

            if conditions[-1] != condition_template[0]:
                reject = False
                conditions.extend(condition_template)
                isi.extend(seed.choice(isi_template, size=10, replace=False).tolist())
                iti.extend(seed.choice(iti_template, size=10, replace=False).tolist())

    config = {
        "name": "posner",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
    }

    return config
