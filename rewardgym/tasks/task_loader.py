from __future__ import annotations

import importlib
import importlib.util
import os
import sys
import types
import warnings
from pathlib import Path


def load_task_plugin(folder_path: Path, namespace_root: str = "rewardgym_tasks"):
    """
    Load <folder_path>/plugin.py as a submodule of a shim package
    'namespace_root.<task_name>' whose __path__ points at folder_path.
    Returns the loaded plugin module.
    """
    task_name = folder_path.name
    pkg_name = f"{namespace_root}.{task_name}"

    if namespace_root not in sys.modules:
        root = types.ModuleType(namespace_root)
        root.__package__ = namespace_root
        root.__path__ = []
        root.__spec__ = importlib.machinery.ModuleSpec(
            namespace_root, loader=None, is_package=True
        )
        sys.modules[namespace_root] = root

    # 1) Ensure a shim package exists in sys.modules
    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__package__ = pkg_name
        pkg.__path__ = [str(folder_path)]
        pkg.__spec__ = importlib.machinery.ModuleSpec(
            pkg_name, loader=None, is_package=True
        )
        pkg.__spec__.submodule_search_locations = [str(folder_path)]
        sys.modules[pkg_name] = pkg

    plugin_path = folder_path / "plugin.py"
    mod_name = f"{pkg_name}.plugin"

    spec = importlib.util.spec_from_file_location(
        mod_name,
        plugin_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load plugin from {plugin_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(mod_name, None)
        raise

    return module


def _discover_plugins(base_dir):
    """
    Discover plugins in the given directory.
    Returns a dict {task_name: task_class}.
    """
    task_registry = {}
    base_dir = Path(base_dir)

    if not base_dir.exists():
        return task_registry

    for task_folder in os.listdir(base_dir):
        folder_path = base_dir / task_folder
        if not folder_path.is_dir():
            continue

        if task_folder == "task_template" or "__" in task_folder:
            continue

        plugin_path = folder_path / "plugin.py"
        if not plugin_path.exists():
            continue

        try:
            plugin_module = load_task_plugin(
                folder_path, namespace_root="rewardgym_tasks"
            )

            if not hasattr(plugin_module, "register_task"):
                raise AttributeError("No register_task() function defined")

            registry = plugin_module.register_task()
            task_registry.update(registry)

            print(f"Registered task: {next(iter(registry.keys()))}")
        except Exception as e:
            warnings.warn(
                f"Could not register task '{task_folder}': {e}",
                UserWarning,
                stacklevel=2,
            )

    return task_registry


def _discover_external_plugins(task_folder: str | Path) -> dict:
    """
    Discover and register tasks from external directories.
    Args:
        task_folder: Path to a task folder containing plugin.py.
    Returns:
        Dictionary of registered tasks {task_name: task_handles}.
    """
    task_registry = {}
    task_folder = Path(task_folder).resolve()
    plugin_path = task_folder / "plugin.py"

    if not plugin_path.exists():
        warnings.warn(f"No plugin.py found in {task_folder}", UserWarning, stacklevel=2)

        return task_registry

    try:
        plugin_module = load_task_plugin(task_folder, namespace_root="rewardgym_tasks")
        plugin_module.__package__ = task_folder.name

        if not hasattr(plugin_module, "register_task"):
            raise AttributeError(f"No register_task() function in {plugin_path}")

        for task_name, handles in plugin_module.register_task().items():
            task_registry[task_name] = handles
            print(f"Registered external task: {task_name}")

    except Exception as e:
        warnings.warn(
            f"Could not register external task '{task_folder}': {e}",
            UserWarning,
            stacklevel=2,
        )

        import traceback

        traceback.print_exc()  # Print full traceback for debugging

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


def get_render_info(task_name, **kwargs):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    get_configs_func = _task_registry[task_name]["get_render_info"]
    if get_configs_func is None:
        raise NotImplementedError(f"get_render_info not implemented for {task_name}")
    return get_configs_func(**kwargs)


def get_instructions_psychopy(task_name, **kwargs):
    from .. import _task_registry

    if task_name not in _task_registry:
        raise ValueError(f"Task '{task_name}' not registered.")
    get_configs_func = _task_registry[task_name]["instructions_psychopy"]
    if get_configs_func is None:
        raise NotImplementedError(
            f"instructions_psychopy not implemented for {task_name}"
        )
    return get_configs_func(**kwargs)


class TaskRegistry:
    """A composition-based task registry with conflict resolution."""

    def __init__(self, initial_data=None):
        self._data = {} if initial_data is None else dict(initial_data)

    def extend(self, other_dict, overwrite=True):
        """Extend the registry with another dictionary."""
        for key, value in other_dict.items():
            if key in self._data:
                if overwrite:
                    warnings.warn(
                        f"Task '{key}' already registered, overwriting.",
                        UserWarning,
                        stacklevel=2,
                    )
                    self._data[key] = value
                else:
                    warnings.warn(
                        f"Task '{key}' already registered, skipping.",
                        UserWarning,
                        stacklevel=2,
                    )
            else:
                self._data[key] = value

    # Delegate dictionary methods to self._data
    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def get(self, key, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)
