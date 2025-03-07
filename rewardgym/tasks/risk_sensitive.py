import itertools
from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward, PseudoRandomReward
from ..utils import check_seed
from .utils import check_condition_present_or, check_conditions_not_following


def get_risk_sensitive(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed: Union[int, np.random.Generator] = 1000,
    key_dict=None,
    **kwargs,
):
    seed = check_seed(seed)
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
        4: PseudoRandomReward(reward_list=[40, 40, 40, 40, 0, 0, 0, 0], seed=seed),
        5: PseudoRandomReward(reward_list=[80, 80, 80, 80, 0, 0, 0, 0], seed=seed),
    }

    action_space = list(reward_structure.keys())
    action_map = {}
    condition_space = action_space + list(itertools.permutations(action_space, 2))
    for n, ii in enumerate(condition_space):
        if isinstance(ii, tuple):
            action_map[n] = {0: ii[0] - 1, 1: ii[1] - 1}
        else:
            action_map[n] = {0: ii - 1}

    reward_meaning = {
        1: "null",
        2: "save-20",
        3: "save-40",
        4: "risky-40",
        5: "risky-80",
    }

    condition_meaning = {}
    for kk in action_map.keys():
        if len(action_map[kk]) == 2:
            condition_meaning[kk] = (
                reward_meaning[action_map[kk][0] + 1]
                + "_"
                + reward_meaning[action_map[kk][1] + 1]
            )
        elif len(action_map[kk]) == 1:
            condition_meaning[kk] = reward_meaning[action_map[kk][0] + 1]

    info_dict = defaultdict(int)
    info_dict.update({"condition-meaning": condition_meaning})

    if render_backend == "pygame":
        window_size = 256

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

        pygame_dict = {
            0: {
                "pygame": [
                    BaseDisplay(None, 1),
                    BaseText("+", 500, textposition=base_position),
                    BaseDisplay(None, 1),
                    stim,
                    BaseAction(),
                ]
            },
            1: {"pygame": final_display},
            2: {"pygame": final_display},
            3: {"pygame": final_display},
            4: {"pygame": final_display},
            5: {"pygame": final_display},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info(
            "risk-sensitive", seed=seed, key_dict=key_dict
        )
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_risk_sensitive_configs(stimulus_set: str = "1"):
    """
    Generating randomized stimulus sequences following Rosenbaum et al. 2022.
    Stimulus generation pseudo random for each block and another check is implemented, to not have two forced choices
    following each other and making sure, that one of each forced choices appears in the first 15 trials.


    Three blocks of 61 stimuli each:
    * 66 risky choices
        * 42 with equal EV
        * 24 with sure 20 vs risky 80
    * 75 forced choices (15 each)
    * 42 test trials (i.e. dominated choices, where one option has clearly higher outcome).

    ITIs are drawn from the fixed set [1.5, 2.125, 2.75, 3.375, 4.0].

    Conditions of importance:
    * 0, 1, 2, 3, 4 = forced choice
    Risky trials, with same EV:
     * 20 vs 0 / 40 = 11 and 18
     * 40 vs 0 / 80 = 16 and 23
    Risky trials, not same EV:
     * 20 vs 0 / 80 = 12 and 22
    Dominated
     * 40 vs 0 / 40 = 15 and 19
     * 20 vs 0 = 5 and 9
     * 40 vs 0 = 6 and 13
     * 0 vs 0 / 20 = 7 and 17
     * 0 vs 0 / 40 = 8 and 21
     * 20 vs 40

    All other possible conditions:
    {0: 'null',
     1: 'save-20',
     2: 'save-40',
     3: 'risky-40',
     4: 'risky-80',
     5: 'null_save-20',
     6: 'null_save-40',
     7: 'null_risky-40',
     8: 'null_risky-80',
     9: 'save-20_null',
     10: 'save-20_save-40',
     11: 'save-20_risky-40',
     12: 'save-20_risky-80',
     13: 'save-40_null',
     14: 'save-40_save-20',
     15: 'save-40_risky-40',
     16: 'save-40_risky-80',
     17: 'risky-40_null',
     18: 'risky-40_save-20',
     19: 'risky-40_save-40',
     20: 'risky-40_risky-80',
     21: 'risky-80_null',
     22: 'risky-80_save-20',
     23: 'risky-80_save-40',
     24: 'risky-80_risky-40'}

    """

    seed = check_seed(int(stimulus_set))

    blocks = 3

    itis = []
    conditions = []

    condition_dict = {
        # fixed choice:
        "null_none": {0: {0: 1, None: None}},
        "none_null": {0: {None: None, 0: 1}},
        "save-20_none": {0: {1: 2, None: None}},
        "none_save-20": {0: {None: None, 1: 2}},
        "save-40_none": {0: {2: 3, None: None}},
        "none_save-40": {0: {None: None, 2: 3}},
        "risky-40_none": {0: {3: 4, None: None}},
        "none_risky-40": {0: {None: None, 3: 4}},
        "risky-80_none": {0: {4: 5, None: None}},
        "none_risky-80": {0: {None: None, 4: 5}},
        # equal ev:
        "save-20_risky-40": {0: {1: 2, 3: 4}},
        "risky-40_save-20": {0: {3: 4, 1: 2}},
        "save-40_risky-80": {0: {2: 3, 4: 5}},
        "risky-80_save-40": {0: {4: 5, 2: 3}},
        # non equal ev:
        "save-20_risky-80": {0: {1: 2, 4: 5}},
        "risky-80_save-20": {0: {4: 5, 1: 2}},
        # Test trials:
        "save-40_risky-40": {0: {2: 3, 3: 4}},
        "risky-40_save-40": {0: {2: 3, 3: 4}},
        "null_save-20": {0: {0: 1, 1: 2}},
        "save-20_null": {0: {1: 2, 0: 1}},
        "null_save-40": {0: {0: 1, 2: 3}},
        "save-40_null": {0: {2: 3, 0: 1}},
        "null_risky-40": {0: {0: 1, 3: 4}},
        "risky-40_null": {0: {3: 4, 0: 1}},
        "null_risky-80": {0: {0: 1, 4: 5}},
        "risky-80_null": {0: {4: 5, 0: 1}},
        "save-20_save-40": {0: {1: 2, 2: 3}},
        "save-40_save-20": {0: {2: 3, 1: 2}},
    }

    for b in range(blocks):
        risky_equal_ev = [
            "save-20_risky-40",
            "risky-40_save-20",
            "save-40_risky-80",
            "risky-80_save-40",
        ] * 3 + [
            seed.choice(["save-20_risky-40", "risky-40_save-20"]),
            seed.choice(["save-40_risky-80", "risky-80_save-40"]),
        ]
        risky_non_equal_ev = ["save-20_risky-80", "risky-80_save-20"] * 4
        forced_choices = (
            [
                "none_null",
                "none_save-20",
                "none_save-40",
                "none_risky-40",
                "none_risky-80",
            ]
            * 2
            + [
                "null_none",
                "save-20_none",
                "save-40_none",
                "risky-40_none",
                "risky-80_none",
            ]
            * 2
            + [
                seed.choice(["none_null", "null_none"]),
                seed.choice(["none_save-20", "save-20_none"]),
                seed.choice(["none_save-40", "save-40_none"]),
                seed.choice(["none_risky-40", "risky-40_none"]),
                seed.choice(["none_risky-80", "risky-80_none"]),
            ]
        )

        test_trials = [
            "save-40_risky-40",
            "risky-40_save-40",
            "null_save-20",
            "save-20_null",
            "null_save-40",
            "save-40_null",
            "null_risky-40",
            "risky-40_null",
            "null_risky-80",
            "risky-80_null",
            "save-20_save-40",
            "save-40_save-20",
        ] + [
            seed.choice(
                [
                    "save-40_risky-40",
                    "risky-40_save-40",
                    "null_save-20",
                    "save-20_null",
                    "null_save-40",
                    "save-40_null",
                ]
            ),
            seed.choice(
                [
                    "null_risky-40",
                    "risky-40_null",
                    "null_risky-80",
                    "risky-80_null",
                    "save-20_save-40",
                    "save-40_save-20",
                ]
            ),
        ]

        # iti_template = [1.5, 2.125, 2.75, 3.375, 4.0] * 12 + [1.5, 2.75, 4.0]
        iti_template = [0.5, 0.75, 1.0, 1.25, 1.5] * 12 + [0.5, 1.0, 1.5]

        condition_template = (
            forced_choices + risky_equal_ev + risky_non_equal_ev + test_trials
        )

        approve = False

        while not approve:
            conditions_proposal = seed.permutation(condition_template).tolist()

            approve = (
                all(
                    [check_condition_present_or(conditions_proposal[:10], jj)]
                    for jj in [
                        (["null_none"], ["none_null"]),
                        (["none_save-20"], ["save-20_none"]),
                        (["none_save-40"], ["save-40_none"]),
                        (["none_risky-40"], ["risky-40_none"]),
                        (["none_risky-80"], ["risky-80_none"]),
                    ]
                )
                and all(
                    [
                        check_conditions_not_following(conditions_proposal, jj)
                        for jj in (
                            ["none_null", "null_none"],
                            ["none_save-20", "save-20_none"],
                            ["none_save-40", "save-40_none"],
                            ["none_risky-40", "risky-40_none"],
                            ["none_risky-80", "risky-80_none"],
                        )
                    ]
                )
                and check_conditions_not_following(conditions_proposal, test_trials)
                and all(
                    [
                        check_conditions_not_following(conditions_proposal, [jj])
                        for jj in risky_non_equal_ev + risky_equal_ev
                    ]
                )
            )

        conditions.extend(conditions_proposal)

        iti = seed.permutation(iti_template).tolist()
        itis.extend(iti)

    config = {
        "name": "risk-sensitive",
        "stimulus_set": stimulus_set,
        "isi": [],
        "iti": itis,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),  # 183
        "update": ["iti"],
        "add_remainder": True,
        "breakpoints": [60, 121],
        "break_duration": 45,
    }

    return config
