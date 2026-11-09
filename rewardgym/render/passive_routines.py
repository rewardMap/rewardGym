from .backend_factories import setup_stimulus
from .render_base import BaseRoutine, EnvironmentContext, StepContext
from .render_helper import log_event
from .stimulus_classes import StimulusDefinition, TextDefinition, RectangleDefinition
from .routine_helpers import conditioned_text


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
        flip: bool = True,
    ):
        super().__init__(
            name=name, duration=duration, rl_label=rl_label, poll_keys=poll_keys
        )

        if isinstance(stimulus_definitions, StimulusDefinition):
            stimulus_definitions = [stimulus_definitions]

        self.stimulus_definitions = stimulus_definitions
        self.flip = flip

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
        for stim in self.stimuli.values():
            stim.draw()

        if self.flip:
            context.render.flip()

        context.render.wait(
            logger=context.logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=context.logger, onset=stim_onset)


class DynamicRoutine(BaseRoutine):
    def __init__(
        self,
        duration: float,
        rl_label: str | None = None,
        stimulus_definitions: StimulusDefinition
        | list[StimulusDefinition]
        | None = None,
        name: str | None = None,
        poll_keys=True,
        flip: bool = True,
        callback_before_draw=None,
    ):
        super().__init__(
            name=name, duration=duration, rl_label=rl_label, poll_keys=poll_keys
        )

        if isinstance(stimulus_definitions, StimulusDefinition):
            stimulus_definitions = [stimulus_definitions]

        self.stimulus_definitions = stimulus_definitions
        self.flip = flip
        self.callback_before_draw = callback_before_draw

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

        if self.callback_before_draw:
            self.callback_before_draw(self, context)

        stim_onset = context.logger.get_time()
        for stim in self.stimuli.values():
            stim.draw()

        if self.flip:
            context.render.flip()

        context.render.wait(
            logger=context.logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=context.logger, onset=stim_onset)


class ConditionedTextCard(DynamicRoutine):
    def __init__(
        self,
        text_definition: TextDefinition,
        condition_text: dict,
        duration: float | None,
        background_definition: RectangleDefinition | None = None,
        rl_label: str | None = None,
        name: str | None = None,
        poll_keys=True,
        flip: bool = True,
        update_target: str = "reward",
    ):
        self.text_name = text_definition.name
        self.update_target = update_target
        self.condition_text = condition_text
        stimulus_definitions = []

        if background_definition:
            stimulus_definitions.append(background_definition)

        stimulus_definitions.append(text_definition)
        self.update_target = update_target

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
            callback_before_draw=conditioned_text,
        )
