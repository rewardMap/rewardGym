from .utils import get_configs, get_env, get_task

FULLPOINTS = {
    "posner": 152,
    "mid": 48,
    "hcp": 13.5,
    "risk-sensitive": 5150,
    "two-step": 100,
    "gonogo": 50,
}

__all__ = ["get_configs", "get_env", "get_task", "FULLPOINTS"]
