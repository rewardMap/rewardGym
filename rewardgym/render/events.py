from enum import Enum
from typing import Any

from ..protocols import InputProtocol, LoggerProtocol
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

    if hasattr(logger.clock, "advance_time"):
        advance = input_handler.next_response_time()

        if advance is None:
            advance = routine.duration

        advance = min(advance, routine.duration)
        logger.clock.advance_time(advance)

    while polling_state == PollStatus.WAITING:
        response = input_handler.key_strokes(
            logger=logger, key_list=list(key_dict.keys())
        )
        # print("polling", response)
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
            return (None, None)

    return action, remaining


def wait(
    logger,
    time: float | None,
    start: float | None = None,
    poll_keys: bool = True,
    input_handler: InputProtocol | None = None,
):
    """
    Wait for a given time.


    Parameters
    ----------
    time : float
        Time to wait, in seconds.
    start : float, optional
        Specify a different time, than the current one of the Logger, by default None
    """
    if poll_keys and input_handler is None:
        raise ValueError("If poll_keys is True, an InputHandler has to be provided!")

    if time is None:
        return

    if start is None:
        start = logger.get_time()

    t_wait = start + time

    if hasattr(logger.clock, "advance_time"):
        logger.clock.advance_time(time)

    # Trying to avoid unnecessary checks
    while t_wait > logger.get_time():
        if poll_keys and input_handler:
            keys = input_handler.get_keys()
            input_handler.interpret_keys(keys, key_list=None, logger=logger)
