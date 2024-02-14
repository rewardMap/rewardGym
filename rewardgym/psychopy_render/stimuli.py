from psychopy import visual

from .logger import ExperimentLogger


class WaitTime:
    def __init__(
        self,
        win: visual.Window,
        logger: ExperimentLogger = None,
        frameDuration: float = 1 / 60,
    ):
        """Class to wait for a given time. Logs keypresses in between.

        Args:
            win (visual.Window): Psychopy window.
            logger (ExperimentLogger, optional): Logging class, to get MR pulses.
                Defaults to None.
            frameDuration (float, optional): Duration in 1/HZ. Defaults to 1/60.
        """

        self.logger = logger
        self.frameDuration = frameDuration
        self.win = win

    def wait(self, time: float, start: float = None):
        """Wait for a given time.

        Args:
            time (float): Time to wait.
            start (float, optional): Specify time or use logging clock. Defaults to None.
        """

        if start is None:
            start = self.logger.getTime()

        t_wait = start + time  # - self.frameDuration

        # Trying to avoid unecessary checks
        if self.logger is not None:
            while t_wait > self.logger.getTime():
                self.logger.keyStrokes(self.win)

        else:
            while t_wait > self.logger.getTime():
                pass


class BaseStimuli:
    def __init__(self, duration):

        self.duration = duration

    def setup(self, win):
        self.win = win

    def __call__(self, **kwargs):

        self.win.flip()


class TextStimulus(BaseStimuli):
    def __init__(self, duration, text, position=None, name=None, text_color="white"):
        self.duration = duration
        self.text = text
        self.position = position
        self.name = name
        self.text_color = text_color

    def setup(self, win):

        self.textStim = visual.TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )
        self.textStim.setAutoDraw(False)

    def __call__(self, win, logger, wait, **kwargs):

        logger.keyStrokes(win)

        stim_onset = logger.getTime()
        self.textStim.draw()
        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.logEvent(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


class ImageStimulus(BaseStimuli):
    def __init__(self, duration, image_paths, positions=None, name=None):
        self.duration = duration
        self.image_paths = image_paths
        self.positions = positions
        self.name = name

    def setup(self, win):

        self.imageStims = []
        for ip, pos in zip(self.image_paths, self.positions):
            self.imageStims.append(visual.ImageStim(win, image=ip, pos=pos))
            self.imageStims.setAutoDraw(False)

    def __call__(self, win, logger, wait, **kwargs):

        logger.keyStrokes(win)

        stim_onset = logger.getTime()

        for ii in self.imageStims:
            ii.draw()

        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.logEvent(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


class ActionStim(BaseStimuli):
    def __init__(
        self, duration, key_dict={"left": 0, "right": 1}, name=None, timeout_action=None
    ):
        self.duration = duration
        self.name = name
        self.key_list = list(key_dict.keys())
        self.key_dict = key_dict
        self.timeout_action = timeout_action

    def setup(self, win):
        pass

    def __call__(self, win, logger, wait, **kwargs):

        logger.keyStrokes(win)

        response_window_onset = logger.getTime()
        response_window = response_window_onset + self.duration
        response_present = False

        while response_window > logger.getTime() and response_present is False:

            response = logger.keyStrokes(win, keyList=self.key_list)

            if response:
                RT = response[1] - response_window_onset
                logger.logEvent(
                    {
                        "event_type": "Response",
                        "response_button": response[0],
                        "response_time": RT,
                    },
                    onset=response_window_onset,
                )
                response_present = True
                response_key = self.key_dict[response[0]]

        if response_present is False:
            RT = None
            logger.logEvent(
                {
                    "event_type": "ResponseTimeOut",
                    "response_late": True,
                    "response_time": RT,
                },
                onset=response_window_onset,
            )
            response_key = self.timeout_action

        # To undraw response windows
        win.flip()

        return response_key


class FeedBackText(BaseStimuli):
    def __init__(
        self,
        duration,
        text,
        position=None,
        name=None,
        target="reward",
        text_color="white",
    ):
        self.duration = duration
        self.text = text
        self.position = position
        self.name = name
        self.text_color = text_color
        self.target = target

    def setup(self, win):

        self.textStim = visual.TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )
        self.textStim.setAutoDraw(False)

    def __call__(self, win, logger, wait, reward, total_reward, **kwargs):

        if self.target == "reward":
            self.textStim.setText(self.text.format(reward))
        elif self.target == "total_reward":
            self.textStim.setText(self.text.format(total_reward))

        logger.keyStrokes(win)

        stim_onset = logger.getTime()
        self.textStim.draw()
        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.logEvent(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None