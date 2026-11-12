from enum import Enum
from typing import Any

from ..protocols import LoggerProtocol
from .contexts import StepContext
from .render_base import BaseRoutine


class PollStatus(Enum):
    WAITING = "waiting"
    RECEIVED = "received"
    TIMEOUT = "timeout"


def log_event(
    routine: BaseRoutine,
    logger: LoggerProtocol,
    onset: float | None = None,
    extra_info: dict | None = None,
):
    """Logging short hand for Routines."""
    base_dict = {
        "event_type": routine.name,
        "expected_duration": routine.duration,
        "rl_label": routine.rl_label,
    }

    if extra_info:
        base_dict.update(extra_info)

    logger.log_event(base_dict, onset=onset)


def response_handling(
    routine: BaseRoutine,
    context: StepContext,
    response_window_onset: float,
    key_dict=None,
) -> tuple[int | None, float | None] | None | Any:
    input_handler = context.input_handler
    logger = context.logger
    layout = context.info["action-layout"]

    if key_dict is None:
        key_dict = routine.key_dict

    layout.add_keys(key_dict)

    # Values to be set:
    response = None
    polling_state = PollStatus.WAITING
    remaining = None
    response_window = response_window_onset + routine.duration
    env_action = None

    if routine.duration is None:
        raise ValueError(f"{routine.duration} needs to be defined.")

    if "simulate" in context.env_context.mode:
        action = context.previous_action
        response_time = context.reaction_time

        if response_time is not None and routine.duration is not None:
            if response_time > routine.duration:
                polling_state = "timeout"
            else:
                polling_state = PollStatus.RECEIVED
                env_action = layout.action_to_graph[action]
                key_action = layout.graph_to_key[env_action][0]

                response = (key_action, response_time + response_window_onset)

        advance = routine.duration
        if response_time is not None:
            advance = min([response_time, routine.duration])

        logger.clock.time += advance

    while polling_state == PollStatus.WAITING:
        response = input_handler.key_strokes(
            logger=logger, key_list=list(key_dict.keys())
        )

        if response_window <= logger.get_time():
            polling_state = PollStatus.TIMEOUT
        if response:
            polling_state = PollStatus.RECEIVED

    if polling_state == PollStatus.RECEIVED:
        response_button, response_time = response
        # Casting response time to reaction time:
        reaction_time = response_time - response_window_onset

        if env_action is None:
            env_action = layout.key_to_graph[response_button]

        key_action = key_dict[response_button]

        log_event(
            routine=routine,
            logger=logger,
            onset=response_window_onset,
            extra_info={
                "response_button": response_button,
                "response_time": reaction_time,
                "action": env_action,
            },
        )

        remaining = routine.duration - reaction_time

    elif polling_state == PollStatus.TIMEOUT:
        key_action = routine.timeout_action

        if key_action is None:
            key_action = logger.na

        log_event(
            routine=routine,
            logger=logger,
            onset=response_window_onset,
            extra_info={
                "response_button": logger.na,
                "response_late": True,
                "action": key_action,
                "event_type": routine.name_timeout,
            },
        )

        if key_action == logger.na:
            return None

    return key_action, remaining
