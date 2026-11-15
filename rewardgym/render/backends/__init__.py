from .backend_base import setup_stimulus, RewardGymBackend

__all__ = ["setup_stimulus", "RewardGymBackend"]


def get_backends():
    registry = {}

    try:
        from .be_psychopy import PsychoPyBackend

        registry["psychopy"] = PsychoPyBackend

    except ImportError:
        pass

    try:
        from .be_pygame import PygameBackend

        registry["pygame"] = PygameBackend

    except ImportError:
        pass

    from .be_simulation import SimulationBackend

    registry["simulation"] = SimulationBackend

    return registry
