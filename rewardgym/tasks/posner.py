from collections import defaultdict
from typing import Literal

from ..reward_classes import BaseReward
from ..utils import check_seed
from .utils import check_conditions_not_following


def get_posner(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed=112,
    key_dict=None,
    **kwargs,
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
                0: "selection",
                1: "cue-left",
                2: "cue-right",
                3: "target-left",
                4: "target-right",
                5: "win",
                6: "lose",
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

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info("posner", seed=seed, key_dict=key_dict)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_posner_configs(stimulus_set: str = "1"):
    seed = check_seed(int(stimulus_set))

    condition_dict = {
        "cue-left-target-left": {0: {0: 1}, 1: {0: 3}},
        "cue-left-target-right": {0: {0: 1}, 1: {0: 4}},
        "cue-right-target-right": {0: {0: 2}, 2: {0: 4}},
        "cue-right-target-left": {0: {0: 2}, 2: {0: 3}},
    }

    # 20 trials in each condition template
    condition_template_80_20 = (
        ["cue-left-target-left"] * 8
        + ["cue-left-target-right"] * 2
        + ["cue-right-target-right"] * 8
        + ["cue-right-target-left"] * 2
    )

    condition_template_90_10 = (
        ["cue-left-target-left"] * 9
        + ["cue-left-target-right"] * 1
        + ["cue-right-target-right"] * 9
        + ["cue-right-target-left"] * 1
    )

    condition_template_70_30 = (
        ["cue-left-target-left"] * 7
        + ["cue-left-target-right"] * 3
        + ["cue-right-target-right"] * 7
        + ["cue-right-target-left"] * 3
    )

    condition_template_60_40 = (
        ["cue-left-target-left"] * 6
        + ["cue-left-target-right"] * 4
        + ["cue-right-target-right"] * 6
        + ["cue-right-target-left"] * 4
    )

    iti_template = [0.5, 0.75, 1.0, 1.25] * 10
    isi_template = [0.4, 0.6] * 20

    n_blocks_condition = 4

    condition_template_sets = seed.choice(
        [
            condition_template_60_40 * 2,
            condition_template_70_30 * 2,
            condition_template_80_20 * 2,
            condition_template_90_10 * 2,
        ],
        size=n_blocks_condition,
        replace=False,
    )

    dont_follow = ["cue-left-target-right", "cue-right-target-left"]

    conditions, isi, iti = [], [], []

    for cn in range(n_blocks_condition):
        reject = True

        while reject:
            condition_template = seed.choice(
                a=condition_template_sets[cn], size=40, replace=False
            ).tolist()

            check = check_conditions_not_following(condition_template, dont_follow, 1)

            if check and (
                len(conditions) == 0 or conditions[-1] != condition_template[0]
            ):
                conditions.extend(condition_template)
                isi.extend(seed.permutation(isi_template).tolist())
                iti.extend(seed.permutation(iti_template).tolist())
                reject = False

    config = {
        "name": "posner",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
        "add_remainder": True,
        "breakpoints": [79],
        "break_duration": 45,
    }

    return config
