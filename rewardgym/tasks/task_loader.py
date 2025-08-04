import importlib
import os
from pathlib import Path

TASKS_DIR = Path(__file__).resolve().parent


def _discover_plugins():
    """Scan tasks/ directory and import plugins that define `register_task()`."""

    task_registry = {}
    for task_folder in os.listdir(TASKS_DIR):
        if not (TASKS_DIR / task_folder).is_dir():
            continue

        if "__" in task_folder:
            continue

        plugin_path = TASKS_DIR / f"{task_folder}/plugin.py"
        try:
            spec = importlib.util.spec_from_file_location(
                name=f"rewardgym.tasks.{task_folder}.plugin", location=plugin_path
            )  # "rewardgym.tasks.{task_folder}")
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            # plugin_module = importlib.import_module(plugin_path)
            if not hasattr(plugin_module, "register_task"):
                raise AttributeError("No register() function defined")
            registry = plugin_module.register_task()
            task_registry.update(registry)

            print(f"Registered: {list(registry.keys())[0]}")
        except (ModuleNotFoundError, AttributeError, Exception) as e:
            #    print(f"[WARN] Could not register task '{task_folder}': {e}")
            # except (AttributeError) as e:
            print(f"[WARN] Could not register task '{task_folder}': {e}")

    return task_registry


def get_task(task_name, *args, **kwargs):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    return _task_registry[task_name]["get_task"](*args, **kwargs)


def get_configs(task_name):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    get_configs_func = _task_registry[task_name]["get_configs"]
    if get_configs_func is None:
        raise NotImplementedError(f"get_configs not implemented for {task_name}")
    return get_configs_func


def get_psychopy_info(task_name, **kwargs):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    get_configs_func = _task_registry[task_name]["get_psychopy_info"]
    if get_configs_func is None:
        raise NotImplementedError(f"get_psychopy_info not implemented for {task_name}")
    return get_configs_func(**kwargs)


def get_pygame_info(task_name, **kwargs):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    get_configs_func = _task_registry[task_name]["get_pygame_info"]
    if get_configs_func is None:
        raise NotImplementedError(f"get_pygame_info not implemented for {task_name}")
    return get_configs_func(**kwargs)
