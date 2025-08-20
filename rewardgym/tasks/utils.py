from typing import Any, List, Literal, Tuple, Union

import numpy as np

from ..environments import BaseEnv, PsychopyEnv, RenderEnv
from .task_loader import get_task


def get_env(
    task_name: Literal[
        "hcp",
        "mid",
        "two-step",
        "risk-sensitive",
        "posner",
        "gonogo",
    ],
    render_backend: Literal["pygame", "psychopy", "psychopy-simulate"] = None,
    random_state: Union[int, np.random.Generator] = 1000,
    **kwargs,
):
    environment_graph, reward_structure, info_dict = get_task(
        task_name,
        render_backend=render_backend,
        random_state=random_state,
    )

    if "meta" in info_dict.keys():
        if "reduced_actions" in info_dict["meta"].keys():
            reduced_actions = info_dict["meta"]["reduced_actions"]

    if render_backend is None:
        env = BaseEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_backend,
            info_dict=info_dict,
            random_state=random_state,
            name=task_name,
            reduced_actions=reduced_actions,
        )
    elif render_backend == "pygame":
        env = RenderEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            info_dict=info_dict,
            random_state=random_state,
            name=task_name,
        )
    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        env = PsychopyEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_backend,
            info_dict=info_dict,
            random_state=random_state,
            name=task_name,
            reduced_actions=reduced_actions,
        )

    return env


def check_conditions_not_following(
    condition_list: List[Any], not_following: List[Any], window_length: int = 1
) -> bool:
    """
    Checks if any elements in the condition_list are followed by elements from the not_following list within a specified window length.

    Parameters
    ----------
    condition_list : List[Any]
        The list of conditions to check.
    not_following : List[Any]
        The list of elements that should not follow the elements in condition_list.
    window_length : int, optional
        The length of the window to check after each element in condition_list, by default 1.

    Returns
    -------
    bool
        Returns True if no elements from not_following appear within the window length after any element in condition_list, False otherwise.
    """
    for n, _ in enumerate(condition_list):
        if condition_list[n] in not_following:
            # Loop over conditions following the window. N + 1 as to make the window_lengths more intuitive.
            if any(
                k in not_following
                for k in condition_list[n + 1 : n + 1 + window_length]
            ):
                return False

    return True


def check_conditions_not_following_substring(
    condition_list: List[str], not_following: List[str], window_length: int = 1
) -> bool:
    """
    Checks if any substrings in the condition_list are followed by elements containing substrings from
    the not_following list within a specified window length.

    Parameters
    ----------
    condition_list : List[str]
        The list of strings to check.
    not_following : List[str]
        The list of substrings that should not follow any string in condition_list.
    window_length : int, optional
        The length of the window to check after each element in condition_list, by default 1.

    Returns
    -------
    bool
        Returns True if no strings containing substrings from not_following appear within the window length
        after any element in condition_list, False otherwise.
    """
    for n in range(len(condition_list)):
        # Check if the current element contains any substring from not_following
        if any(substring in condition_list[n] for substring in not_following):
            # Check the elements within the window for the presence of not_following substrings
            if any(
                any(substring in condition_list[k] for substring in not_following)
                for k in range(n + 1, min(n + 1 + window_length, len(condition_list)))
            ):
                return False
    return True


def check_conditions_present(
    condition_list: List[Any], conditions_required: List[Any]
) -> bool:
    """
    Checks if all elements in the conditions_required list are present in the condition_list.

    Parameters
    ----------
    condition_list : List[Any]
        The list of conditions to check.
    conditions_required : List[Any]
        The list of elements that must be present in the condition_list.

    Returns
    -------
    bool
        Returns True if all elements from conditions_required are present in the condition_list, False otherwise.
    """
    test_set = set(condition_list)
    required_set = set(conditions_required)

    return required_set.issubset(test_set)


def check_condition_present_or(
    condition_list: List[Any], condition_required: Tuple[List]
) -> bool:
    """
    Checks if any of the specified conditions are present in the condition list.

    Parameters
    ----------
    condition_list : List[Any]
        The list of conditions to check against.
    condition_required : Tuple[List]
        A tuple of lists, where each list represents a condition to be checked.
        The function will return `True` if at least one of the conditions in
        the tuple is present in the `condition_list`.

    Returns
    -------
    bool
        Returns `True` if at least one of the conditions in `condition_required`
        is present in `condition_list`, otherwise `False`.

    Examples
    --------
    >>> condition_list = ['none_risky-40', 'save-20_none']
    >>> condition_required = (['risky-40_none'], ['none_risky-40'])
    >>> check_condition_present_or(condition_list, condition_required)
    True

    >>> condition_list = ['save-20_none', 'save-40_none']
    >>> condition_required = (['risky-40_none'], ['none_risky-40'])
    >>> check_condition_present_or(condition_list, condition_required)
    False
    """
    return any(
        [check_conditions_present(condition_list, cr) for cr in condition_required]
    )
