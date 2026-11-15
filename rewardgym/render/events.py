from enum import Enum
from typing import Any

from ..protocols import LoggerProtocol
from .contexts import StepContext


class PollStatus(Enum):
    WAITING = "waiting"
    RECEIVED = "received"
    TIMEOUT = "timeout"


def log_event(
    routine,
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
    routine,
    context: StepContext,
    response_window_onset: float,
    key_dict=None,
) -> tuple[int | None, float | None] | None | Any:
    input_handler = context.input_handler
    logger = context.logger
    layout = context.info["action-layout"]

    if key_dict is None:
        key_dict = routine.key_dict

    tmp = {}

    for k, v in key_dict.items():
        if v in layout.action_to_graph and layout.action_to_graph[v] is not None:
            tmp[k] = v

    key_dict = tmp
    layout.add_keys(key_dict)

    # Values to be set:
    response = None
    polling_state = PollStatus.WAITING
    remaining = None
    response_window = response_window_onset + routine.duration
    env_action = None

    if routine.duration is None:
        raise ValueError(f"{routine.duration} needs to be defined.")

    if "simulation" in context.env_context.mode:
        env_action = context.previous_action
        response_time = context.reaction_time
        if response_time is not None and routine.duration is not None:
            if response_time > routine.duration:
                polling_state = PollStatus.TIMEOUT
            else:
                polling_state = PollStatus.RECEIVED
                action = layout.graph_to_action[env_action]
                response_button = layout.graph_to_key[env_action][0]
                response = (response_button, response_time + response_window_onset)

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

        if env_action is None and response_button in layout.key_to_graph:
            env_action = layout.key_to_graph[response_button]

        action = layout.key_to_action[response_button]

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
        action = routine.timeout_action

        if action is None:
            action = logger.na
        else:
            env_action = layout.action_to_graph[action]

        log_event(
            routine=routine,
            logger=logger,
            onset=response_window_onset,
            extra_info={
                "response_button": logger.na,
                "response_late": True,
                "action": env_action,
                "event_type": routine.name_timeout,
            },
        )

        if action == logger.na:
            return None

    return action, remaining
