from typing import Union

import numpy as np


def check_elements_in_list(check_list: list, check_set: list):

    return all([ii in check_set for ii in check_list])


def unpack_conditions(conditions: tuple = None, episode: int = None):

    condition = get_condition_state(conditions=conditions[0], episode=episode)
    starting_position = get_condition_state(conditions=conditions[1], episode=episode)

    return condition, starting_position


def get_condition_state(
    conditions: Union[None, list, tuple] = None, episode: int = None
):

    if conditions is None:
        current_condition = conditions
    elif isinstance(conditions, list):
        current_condition = conditions[episode]
    elif isinstance(conditions, tuple):
        if len(conditions) == 2:
            current_condition = np.random.choice(conditions[0], p=conditions[1])
        else:
            current_condition = np.random.choice(conditions[0])

    return current_condition
