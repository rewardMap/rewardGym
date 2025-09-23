from .task_loader import TaskRegistry, get_configs, get_psychopy_info
from .utils import get_env, get_task

FULLPOINTS = {
    "posner": 152,
    "mid": 48,
    "hcp": 13.5,
    "risk-sensitive": 5150,
    "two-step": 100,
    "gonogo": 43,
}

__all__ = [
    "get_configs",
    "get_env",
    "get_task",
    "FULLPOINTS",
    "get_psychopy_info",
    "TaskRegistry",
]
