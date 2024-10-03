import itertools
from typing import Dict, List, Union

import numpy as np


def run_single_episode(
    env,
    agent,
    starting_position: int,
    condition: int,
    update_agent: bool = True,
    step_reward: bool = False,
) -> Union[List, List, float]:
    """
    Runs a single episode of a task.

    Parameters
    ----------
    env : env.BaseEnv
        A task-environemnt.
    agent : _type_
        The agent playing the game
    starting_position : int
        Where in the graph the agent starts the task.
    condition : int
        Which condition the agent is in.
    update_agent : bool, optional
        If the agent should update internal states, by default True
    step_reward : bool, optional
        If all rewards should be triggered e.g. in two-step task, by default False

    Returns
    -------
    Union[List, List, float]
        returns the agent's observations (excluding starting point), agent's actions,
        and obtained reward.
    """
    obs, info = env.reset(agent_location=starting_position, condition=condition)

    states, actions, rewards = [], [], []

    done = False

    while not done:
        old_info = info
        action = agent.get_action(obs, info["avail-actions"])

        next_obs, reward, terminated, truncated, info = env.step(
            action, step_reward=step_reward
        )

        if update_agent:
            if "remap-actions" in old_info.keys():
                action = old_info["remap-actions"][action]

            agent.update(obs, action, reward, terminated, next_obs)

        done = terminated or truncated
        obs = next_obs

        actions.append(action)
        states.append(obs)
        rewards.append(reward)

    return states, actions, rewards


def add_to_df(
    episode_step: List,
    episode: int = None,
    condition: int = None,
    starting_position: int = None,
    df: Dict = None,
) -> Dict:
    """
    Helper function to collect outcomes of run_single_episode in a dictionary,
    which could subsequently be transformed to a pandas DataFrame.
    The columns are:
    ['index', 'episode', 'state', 'action', 'reward', 'condition', 'starting_position']

    Parameters
    ----------
    episode_step : List
        Outcomes of run_single_episode, alternatively a list of lists, that
        contains, state, action, and reward.
    episode : int, optional
        Episode counter variable, by default None
    condition : int, optional
        Condition of the episode, by default None
    starting_position : int, optional
        Where the agent started, by default None
    df : Dict, optional
        Dict to append to, if None, creates a new dict, by default None

    Returns
    -------
    Dict
        Returns a dictionary logging the current episode.
    """

    df_cols = [
        "index",
        "episode",
        "state",
        "action",
        "reward",
        "condition",
        "starting_position",
    ]
    if df is None:
        df = {ii: [] for ii in df_cols}
        index = 0
    else:
        index = df["index"][-1] + 1

    for st, ac, rew in zip(*episode_step):
        for ii, jj in zip(
            df_cols, [index, episode, st, ac, rew, condition, starting_position]
        ):
            df[ii].append(jj)

        index += 1

    return df


def check_elements_in_list(check_list: List, check_set: List) -> bool:
    """
    Checks if all elements in the check_list are included in the check

    Parameters
    ----------
    check_list : list
        List of items that should be included in check_set.
    check_set : List
        Set of items to check agains.

    Returns
    -------
    bool
        True if all elements in the check_list are included in the check_set
    """
    return all([ii in check_set for ii in check_list])


def unpack_conditions(conditions: tuple = None, episode: int = None) -> Union[int, int]:
    """
    Unpacks a condition / starting position set.

    Parameters
    ----------
    conditions : tuple, optional
        _description_, by default None
    episode : int, optional
        _description_, by default None

    Returns
    -------
    Union[int, int]
        _description_
    """
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


def get_condition_meaning(
    info_dict: Dict, starting_position: int, condition: int
) -> str:
    """
    Construct the meaning of a trial based on condition and starting position.

    Parameters
    ----------
    info_dict : Dict
        A dictionary containing information about conditions and positions. It should have the keys:
        - 'condition': A dictionary mapping condition IDs to their meanings.
        - 'position': A dictionary mapping starting positions to their meanings.
    starting_position : int
        The ID of the starting position.
    condition : int
        The ID of the condition.

    Returns
    -------
    str
        The concatenated meaning of the condition and starting position.

    Notes
    -----
    If either 'condition' or 'position' is missing from `info_dict`, the corresponding part of
    the meaning will not be included in the result.
    """

    trial_type = ""
    if "condition" in info_dict.keys():
        trial_type += info_dict["condition"][condition]

    if "position" in info_dict.keys():
        trial_type += info_dict["position"][starting_position]

    return trial_type


def check_seed(seed: Union[np.random.Generator, int] = 1234) -> np.random.Generator:
    """
    Checks if a provided seed is a np.random.Generator object or an integer.
    If it is an integer, creates a Generator object using the integer as a seed
    , else returns the provided
    Generator.

    Parameters
    ----------
    seed : Union[np.random.Generator, int], optional
        A np.random.Generator or an integer, used to seed the Generator, by default 1234

    Returns
    -------
    np.random.Generator
        A np.random.Generator object.
    """
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
    terminals = get_stripped_graph(graph)
    terminals = terminals.values()

    terminals = list(itertools.chain.from_iterable(terminals))
    nodes = list(graph.keys())
    starting_nodes = list(set(nodes) - set(terminals))

    return starting_nodes


def get_stripped_graph(graph: Dict):
    """
    Processes a graph by stripping and flattening its edges.

    The function takes a graph (a dictionary where keys are nodes and values are edges)
    and processes the edges. If the edge is a tuple, it extracts the first element.
    If the edge is a dictionary, it extracts and flattens the first elements of the
    tuples that are non-string keys. The function returns a new graph with the
    processed edges.

    Parameters
    ----------
    graph : dict
        A dictionary representing the graph. Keys are nodes and values are edges, which
        can be tuples, dictionaries, or other types.

    Returns
    -------
    stripped_graph : dict
        A dictionary representing the processed graph, where the edges have been stripped
        and flattened as described.

    Examples
    --------
    >>> graph = {
    ...     'A': (['B', 'C'],),
    ...     'B': {'1': (['D'],), 2: (['E'],), 3: ['F', 'G']},
    ...     'C': ['H', 'I']
    ... }
    >>> get_stripped_graph(graph)
    {'A': ['B', 'C'], 'B': ['D', 'E', 'F', 'G'], 'C': ['H', 'I']}
    """

    stripped_graph = {}
    for nd, edg in graph.items():
        if isinstance(edg, tuple):
            edges = edg[0]
        elif isinstance(edg, dict):
            edges = [
                edg[k][0] if isinstance(edg[k], tuple) else edg[k]
                for k in edg.keys()
                if not isinstance(k, str)
            ]
            edges = list(itertools.chain.from_iterable(edges))  # flatten list
        else:
            edges = edg

        stripped_graph[nd] = edges

    return stripped_graph


def update_psychopy_trials(settings, env, episode):
    # Update timings
    if settings["update"] is not None and len(settings["update"]) > 0:
        for k in settings["update"]:
            for jj in env.info_dict.keys():
                if "psychopy" in env.info_dict[jj].keys():
                    for ii in env.info_dict[jj]["psychopy"]:
                        if ii.name == k:
                            ii.duration = settings[k][episode]
