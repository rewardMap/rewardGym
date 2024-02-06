from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import BaseReward


def get_posner(conditions=None, render_backend=None, window_size=None):

    environment_graph = {
        0: [4, 5],  # left left
        1: [5, 4],  # left right
        2: [4, 5],  # right left
        3: [5, 4],  # right right
        4: [],  # Win
        5: [],  # Lose
    }

    reward_structure = {
        4: BaseReward([1]),
        5: BaseReward([0]),
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
