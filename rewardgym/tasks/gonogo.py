from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import PseudoRandomReward
from ..utils import check_seed
from .utils import check_conditions_present


def get_gonogo(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed: Union[int, np.random.Generator] = 1000,
    key_dict=None,
):
    environment_graph = {
        0: {0: ([1, 2, 3, 4], 0.25), "skip": True},
        1: [7, 8],  # win - go (action1)
        2: [5, 6],  # punish - go (action1)
        3: [8, 7],  # win - nogo (action2)
        4: [6, 5],  # punish - nogo (action2)
        5: [],  # Punish low
        6: [],  # Punish high
        7: [],  # Win high
        8: [],  # Win low
    }

    reward_structure = {
        5: PseudoRandomReward(reward_list=[-1, -1, 0, 0, 0, 0, 0, 0, 0, 0], seed=seed),
        6: PseudoRandomReward(
            reward_list=[-1, -1, -1, -1, -1, -1, -1, -1, 0, 0], seed=seed
        ),
        7: PseudoRandomReward(reward_list=[1, 1, 1, 1, 1, 1, 1, 1, 0, 0], seed=seed),
        8: PseudoRandomReward(reward_list=[1, 1, 0, 0, 0, 0, 0, 0, 0, 0], seed=seed),
    }

    info_dict = defaultdict(int)
    info_dict.update(
        {"position": {0: "go-win", 1: "go-punish", 2: "nogo-win", 3: "nogo-punish"}}
    )

    if render_backend == "pygame":
        from ..pygame_render.stimuli import BaseDisplay, BaseText, TimedAction
        from ..pygame_render.task_stims import FormatTextReward

        window_size = 256

        base_position = (window_size // 2, window_size // 2)

        reward_disp = FormatTextReward(
            "You gain: {0}", 1000, textposition=base_position, target="reward"
        )

        earnings_text = FormatTextReward(
            "You have gained: {0}",
            500,
            textposition=base_position,
            target="total_reward",
        )

        def first_step(stim):
            return [
                BaseDisplay(None, 500),
                BaseText(stim, 1000, textposition=base_position),
                BaseDisplay(None, 500),
                BaseText("x", 100, textposition=base_position),
                TimedAction(500),
            ]

        final_disp = [
            BaseDisplay(None, 500),
            reward_disp,
            earnings_text,
        ]

        pygame_dict = {
            0: {"pygame": first_step("A")},
            1: {"pygame": first_step("B")},
            2: {"pygame": first_step("C")},
            3: {"pygame": first_step("D")},
            4: {"pygame": final_disp},
            5: {"pygame": final_disp},
            6: {"pygame": final_disp},
            7: {"pygame": final_disp},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from ..psychopy_render import get_psychopy_info

        if key_dict is None:
            key_dict = {"space": 0}

        psychopy_dict, _ = get_psychopy_info("gonogo", seed=seed, key_dict=key_dict)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict


def generate_gonogo_configs(stimulus_set: str = "1"):
    seed = check_seed(int(stimulus_set))

    condition_dict = {
        "go-win": {0: {0: 1}},
        "go-punish": {0: {0: 2}},
        "nogo-win": {0: {0: 3}},
        "nogo-punish": {0: {0: 4}},
    }

    condition_template = ["go-win", "go-punish", "nogo-win", "nogo-punish"] * 15  # 80 %
    iti_template = [0.5, 0.75, 1.0, 1.25] * 15
    isi_template = [0.25, 0.75, 1.125, 1.75, 2.0] * 12  # 5 * 12 = 60

    n_blocks = 3

    check = False
    while not check:
        conditions = seed.permutation(condition_template).tolist()
        check = check_conditions_present(conditions[:8], list(condition_dict.keys()))

    isi = seed.permutation(isi_template).tolist()
    iti = seed.permutation(iti_template).tolist()

    for _ in range(n_blocks - 1):
        conditions.extend(seed.permutation(condition_template).tolist())
        isi.extend(seed.permutation(isi_template).tolist())
        iti.extend(seed.permutation(iti_template).tolist())

    config = {
        "name": "gonogo",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
        "add_remainder": True,
        "breakpoints": [59, 119],
        "break_duration": 45,
    }

    return config
