import pathlib

from . import _version
from .tasks import get_configs, get_env, get_psychopy_info, task_loader
from .utils import check_seed, run_single_episode

_task_registry = task_loader._discover_plugins()

ASSETS_PATH = pathlib.Path(__file__).parent.resolve() / "assets"

ENVIRONMENTS = list(_task_registry.keys())

__all__ = [
    "get_configs",
    "get_env",
    "run_single_episode",
    "ENVIRONMENTS",
    "get_psychopy_info",
    "check_seed",
]

__version__ = _version.get_versions()["version"]
