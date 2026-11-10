from .backend_factories import setup_stimulus
from .render_base import BaseRoutine, EnvironmentContext, StepContext
from .render_helper import log_event
from .stimulus_classes import (
    StimulusDefinition,
    TextDefinition,
    RectangleDefinition,
    ImageDefinition,
)
from .routine_helpers import (
    conditioned_text,
    state_selection_with_highlight,
    reward_update_routine,
    autodraw_false,
)
from typing import TypedDict

import warnings

from ..stimuli import (
    lose_cross,
    win_cross,
    zero_cross,
)


class FeedbackStimuli(TypedDict, total=False):
    win: StimulusDefinition
    lose: StimulusDefinition
    zero: StimulusDefinition


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

        extra_info = self.get_log_info(context=context)
        log_event(self, logger=context.logger, onset=stim_onset, extra_info=extra_info)


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
        callback_after_draw=None,
    ):
        super().__init__(
            name=name, duration=duration, rl_label=rl_label, poll_keys=poll_keys
        )

        if isinstance(stimulus_definitions, StimulusDefinition):
            stimulus_definitions = [stimulus_definitions]

        self.stimulus_definitions = stimulus_definitions
        self.flip = flip
        self.callback_before_draw = callback_before_draw
        self.callback_after_draw = callback_after_draw

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

        if self.callback_after_draw:
            self.callback_after_draw(self, context)

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


class StateBasedDisplay(DynamicRoutine):
    def __init__(
        self,
        duration: float | None,
        state_definition_map: dict,
        border_definition: RectangleDefinition | bool | None = True,
        stimulus_shift: tuple = (350, 0),
        rl_label: str | None = None,
        name: str | None = None,
        poll_keys=True,
        flip: bool = True,
        selection: bool = False,
    ):
        if border_definition is None or border_definition is True:
            self.border_definition = RectangleDefinition(
                name="border",
                lineColor="white",
                lineWidth=7,
                height=0,
                width=0,
            )
        else:
            self.border_definition = None

        self.state_definition_map = state_definition_map
        self.stimulus_shift = stimulus_shift

        stimulus_definitions = [i for i in self.state_definition_map.values()]
        self.selection = selection
        self.border_name = None

        if self.border_definition is not None:
            stimulus_definitions.append(self.border_definition)
            self.border_name = self.border_definition.name

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
            callback_before_draw=state_selection_with_highlight,
        )


