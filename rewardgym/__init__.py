from . import _version
from .tasks import get_configs, get_env, get_psychopy_info, task_loader
from .utils import run_single_episode

_task_registry = task_loader._discover_plugins()


ENVIRONMENTS = [
    "hcp",
    "mid",
    "two-step",
    "risk-sensitive",
    "posner",
    "gonogo",
]

__all__ = [
    "get_configs",
    "get_env",
    "run_single_episode",
    "ENVIRONMENTS",
    "get_psychopy_info",
]

__version__ = _version.get_versions()["version"]
