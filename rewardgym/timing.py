# Will be used later on - it's
from .keyhandler import InputProtocol


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

    # Trying to avoid unnecessary checks
    while t_wait > logger.get_time():
        if poll_keys and input_handler:
            keys = input_handler.get_keys()
            input_handler.interpret_keys(keys, key_list=None, logger=logger)


def simulation_wait(clock, time: float, start: float | None = None):
    """
    Wait for a given time.


    Parameters
    ----------
    time : float
        Time to wait, in seconds.
    start : float, optional
        Specify a different time, than the current one of the Logger, by default None
    """
    if time is None:
        return

    if start is None:
        start = clock.get_time()

    clock.time += time
