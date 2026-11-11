from .render_base import BaseRoutine
from typing import Any
from .stimulus_classes import StimulusDefinition, TextDefinition
from .contexts import StepContext
from .render_helper import log_event, response_handling


class ActionRoutine(BaseRoutine):
    def __init__(
        self,
        name,
        duration: float,
        key_dict: dict,
        rl_label: str | None = None,
        stimulus_definitions: list[StimulusDefinition] | None = None,
        timeout_action: Any | None = None,
        name_timeout: str | None = None,
        flip: bool = False,
        poll_keys=True,
        before_action_callback: None = None,
        after_action_callback: None = None,
        detect_too_early: bool = False,
        too_early_action: Any | None = None,
        too_early_warning: StimulusDefinition | None = None,
    ):
        stimulus_definitions = []

        self.detect_too_early = detect_too_early
        self.too_early_action = too_early_action

        if self.detect_too_early and too_early_warning is None:
            self.too_early_warning = TextDefinition(
                name="response-too-early",
                pos=(0, -150),
                text="Don't press too early!",
                height=28,
                color="white",
            )
        else:
            self.too_early_warning = too_early_warning

        stimulus_definitions.append(self.too_early_warning)

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            flip=flip,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
        )

        self.key_dict = key_dict
        self.key_list = list(key_dict.keys())
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.stimulus_definitions = stimulus_definitions
        self.before_action_callback = before_action_callback
        self.after_action_callback = after_action_callback

        self.returns_action = True

    def display(self, context: StepContext):
        self.draw_list = []

        if self.before_action_callback:
            self.before_action_callback(self, context)

        response_window_onset = context.logger.get_time()

        if self.detect_too_early:
            too_early = self.check_too_early(
                context, response_window_onset=response_window_onset
            )
        else:
            too_early = False

        if self.draw_list is None:
            self.draw_list = self.stimuli.keys()

        for stim_name in self.draw_list:
            if self.stimuli[stim_name].opacity > 0:
                self.stimuli[stim_name].draw()

        if self.flip:
            context.render.flip()

        response = response_handling(
            self, context, response_window_onset=response_window_onset
        )

        if self.detect_too_early and too_early:
            _action, remaining = response
            response = (self.too_early_action, remaining)
            self.stimuli[self.too_early_warning.name].draw()

        if self.after_action_callback:
            self.after_action_callback(self, context)

        self.draw_list = None

        return response

    def check_too_early(self, context, response_window_onset):
        response = context.input_handler.key_strokes(
            logger=context.logger, key_list=self.key_list
        )

        too_early = False

        if response:
            RTE = response[1] - response_window_onset
            log_event(
                self,
                logger=context.logger,
                extra_info={
                    "event_type": self.too_early_warning.name,
                    "response_button": response[0],
                    "response_time": RTE,
                },
                onset=response_window_onset,
            )
            too_early = True

        return too_early
