import itertools
from collections import defaultdict
from typing import Union

import numpy as np

from ..reward_classes import BaseReward


def get_risk_sensitive(conditions=None, render_backend=None, window_size=None):

    environment_graph = {
        0: [1, 2, 3],  # win - go (action1)
        1: [],  # punish - go (action1)
        2: [],  # win - nogo (action2)
        3: [],  # punish - nogo (action2)
    }

    reward_structure = {
        1: BaseReward(reward=[1, 0], p=[0.2, 0.8]),
        2: BaseReward(reward=[1, 0], p=[0.5, 0.5]),
        3: BaseReward(reward=[1, 0], p=[0.8, 0.2]),
    }

    if conditions is None:
        action_space = list(reward_structure.keys())
        action_map = {}
        condition_space = action_space + list(itertools.permutations(action_space, 2))
        for n, ii in enumerate(condition_space):
            if isinstance(ii, tuple):
                action_map[n] = {0: ii[0] - 1, 1: ii[1] - 1}
            else:
                action_map[n] = {0: ii - 1}

        condition_out = ((list(action_map.keys()), ([0])), action_map)

    if render_backend is None:
        info_dict = defaultdict(int)

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        raise NotImplementedError("Pygame implementation still ongoing")

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict