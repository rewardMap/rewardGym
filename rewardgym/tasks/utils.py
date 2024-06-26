from typing import Literal, Union

import numpy as np

from ..environments import BaseEnv, MultiChoiceEnv, RenderEnv, RenderEnvMultiChoice

# TODO Maybe enums are the way to go, for now staying with literal.


def get_task(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    conditions: Union[list, np.ndarray] = None,
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

    environment_graph, reward_structure, condition_out, info_dict = get_task_func(
        conditions, render_backend=render_backend, window_size=window_size, seed=seed
    )

    return environment_graph, reward_structure, condition_out, info_dict


def get_env(
    task_name: Literal["hcp", "mid", "two-step", "risk-sensitive", "posner", "gonogo"],
    conditions: Union[list, np.ndarray] = None,
    render_mode: Literal["human"] = None,
    render_backend: Literal["pygame", "psychopy"] = None,
    window_size: int = None,
    seed: Union[int, np.random.Generator] = 1000,
):

    environment_graph, reward_structure, condition_out, info_dict = get_task(
        task_name,
        conditions,
        render_backend=render_backend,
        window_size=window_size,
        seed=seed,
    )

    if (render_mode is None) and (render_backend is None):

        if task_name == "risk-sensitive":
            env = MultiChoiceEnv(
                environment_graph=environment_graph,
                condition_dict=condition_out[1],
                reward_locations=reward_structure,
                render_mode=render_mode,
                info_dict=info_dict,
                seed=seed,
            )
            condition_out = condition_out[0]
        else:
            env = BaseEnv(
                environment_graph=environment_graph,
                reward_locations=reward_structure,
                render_mode=render_mode,
                info_dict=info_dict,
                seed=seed,
            )
    else:
        if task_name == "risk-sensitive":
            env = RenderEnvMultiChoice(
                environment_graph=environment_graph,
                condition_dict=condition_out[1],
                reward_locations=reward_structure,
                render_mode=render_mode,
                info_dict=info_dict,
                window_size=window_size,
                seed=seed,
            )
            condition_out = condition_out[0]
        else:
            env = RenderEnv(
                environment_graph=environment_graph,
                reward_locations=reward_structure,
                render_mode=render_mode,
                info_dict=info_dict,
                window_size=window_size,
                seed=seed,
            )

    return env, condition_out


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
        from .risk_sensitive import generate_risk_senistive_configs as generate_configs

    elif task_name == "posner":
        from .posner import generate_posner_configs as generate_configs

    elif task_name == "gonogo":
        from .gonogo import generate_gonogo_configs as generate_configs

    else:
        raise NotImplementedError(f"Task {task_name} is not implemented.")

    return generate_configs()
