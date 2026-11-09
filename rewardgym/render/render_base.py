from abc import ABC, abstractmethod

from .contexts import EnvironmentContext, StepContext


class BaseRoutine(ABC):
    """Base class for all stimuli with context-aware presentation"""

    def __init__(
        self,
        name: str | None = None,
        duration: float | None = None,
        rl_label: str | None = None,
        noflip=False,
        poll_keys=True,
    ):
        self.name = name
        self.duration = duration
        self.rl_label = rl_label
        self.is_setup = False
        self.noflip = noflip
        self.returns_action = False
        self.poll_keys = poll_keys

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


class ActionRoutine(BaseRoutine):
    def __init__(
        self,
        name,
        duration,
        key_dict,
        rl_label,
        timeout_action,
        name_timeout,
        noflip,
        poll_keys=True,
    ):
        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            noflip=noflip,
            poll_keys=poll_keys,
        )

        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.returns_action = True
