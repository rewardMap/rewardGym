import warnings
from .backend_base import RewardGymBackend, setup_stimulus
from .be_simulation import SimulationBackend

__all__ = ["RewardGymBackend", "setup_stimulus"]


class BackendRegistry(dict):
    """Backend registry with duplicate handling."""

    def register(self, name, backend, *, overwrite=False):
        if name in self:
            if not overwrite:
                warnings.warn(
                    f"Backend '{name}' already registered, skipping.",
                    UserWarning,
                    stacklevel=2,
                )
                return

            warnings.warn(
                f"Backend '{name}' already registered, overwriting.",
                UserWarning,
                stacklevel=2,
            )

        self[name] = backend


BACKENDS = BackendRegistry()


try:
    from .be_psychopy import PsychoPyBackend

    BACKENDS.register("psychopy", PsychoPyBackend)

except ImportError:
    pass

try:
    from .be_pygame import PygameBackend

    BACKENDS.register("pygame", PygameBackend)

except ImportError:
    pass

try:
    from .be_pygame import PygameBackendHeadless

    BACKENDS.register("pygame-headless", PygameBackendHeadless)

except ImportError:
    pass

BACKENDS.register("simulation", SimulationBackend)
