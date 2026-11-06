from abc import ABC, abstractmethod

from .contexts import StepContext


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
        if "simulate" in context.env_context.mode:
            return self.simulate(context)
        return self.display(context)

    def setup(self, win, **kwargs):
        """Setup the stimulus with required resources"""
        self._setup(win, **kwargs)
        self.is_setup = True

    @abstractmethod
    def _setup(self, win, **kwargs):
        """Internal setup implementation"""

    @abstractmethod
    def display(self, context: StepContext):
        """Actual display implementation"""

    @abstractmethod
    def simulate(self, context: StepContext):
        """Simulation implementation"""

    def _log_event(self, logger, stim_onset=None, extra_info=None):
        """Common logging functionality"""
        base_dict = {
            "event_type": self.name,
            "expected_duration": self.duration,
            "rl_label": self.rl_label,
        }

        if extra_info:
            base_dict.update(extra_info)

        logger.log_event(base_dict, onset=stim_onset)


class ActionRoutine(PresentationRoutine):
    def __init__(
        self, name, duration, key_dict, rl_label, timeout_action, name_timeout, noflip
    ):
        super().__init__(name=name, duration=duration, rl_label=rl_label, noflip=noflip)

        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.returns_action = True
