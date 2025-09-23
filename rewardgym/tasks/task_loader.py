import importlib
import importlib.util
import os
import sys
from pathlib import Path


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
            spec = importlib.util.spec_from_file_location(
                name=f"rewardgym.tasks.{task_folder}.plugin", location=plugin_path
            )
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            if not hasattr(plugin_module, "register_task"):
                raise AttributeError("No register_task() function defined")

            registry = plugin_module.register_task()
            task_registry.update(registry)

            print(f"Registered task: {list(registry.keys())[0]}")
        except Exception as e:
            print(f"[WARN] Could not register task '{task_folder}': {e}")

    return task_registry


def _discover_external_plugins(task_folder):
    """Load a task from an external folder, preserving relative imports."""
    task_registry = {}
    task_folder = Path(task_folder).resolve()
    plugin_path = task_folder / "plugin.py"

    if not plugin_path.exists():
        print(f"[WARN] No plugin.py found in {task_folder}")
        return task_registry

    try:
        # Step 1: Add the task folder's parent to sys.path
        # This allows relative imports (e.g., from .core) to resolve.
        parent_dir = str(task_folder.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

        # Step 2: Create a module spec with a fake package name
        # This tricks Python into treating the folder as a package.
        module_name = f"external_task_{task_folder.name}"
        spec = importlib.util.spec_from_file_location(
            name=module_name,
            location=plugin_path,
        )
        plugin_module = importlib.util.module_from_spec(spec)

        # Step 3: Set __package__ to enable relative imports
        # This is critical for `from .core import ...` to work.
        plugin_module.__package__ = f"{task_folder.name}"

        # Step 4: Execute the module
        spec.loader.exec_module(plugin_module)

        if not hasattr(plugin_module, "register_task"):
            raise AttributeError("No register_task() function defined in plugin.py")

        # Step 5: Register the task
        registry = plugin_module.register_task()
        task_registry.update(registry)
        print(f"Registered external task: {list(registry.keys())[0]}")

    except Exception as e:
        print(f"[WARN] Could not register external task '{task_folder}': {e}")
    finally:
        # Step 6: Clean up sys.path to avoid pollution
        if parent_dir in sys.path:
            sys.path.remove(parent_dir)

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
                    print(f"[WARN] Task '{key}' already registered, overwriting.")
                    self._data[key] = value
                else:
                    print(f"[WARN] Task '{key}' already registered, skipping.")
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
