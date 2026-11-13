from typing import Any, TypedDict

from .contexts import StepContext
from .render_base import BaseRoutine
from .render_helper import log_event, response_handling
from .routine_helpers import (
    draw_subset_after,
    draw_subset_before,
    nfc_selection,
    nfc_setup,
)
from .stimulus_classes import RectangleDefinition, StimulusDefinition, TextDefinition


class PresentationSettings(TypedDict, total=False):
    duration_after: float | None
    rl_label_before: str | None
    rl_label_after: str | None
    name_before: str | None
    name_after: str | None
    present_after: bool = False


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
        presentation_settings: PresentationSettings | None = None,
        before_action_callback: None = None,
        after_action_callback: None = None,
        detect_too_early: bool = False,
        too_early_action: Any | None = None,
        too_early_warning: StimulusDefinition | None = None,
    ):
        if stimulus_definitions is None:
            stimulus_definitions = []

        self.presentation_settings: PresentationSettings = {
            "duration_after": None,
            "rl_label_before": None,
            "rl_label_after": None,
            "name_before": None,
            "name_after": None,
            "present_after": False,
        }

        if presentation_settings is not None:
            self.presentation_settings = {
                **self.presentation_settings,
                **presentation_settings,
            }

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

        if self.too_early_warning is not None:
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
        state = {"extra_info": {}}
        self.draw_list = None

        if self.before_action_callback:
            out = self.before_action_callback(self, context)
            if out is not None:
                state.update(out)

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

        self.draw_list = None

        if self.flip:
            context.render.flip()

        if self.presentation_settings["name_before"]:
            log_event(
                self,
                logger=context.logger,
                extra_info={
                    "event_type": self.presentation_settings["name_before"],
                    "rl_label": self.presentation_settings["rl_label_before"],
                    **state["extra_info"],
                },
            )

        response = response_handling(
            self, context, response_window_onset=response_window_onset
        )

        if self.detect_too_early and too_early:
            _action, remaining = response
            response = (self.too_early_action, remaining)
            self.too_early_warning.draw()

        if self.after_action_callback:
            self.after_action_callback(self, context, state, response)

        if self.presentation_settings["present_after"]:
            after_onset = context.logger.get_time()

            for stim_name in self.draw_list:
                if self.stimuli[stim_name].opacity > 0:
                    self.stimuli[stim_name].draw()

            context.render.flip()

            context.render.wait(
                logger=context.logger,
                input_handler=context.input_handler,
                time=self.presentation_settings["duration_after"],
                start=after_onset,
                poll_keys=self.poll_keys,
            )

            log_event(
                self,
                context.logger,
                onset=after_onset,
                extra_info={
                    "event_type": self.presentation_settings["name_after"],
                    "rl_label": self.presentation_settings["rl_label_after"],
                },
            )
        print(response)

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


class NAFCRoutine(ActionRoutine):
    def __init__(
        self,
        name,
        duration: float,
        key_dict: dict,
        rl_label: str | None = None,
        stimulus_mapping: dict[int, StimulusDefinition] | None = None,
        scene_stimuli: list[StimulusDefinition] | None = None,
        timeout_action: Any | None = None,
        name_timeout: str | None = None,
        flip: bool = True,
        poll_keys=True,
        presentation_settings: PresentationSettings | None = None,
        detect_too_early: bool = False,
        too_early_action: Any | None = None,
        too_early_warning: StimulusDefinition | None = None,
        positions: dict[int, tuple[float | int, float | int]] | None = None,
        randomize_positions: bool = False,
        highlight_selected: bool = True,
        highlight_definition: RectangleDefinition | None = None,
    ):
        self.presentation_settings: PresentationSettings = {
            "duration_after": None,
            "rl_label_before": None,
            "rl_label_after": None,
            "name_before": "display",
            "name_after": "selection",
            "present_after": True,
        }

        self.positions = positions
        self.randomize_positions = randomize_positions

        stimulus_definitions = []

        self.stimulus_mapping = {}
        if stimulus_mapping is not None:
            for k, v in stimulus_mapping.items():
                stimulus_definitions.append(v)
                self.stimulus_mapping[k] = v.name

        if scene_stimuli is not None:
            self.scene_stimuli = [i.name for i in scene_stimuli]
            stimulus_definitions.extend(scene_stimuli)
        else:
            self.scene_stimuli = []

        if highlight_selected:
            if highlight_definition is None:
                highlight_definition = RectangleDefinition(
                    name="border",
                    lineColor="white",
                    lineWidth=10,
                    height=0,
                    width=0,
                )

            stimulus_definitions.append(highlight_definition)
            self.highlight_name = highlight_definition.name
        else:
            self.highlight_name = None

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            flip=flip,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
            before_action_callback=nfc_setup,
            after_action_callback=nfc_selection,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            key_dict=key_dict,
            detect_too_early=detect_too_early,
            too_early_action=too_early_action,
            too_early_warning=too_early_warning,
            presentation_settings=presentation_settings,
        )
        if presentation_settings is not None:
            self.presentation_settings = {
                **self.presentation_settings,
                **presentation_settings,
            }


class ChangeSceneAfterAction(ActionRoutine):
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
        presentation_settings: PresentationSettings | None = None,
        before_action_callback: None = None,
        after_action_callback: None = None,
        detect_too_early: bool = False,
        too_early_action: Any | None = None,
        too_early_warning: StimulusDefinition | None = None,
        draw_stims_before: list[str] | None = None,
        draw_stims_after: list[str] | None = None,
    ):
        self.draw_stims_before = draw_stims_before

        if self.draw_stims_before is None:
            self.draw_stims_before = [i.name for i in stimulus_definitions]

        self.draw_stims_after = draw_stims_after

        if self.draw_stims_after is None:
            self.draw_stims_after = [i.name for i in stimulus_definitions]

        super().__init__(
            name=name,
            duration=duration,
            rl_label=rl_label,
            flip=flip,
            poll_keys=poll_keys,
            stimulus_definitions=stimulus_definitions,
            before_action_callback=draw_subset_before,
            after_action_callback=draw_subset_after,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            key_dict=key_dict,
            detect_too_early=detect_too_early,
            too_early_action=too_early_action,
            too_early_warning=too_early_warning,
            presentation_settings=presentation_settings,
        )
