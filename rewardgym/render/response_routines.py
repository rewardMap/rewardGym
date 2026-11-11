from .render_base import BaseRoutine
from typing import Any
from .stimulus_classes import StimulusDefinition
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
        flip: bool = True,
        poll_keys=True,
        before_action_callback: None = None,
        after_action_callback: None = None,
        too_early_callback: None = None,
    ):
        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            flip=flip,
            poll_keys=poll_keys,
        )

        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.returns_action = True
        self.stimulus_definitions = stimulus_definitions
        self.before_action_callback = before_action_callback
        self.after_action_callback = after_action_callback
        self.too_early_callback = too_early_callback

    def display(self, context: StepContext):
        if self.before_action_callback:
            self.before_action_callback(self, context)

        if not self.too_early_callback:
            context.input_handler.key_strokes(logger=context.logger)
        else:
            self.too_early_callback(self, context)

        response_window_onset = context.logger.get_time()

        for stim in self.stimuli.values():
            stim.draw()

        if self.flip:
            context.render.flip()

        response = response_handling(
            self, context, response_window_onset=response_window_onset
        )

        extra_info = self.get_log_info(context=context)
        log_event(
            self,
            logger=context.logger,
            onset=response_window_onset,
            extra_info=extra_info,
        )

        if self.after_action_callback:
            self.before_action_callback(self, context)

        return response
