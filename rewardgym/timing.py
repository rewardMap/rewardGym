# Will be used later on - it's

def wait(
    logger, win, time: float, start: float | None = None, wait_no_keys: bool = False
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
    if time is None:
        return

    if start is None:
        start = logger.get_time()

    t_wait = start + time  # - logger.frameDuration

    # Trying to avoid unnecessary checks
    while t_wait > logger.get_time():
        if not wait_no_keys:
            logger.key_strokes(win)


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
