from collections import defaultdict

from ..reward_classes import DriftingReward
from ..utils import check_seed
from .utils import check_conditions_not_following


def get_two_step(render_backend=None, seed=111, key_dict=None, **kwargs):
    seed = check_seed(seed)

    environment_graph = {
        0: ([1, 2], 0.7),
        1: [3, 4],
        2: [5, 6],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    reward_structure = {
        3: DriftingReward(seed=seed, p=None),
        4: DriftingReward(seed=seed, p=None),
        5: DriftingReward(seed=seed, p=None),
        6: DriftingReward(seed=seed, p=None),
    }

    info_dict = defaultdict(int)

    if render_backend == "pygame":
        window_size = 256

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import feedback_block

        base_position = (window_size // 2, window_size // 2)

        reward_disp, earnings_text = feedback_block(base_position)

        final_display = [
            BaseDisplay(None, 1),
            reward_disp,
            earnings_text,
        ]

        def first_step(text):
            return [
                BaseDisplay(None, 1),
                BaseText("+", 500, textposition=base_position),
                BaseDisplay(None, 1),
                BaseText(text, 50, textposition=base_position),
                BaseAction(),
            ]

        pygame_dict = {
            0: {"pygame": first_step("A       or       B")},
            1: {"pygame": first_step("C       or       D")},
            2: {"pygame": first_step("E       or       F")},
            3: {"pygame": final_display},
            4: {"pygame": final_display},
            5: {"pygame": final_display},
            6: {"pygame": final_display},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info("two-step", seed=seed, key_dict=key_dict)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_two_step_configs(stimulus_set: str = "1"):
    condition_dict = {
        "expected-transition": {0: {0: 1, 1: 2}},
        "unexpected-transition": {0: {0: 2, 1: 1}},
        None: None,
    }
    seed = check_seed(int(stimulus_set))

    # Actually create pseudo-random transitions:
    transition_list = ["expected-transition"] * 14 + ["unexpected-transition"] * 6
    iti_jitter = [0.1, 0.15, 0.2, 0.25, 0.3] * 4

    conditions = []
    itis = []

    for _ in range(9):
        reject = True
        itis.extend(
            seed.choice(a=iti_jitter, size=len(iti_jitter), replace=False).tolist()
        )

        while reject:
            condition_proposal = seed.choice(
                a=transition_list, size=len(transition_list), replace=False
            ).tolist()
            check = check_conditions_not_following(
                condition_proposal, ["unexpected-transition"], 1
            )

            if check:
                reject = False
                conditions.extend(condition_proposal)

    configs = {
        "name": "two-step",
        "set": stimulus_set,
        "iti": itis,
        "isi": None,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["iti"],
        "add_remainder": True,
        "breakpoints": [int(len(conditions) // 2 - 1)],
        "break_duration": 45,
    }

    return configs
