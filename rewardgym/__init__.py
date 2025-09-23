import pathlib

from . import _version
from .tasks import TaskRegistry, get_configs, get_env, get_psychopy_info, task_loader
from .utils import check_random_state, run_single_episode

TASKS_DIR = pathlib.Path(__file__).resolve().parent

_task_registry = TaskRegistry(task_loader._discover_plugins(TASKS_DIR / "tasks"))

ASSETS_PATH = pathlib.Path(__file__).parent.resolve() / "assets"

ENVIRONMENTS = list(_task_registry.keys())

__all__ = [
    "get_configs",
    "get_env",
    "run_single_episode",
    "ENVIRONMENTS",
    "get_psychopy_info",
    "check_random_state",
]

__version__ = _version.get_versions()["version"]


def extend_task_registry(extra_dirs, overwrite=True):
    global _task_registry
    for d in extra_dirs:
        extra = task_loader._discover_external_plugins(d)
        _task_registry.extend(extra, overwrite=overwrite)
    return _task_registry
