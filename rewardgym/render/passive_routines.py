from .backend_factories import setup_stimulus
from .render_base import BaseRoutine, EnvironmentContext, StepContext
from .render_helper import log_event
from .stimulus_classes import StimulusDefinition


class PresentationRoutine(BaseRoutine):
    def __init__(
        self,
        duration: float,
        rl_label: str | None = None,
        stimulus_definitions: StimulusDefinition
        | list[StimulusDefinition]
        | None = None,
        name: str | None = None,
        poll_keys=True,
    ):
        super().__init__(
            name=name, duration=duration, rl_label=rl_label, poll_keys=poll_keys
        )

        if isinstance(stimulus_definitions, StimulusDefinition):
            stimulus_definitions = [stimulus_definitions]

        self.stimulus_definitions = stimulus_definitions

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

        for stim in self.stimulus_definitions:
            self.stimuli[stim.name] = setup_stimulus(
                window=context.win, factory=context.stimuli, definition=stim
            )

    def display(self, context: StepContext) -> None:
        """
        Calls the stimulus object. In this case drawing the text stim, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
            The logger associated with the experiment.

        Returns
        -------
        None
        Should return None

        """

        stim_onset = context.logger.get_time()
        for stim in self.stimuli:
            stim.draw()

        context.render.flip()

        context.render.wait(
            logger=context.logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=context.logger, onset=stim_onset)
