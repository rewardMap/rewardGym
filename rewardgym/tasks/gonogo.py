from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import PseudoRandomReward
from ..utils import check_seed
from .utils import check_conditions_present


def get_gonogo(
    starting_positions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
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

    if starting_positions is None:
        condition_out = (None, ([0, 1, 2, 3],))
    else:
        condition_out = (None, (starting_positions))

    info_dict = defaultdict(int)
    info_dict.update(
        {"position": {0: "go-win", 1: "go-punish", 2: "nogo-win", 3: "nogo-punish"}}
    )

    if render_backend == "pygame":

        from ..pygame_render.stimuli import BaseDisplay, BaseText, TimedAction
        from ..pygame_render.task_stims import FormatText, FormatTextReward

        if window_size is None:
            return ValueError("window_size needs to be defined!")

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
            0: {"human": first_step("A")},
            1: {"human": first_step("B")},
            2: {"human": first_step("C")},
            3: {"human": first_step("D")},
            4: {"human": final_disp},
            5: {"human": final_disp},
            6: {"human": final_disp},
            7: {"human": final_disp},
        }

        info_dict.update(pygame_dict)

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict


def generate_gonogo_configs(stimulus_set: str = "1"):

    seed = check_seed(int(stimulus_set))

    condition_dict = {
        "go-win": {0: {0: 1}},
        "go-punish": {0: {0: 2}},
        "nogo-win": {0: {0: 3}},
        "nogo-punish": {0: {0: 4}},
    }

    condition_template = ["go-win", "go-punish", "nogo-win", "nogo-punish"] * 15  # 80 %
    iti_template = [0.75, 1.0, 1.25, 1.5] * 15
    isi_template = [0.25, 0.75, 1.125, 1.75, 2.0] * 12  # 5 * 12 = 60

    n_blocks = 3

    check = False
    while not check:
        conditions = seed.choice(a=condition_template, size=60, replace=False).tolist()
        check = check_conditions_present(conditions[:10], list(condition_dict.keys()))

    isi = seed.choice(isi_template, size=60, replace=False).tolist()
    iti = seed.choice(iti_template, size=60, replace=False).tolist()

    for _ in range(n_blocks - 1):
        conditions.extend(
            seed.choice(a=condition_template, size=60, replace=False).tolist()
        )
        isi.extend(seed.choice(isi_template, size=60, replace=False).tolist())
        iti.extend(seed.choice(iti_template, size=60, replace=False).tolist())

    config = {
        "name": "gonogo",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_target": "location",
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
    }

    return config
