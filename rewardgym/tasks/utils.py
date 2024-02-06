from typing import Literal, Union

import numpy as np

from ..environments import BaseEnv, RenderEnv

# TODO Maybe enums are the way to go, for now staying with literal.


def get_task(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    conditions: Union[list, np.ndarray] = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
):

    if task_name == "hcp":
        from .hcp import get_hcp

        environment_graph, reward_structure, condition_out, info_dict = get_hcp(
            conditions=conditions,
            render_backend=render_backend,
            window_size=window_size,
        )

    elif task_name == "mid":
        from .mid import get_mid

        environment_graph, reward_structure, condition_out, info_dict = get_mid(
            conditions=conditions,
            render_backend=render_backend,
            window_size=window_size,
        )

    elif task_name == "two-step":
        pass
    elif task_name == "risk-sensitive":
        pass
    elif task_name == "posner":
        pass
    elif task_name == "gonogo":
        pass
    else:
        raise NotImplementedError(f"Task {task_name} is not implemented.")

    return environment_graph, reward_structure, condition_out, info_dict


def get_env(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    conditions: Union[list, np.ndarray] = None,
    render_mode: Literal["human"] = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
):

    environment_graph, reward_structure, condition_out, info_dict = get_task(
        task_name, conditions, render_backend=render_backend, window_size=window_size
    )

    if (render_mode is None) and (render_backend is None):

        env = BaseEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_mode,
            info_dict=info_dict,
        )
    else:
        env = RenderEnv(
            environment_graph=environment_graph,
            reward_locations=reward_structure,
            render_mode=render_mode,
            info_dict=info_dict,
            window_size=window_size,
        )

    return env, condition_out