class FeedBackRoutine(DynamicRoutine):
    """
    Class that possibly will be superseded or become obsolete at some point.

    Purpose of the class is to provide feedback to the participant, about the
    number of points they have received in a given trial or across the experiment.
    """

    def __init__(
        self,
        duration: float,
        reward_text: TextDefinition | None = None,
        reward_text_template: str | None = None,
        show_bar: bool = True,
        show_total_reward: bool = True,
        total_reward_text: TextDefinition | None = None,
        total_reward_text_template: str | None = None,
        reward_bar: RectangleDefinition | None = None,
        reward_bar_indicator: RectangleDefinition | None = None,
        show_reward_bar_labels: bool = True,
        reward_bar_labels: tuple[str, str] | list[TextDefinition] | None = None,
        show_feedbackstim: bool = True,
        feedback_stim: FeedbackStimuli | None = None,
        position: tuple[int, int] = (0, 125),
        name: str | None = None,
        bar_total: float | None = None,
        rl_label: str | None = None,
        poll_keys=True,
    ):
        """
        FeedBack class, provides feedback to the participant, by creating
        updatable TextStims.

        Parameters
        ----------
        duration : float
            Duration of the feedback.
        text : str
            The text that should be displayed on the screen. Should be a format string!
        position : Tuple[int, int], optional
            Where to display the text (by default in px), by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        target : Literal[&quot;reward&quot;, &quot;total_reward&quot;], optional
            If the trial's reward or the total reward should be shown, by default "reward"
        text_color : str, optional
            Color of the text, by default "white"
        feedback_stim : Dict, optional
            If the feedback_stim should be displayed, if True changes fixation cross,
            if None does not show an image as feedback. For other images populate the
            keys: win, lose, zero with a string to an image or a numpy array.
        """

        if reward_text_template is None:
            self.reward_text_template = "{reward}"

        if total_reward_text_template is None:
            self.total_reward_text_template = "Total: {reward}"

        self.component_names = {
            "reward": None,
            "bar": None,
            "indicator": None,
            "bar_labels": None,
            "stim_win": None,
            "stim_lose": None,
            "stim_zero": None,
            "reward_total": None,
        }

        stimulus_definitions = []

        if show_bar and bar_total is None:
            warnings.warn(
                "Cannot display reward bar if no maximum is set - reward bar is set to False"
            )
            show_bar = False

        if show_total_reward and show_bar:
            show_bar = True
            show_total_reward = False
            warnings.warn("Not showing total reward, if bar is set.")

        def add_component(key, definiton):
            self.component_names[key] = definiton.name
            stimulus_definitions.append(definiton)

        if reward_text is None:
            reward_text = TextDefinition(
                name="reward",
                text="",
                opacity=0.0,
                pos=(0, 125),
                color="white",
                height=50,
                font="arial",
                alignText="center",
                anchorHoriz="center",
            )
        add_component("reward", reward_text)

        if show_total_reward:
            if total_reward_text is None:
                total_reward_text = TextDefinition(
                    name="total-reward",
                    opacity=0.0,
                    text="",
                    pos=(0, 250),
                    color="white",
                    height=20,
                    font="arial",
                    alignText="center",
                    anchorHoriz="center",
                )

            add_component("reward_total", total_reward_text)

        if show_bar:
            if reward_bar is None:
                reward_bar = RectangleDefinition(
                    name="rewardbar",
                    width=400,
                    height=50,
                    lineColor="white",
                    fillColor=[0.25, 0.25, 0.75],
                    lineWidth=5,
                    pos=(0, 350),
                    units="pix",
                    autoDraw=True,
                )

            if reward_bar_indicator is None:
                reward_bar_indicator = RectangleDefinition(
                    name="reward-indicator",
                    width=10,
                    height=reward_bar.height + 10,
                    lineColor=None,
                    fillColor="white",
                    lineWidth=0,
                    pos=(-reward_bar.width // 2, 350),
                    autoDraw=True,
                )
            add_component("bar", reward_bar)
            add_component("indicator", reward_bar_indicator)

        if show_bar and show_reward_bar_labels:
            self.component_names["bar_labels"] = []
            label_list = None
            if reward_bar_labels is None:
                label_list = ("0 kr", "75 kr")
            elif isinstance(reward_bar_labels, tuple):
                label_list = reward_bar_labels

            if label_list is not None:
                reward_bar_labels = []
                for ll, pos in zip(
                    label_list,
                    [
                        (-reward_bar.width // 2 - 40, 350),
                        (reward_bar.width // 2 + 40, 350),
                    ],
                ):
                    stimulus_definitions.append(
                        TextDefinition(
                            name=f"label-{ll}",
                            color="white",
                            height="25",
                            pos=pos,
                            text=ll,
                            autoDraw=True,
                        )
                    )
                    self.component_names["bar_labels"].append(
                        stimulus_definitions[-1].name
                    )

            else:
                for bl in reward_bar_labels:
                    self.component_names["bar_labels"].append(bl.name)
                    stimulus_definitions.append(bl)

        if show_feedbackstim:
            if feedback_stim is None:
                feedback_stim = {}
                for fs_nam, stim in zip(
                    ["win", "lose", "zero"], [win_cross(), lose_cross(), zero_cross()]
                ):
                    feedback_stim[name] = ImageDefinition(
                        name="feedback-" + fs_nam,
                        image=stim,
                        pos=(0, 0),
                        opacity=0.0,
                    )

            for fs_k, fs_def in feedback_stim.items():
                add_component("stim_" + fs_k, fs_def)

        self.bar_total = bar_total
        self.tear_down_stimuli = [
            self.component_names[i]
            for i in ["stim_win", "stim_lose", "stim_zero", "reward", "reward_total"]
        ]

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
            callback_before_draw=reward_update_routine,
            callback_after_draw=autodraw_false,
        )

    def get_log_info(self, context: StepContext):
        return {"reward": context.reward, "total_reward": context.total_reward}
