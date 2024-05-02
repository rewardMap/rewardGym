from collections import defaultdict
from typing import Literal, Union

import numpy as np

from ..reward_classes import BaseReward
from ..utils import check_seed


def get_gonogo(
    starting_positions: list = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
):

    environment_graph = {
        0: [6, 7],  # win - go (action1)
        1: [4, 5],  # punish - go (action1)
        2: [7, 6],  # win - nogo (action2)
        3: [5, 4],  # punish - nogo (action2)
        4: [],  # Punish low
        5: [],  # Punish high
        6: [],  # Win high
        7: [],  # Win low
    }

    reward_structure = {
        4: BaseReward(reward=[-1, 0], p=[0.2, 0.8], seed=seed),
        5: BaseReward(reward=[-1, 0], p=[0.8, 0.2], seed=seed),
        6: BaseReward(reward=[1, 0], p=[0.8, 0.2], seed=seed),
        7: BaseReward(reward=[1, 0], p=[0.2, 0.8], seed=seed),
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

    seed = check_seed(98)

    condition_template = [0, 0, 1, 1, 2, 2, 3, 3]  # 80 %
    iti_template = [0.75, 1.0, 1.25, 1.5] * 2
    isi_template = [0.25, 0.5, 0.75, 1.0] * 2

    n_trials_per_condition = 5

    conditions = seed.choice(a=condition_template, size=8, replace=False).tolist()
    isi = seed.choice(isi_template, size=8, replace=False).tolist()
    iti = seed.choice(iti_template, size=8, replace=False).tolist()

    for _ in range(n_trials_per_condition - 1):
        conditions.extend(
            seed.choice(a=condition_template, size=8, replace=False).tolist()
        )
        isi.extend(seed.choice(isi_template, size=8, replace=False).tolist())
        iti.extend(seed.choice(iti_template, size=8, replace=False).tolist())

    config = {
        "name": "gonogo",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_target": "location",
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
    }

    return config
