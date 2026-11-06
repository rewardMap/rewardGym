from abc import ABC, abstractmethod

from .contexts import EnvironmentContext, StepContext


class PresentationRoutine(ABC):
    """Base class for all stimuli with context-aware presentation"""

    def __init__(
        self,
        name: str | None = None,
        duration: float | None = None,
        rl_label: str | None = None,
        noflip=False,
    ):
        self.name = name
        self.duration = duration
        self.rl_label = rl_label
        self.is_setup = False
        self.noflip = noflip
        self.returns_action = False

    def present(self, context: StepContext):
        """Public method that handles context-aware presentation"""
        return self.display(context)

    def setup(self, context: EnvironmentContext, **kwargs):
        """Setup the stimulus with required resources"""
        self._setup(context, **kwargs)
        self.is_setup = True

    @abstractmethod
    def _setup(self, context: EnvironmentContext, **kwargs):
        """Internal setup implementation"""

    @abstractmethod
    def display(self, context: StepContext):
        """Actual display implementation"""


class ActionRoutine(PresentationRoutine):
    def __init__(
        self, name, duration, key_dict, rl_label, timeout_action, name_timeout, noflip
    ):
        super().__init__(name=name, duration=duration, rl_label=rl_label, noflip=noflip)

        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.returns_action = True
