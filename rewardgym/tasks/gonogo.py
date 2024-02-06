from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import BaseReward


def get_gonogo(conditions=None, render_backend=None, window_size=None):

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
        4: BaseReward(reward=[-1, 0], p=[0.2, 0.8]),
        5: BaseReward(reward=[-1, 0], p=[0.8, 0.2]),
        6: BaseReward(reward=[1, 0], p=[0.8, 0.2]),
        7: BaseReward(reward=[1, 0], p=[0.2, 0.8]),
    }

    if conditions is None:
        condition_out = (None, ([0, 1, 2, 3]))

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        raise NotImplementedError("Pygame implementation still ongoing")

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
