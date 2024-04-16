import itertools
from typing import List, Union

import numpy as np


def check_elements_in_list(check_list: list, check_set: List):

    return all([ii in check_set for ii in check_list])


def unpack_conditions(conditions: tuple = None, episode: int = None):

    condition = get_condition_state(conditions=conditions[0], episode=episode)
    starting_position = get_condition_state(conditions=conditions[1], episode=episode)

    return condition, starting_position


def get_condition_state(
    conditions: Union[None, List, tuple] = None, episode: int = None
):

    if conditions is None:
        current_condition = conditions
    elif isinstance(conditions, List):
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


def get_starting_nodes(graph: dict) -> List:
    """
    Returns the starting nodes of a graph.

    Parameters
    ----------
    graph : dict
        A dictionary of acyclic directed graph(s).

    Returns
    -------
    List
        the starting position of each graph.
    """

    terminals = [ii[0] if isinstance(ii, tuple) else ii[:] for ii in graph.values()]
    terminals = list(itertools.chain.from_iterable(terminals))
    nodes = list(graph.keys())
    starting_nodes = list(set(nodes) - set(terminals))

    return starting_nodes
