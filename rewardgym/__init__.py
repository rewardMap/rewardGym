import pathlib

from . import _version
from .tasks import TaskRegistry, get_configs, get_env, get_render_info, task_loader
from .utils import check_random_state, run_single_episode
from .render import stimuli
from . import agents, data_tools, environments, runner, tasks, render

ENVIRONMENTS = []
__all__ = [
    "ENVIRONMENTS",
    "check_random_state",
    "environments",
    "get_configs",
    "get_env",
    "get_render_info",
    "run_single_episode",
    "runner",
    "stimuli",
    "render",
    "tasks",
    "agents",
    "data_tools",
]

TASKS_DIR = pathlib.Path(__file__).resolve().parent

_task_registry = TaskRegistry(task_loader._discover_plugins(TASKS_DIR / "tasks"))


ASSETS_PATH = pathlib.Path(__file__).parent.resolve() / "assets"

ENVIRONMENTS = list(_task_registry.keys())


__version__ = _version.get_versions()["version"]


def extend_task_registry(extra_dirs, overwrite=True):
    for d in extra_dirs:
        extra = task_loader._discover_external_plugins(d)
        _task_registry.extend(extra, overwrite=overwrite)
    return _task_registry
