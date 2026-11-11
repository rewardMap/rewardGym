from abc import ABC, abstractmethod

from .contexts import EnvironmentContext, StepContext
from .backend_factories import setup_stimulus
from .stimulus_classes import StimulusDefinition


class BaseRoutine(ABC):
    """Base class for all stimuli with context-aware presentation"""

    def __init__(
        self,
        name: str | None = None,
        duration: float | None = None,
        rl_label: str | None = None,
        flip=True,
        poll_keys=True,
        stimulus_definitions: list[StimulusDefinition] | None = None,
    ):
        self.name = name
        self.duration = duration
        self.rl_label = rl_label
        self.is_setup = False
        self.flip = flip
        self.returns_action = False
        self.poll_keys = poll_keys
        self.draw_list = None

    def present(self, context: StepContext):
        """Public method that handles context-aware presentation"""
        return self.display(context)

    def setup(self, context: EnvironmentContext, **kwargs):
        """Setup the stimulus with required resources"""
        self._setup(context, **kwargs)
        self.is_setup = True

    def _setup(self, context: EnvironmentContext, **kwargs):
        """
        Performs the setup for the stimulus object. Initiating a PsychoPy.TextStim,
        object, using the parameters given parameters.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """
        self.stimuli = {}

        if self.stimulus_definitions is not None:
            for stim in self.stimulus_definitions:
                self.stimuli[stim.name] = setup_stimulus(
                    window=context.win, factory=context.stimuli, definition=stim
                )

    @abstractmethod
    def display(self, context: StepContext):
        """Actual display implementation"""

    def get_log_info(
        self,
        context: StepContext,
    ) -> dict:
        return {}
