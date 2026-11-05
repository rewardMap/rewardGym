from typing import Any

from .environments import StepContext
from .protocols import LoggerProtocol
from .render_base import ActionRoutine, PresentationRoutine
from .utils import get_key_from_dict

from enum import Enum


class PollStatus(Enum):
    WAITING = "waiting"
    RECEIVED = "received"
    TIMEOUT = "timeout"


def log_event(
    routine: ActionRoutine | PresentationRoutine,
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
    routine: ActionRoutine,
    context: StepContext,
    response_window_onset: float,
    key_dict=None,
) -> tuple[int | None, float | None] | None | Any:
    input_handler = context.input_handler
    logger = context.logger
    info = context.info

    if key_dict is None:
        key_dict = routine.key_dict

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
                env_action = get_response_from_action(action, info)
                key_action = get_key_from_dict(key_dict, env_action)[
                    0
                ]  # TODO: More safeguarding.
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
            env_action = get_action_from_response_key(response_button, info, key_dict)

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


def get_action_from_response_key(
    response_key: int | str, info: dict | None, key_dict: dict
):
    if info is None or "behav_remap" not in info:
        return None
    else:
        return info["behav_remap"][key_dict[response_key]]


def get_response_from_action(action: int | str, info: dict | None):
    if info is None or "behav_remap" not in info:
        return action

    else:
        response_button = [n for n, b in enumerate(info["behav_remap"]) if b == action]

        if len(response_button) == 1:
            response_button = response_button[0]
        else:
            response_button = action

    return response_button


def simulate_response(
    routine: ActionRoutine,
    context: StepContext,
    response_window_onset,
    info,
):
    if routine.duration is None:
        raise ValueError(f"{routine.duration} needs to be defined.")

    logger = context.logger
    response_key = context.previous_action
    rt = context.reaction_time

    if rt is None:
        raise ValueError(
            "Simulations should run with `expose_last_stim=True`. rt cannot be 'None'!"
        )

    if rt > routine.duration:
        if response_key is None:
            response_key = logger.na
            response_button = logger.na

        logger.log_event(
            {
                "event_type": routine.name_timeout,
                "response_late": True,
                "response_time": rt,
                "response_button": response_button,
                "action": response_key,
                "rl_label": routine.rl_label,
            },
            onset=response_window_onset,
        )
        response_key = routine.timeout_action
        remaining = None

        if response_key is None:
            return None

    else:
        logger.log_event(
            {
                "event_type": routine.name,
                "response_button": response_button,
                "response_time": rt,
                "action": response_key,
                "rl_label": routine.rl_label,
            },
            onset=response_window_onset,
        )
        remaining = routine.duration - rt

    return response_key, remaining
