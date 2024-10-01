from collections import defaultdict

from ..reward_classes import DriftingReward
from ..utils import check_seed
from .utils import check_conditions_not_following_substring


def get_two_step_flip(render_backend=None, seed=111, key_dict=None, **kwargs):
    seed = check_seed(seed)

    environment_graph = {
        0: {0: ([1, 2, 3, 4], 0.25), "skip": True},
        1: ([5, 7], 0.7),
        2: ([7, 5], 0.7),
        3: ([6, 8], 0.7),
        4: ([8, 6], 0.7),
        5: [9, 10],  # state 2 config 1
        6: [10, 9],  # state 2 config 2
        7: [11, 12],  # state 3 config 1
        8: [12, 11],  # state 3 config 2
        9: [],  # reward state 2 stim 1
        10: [],  # reward state 2 stim 2
        11: [],  # reward state 3 stim 1
        12: [],  # reward state 3 stim 2
    }

    reward_structure = {
        9: DriftingReward(seed=seed, p=None),
        10: DriftingReward(seed=seed, p=None),
        11: DriftingReward(seed=seed, p=None),
        12: DriftingReward(seed=seed, p=None),
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


def generate_two_step_flip_configs(stimulus_set: int = 10):
    # For two-step we need some randomization of left and right displays at first
    # and second level, this means we need to also permute expected and
    # unexpected transitions - which is not too bad as we are now logging
    # explicitly

    #    1: [3, 4],
    #    2: [5, 6],

    seed = check_seed(stimulus_set)

    condition_dict = {
        "config1-expected": {0: {0: 1}, 1: {0: 5, 1: 7}},
        "config2-expected": {0: {0: 2}, 2: {0: 7, 1: 5}},
        "config3-expected": {0: {0: 3}, 3: {0: 6, 1: 8}},
        "config4-expected": {0: {0: 4}, 4: {0: 8, 1: 6}},
        "config1-unexpected": {0: {0: 1}, 1: {0: 7, 1: 5}},
        "config2-unexpected": {0: {0: 2}, 2: {0: 5, 1: 7}},
        "config3-unexpected": {0: {0: 3}, 3: {0: 8, 1: 6}},
        "config4-unexpected": {0: {0: 4}, 4: {0: 6, 1: 8}},
        None: None,
    }

    # creating conditions
    expected = [
        "config1-expected",
        "config2-expected",
        "config3-expected",
        "config4-expected",
    ]
    unexpected = [
        "config1-unexpected",
        "config2-unexpected",
        "config3-unexpected",
        "config4-unexpected",
    ]

    condition_list = []

    n_blocks = 4  # 4 blocks of 40 trials = 160 trials

    print("begin sampling")
    for _ in range(n_blocks):
        condition_list_proposal = []

        for ex in expected:
            condition_list_proposal.extend([ex] * 7)
        for ux in unexpected:
            condition_list_proposal.extend([ux] * 3)

        while True:
            condition_list_proposal = seed.permutation(condition_list_proposal).tolist()

            if check_conditions_not_following_substring(
                condition_list=condition_list_proposal,
                not_following=["unexpected"],
                window_length=1,
            ):
                condition_list.extend(condition_list_proposal)
                break

    n_trials = len(condition_list)

    configs = {
        "name": "two-step",
        "set": stimulus_set,
        "iti": [1.0] * n_trials,
        "isi": None,
        "condition": condition_list,
        "condition_dict": condition_dict,
        "ntrials": n_trials,
        "update": ["iti"],
        "add_remainder": True,
        "breakpoints": [79],
        "break_duration": 15,
    }

    return configs
