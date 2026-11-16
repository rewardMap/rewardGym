from .backend_base import RewardGymBackend, setup_stimulus

__all__ = ["RewardGymBackend", "setup_stimulus"]


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

    try:
        from .be_pygame import PygameBackendHeadless

        registry["pygame-headless"] = PygameBackendHeadless

    except ImportError:
        pass

    from .be_simulation import SimulationBackend

    registry["simulation"] = SimulationBackend

    return registry
