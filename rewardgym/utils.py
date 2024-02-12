import itertools
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


def check_seed(seed: Union[np.random.Generator, int] = 1234):

    if isinstance(seed, np.random.Generator):
        return seed
    else:
        return np.random.default_rng(seed)


def get_starting_nodes(graph: dict):
    """
    Finds the starting position of a graph dictionary. I.e. positions which cannot
    be accessed from any other position in the directed graph.

    :param graph: _description_
    :type graph: dict
    :return: _description_
    :rtype: _type_
    """

    terminals = [ii[0] if isinstance(ii, tuple) else ii[:] for ii in graph.values()]
    terminals = list(itertools.chain.from_iterable(terminals))
    nodes = list(graph.keys())
    starting_node = list(set(nodes) - set(terminals))

    return starting_node
