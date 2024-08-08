from typing import Any, List, Literal, Union

import numpy as np

from ..environments import BaseEnv, PsychopyEnv, RenderEnv

# TODO Maybe enums are the way to go, for now staying with literal.


def get_task(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    render_backend: Literal["pygame"] = None,
    window_size: int = None,
    seed: Union[np.random.Generator, int] = 1000,
):

    if task_name == "hcp":
        from .hcp import get_hcp as get_task_func

    elif task_name == "mid":
        from .mid import get_mid as get_task_func

    elif task_name == "two-step":
        from .two_step import get_two_step as get_task_func

    elif task_name == "risk-sensitive":
        from .risk_sensitive import get_risk_sensitive as get_task_func

    elif task_name == "posner":
        from .posner import get_posner as get_task_func

    elif task_name == "gonogo":
        from .gonogo import get_gonogo as get_task_func

    else:
        raise NotImplementedError(f"Task {task_name} is not implemented.")

    environment_graph, reward_structure, info_dict = get_task_func(
        render_backend=render_backend, window_size=window_size, seed=seed
    )

    return environment_graph, reward_structure, info_dict


def get_env(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    render_mode: Literal["human"] = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
    **kwargs,
):

    environment_graph, reward_structure, info_dict = get_task(
        task_name,
        render_backend=render_backend,
        window_size=window_size,
        seed=seed,
    )

    if (render_mode is None) and (render_backend is None):
        env = BaseEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
            name=task_name,
        )
    elif render_backend == "pygame":
        env = RenderEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_mode,
            info_dict=info_dict,
            window_size=window_size,
            seed=seed,
            name=task_name,
        )
    elif render_backend == "psychopy":
        env = PsychopyEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
            name=task_name,
            n_actions=2 if task_name == "risk-sensitive" else None,
            window=kwargs["window"],
            logger=kwargs["logger"],
        )

    return env


def get_configs(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"]
):

    if task_name == "hcp":
        from .hcp import generate_hcp_configs as generate_configs

    elif task_name == "mid":
        from .mid import generate_mid_configs as generate_configs

    elif task_name == "two-step":
        from .two_step import generate_two_step_configs as generate_configs

    elif task_name == "risk-sensitive":
        from .risk_sensitive import generate_risk_sensitive_configs as generate_configs

    elif task_name == "posner":
        from .posner import generate_posner_configs as generate_configs

    elif task_name == "gonogo":
        from .gonogo import generate_gonogo_configs as generate_configs

    else:
        raise NotImplementedError(f"Task {task_name} is not implemented.")

    return generate_configs


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
