from typing import List, Tuple

from psychopy import visual

from .logger import ExperimentLogger


class WaitTime:
    """
    WaitTime class. This a class used to put the PsychoPy experiment on hold
    for a given duration. While waiting, this class also checks if any buttons
    have been pressed, so that the experiment can be terminated or MRI triggers
    can be collected.
    """

    def __init__(
        self,
        win: visual.Window,
        logger: ExperimentLogger = None,
        frameDuration: float = 1 / 60,
    ):
        """
        Class to wait for a given time. Logs keypresses in between.

        Parameters
        ----------
        win : visual.Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger, optional
            The logger associated with the experiment, by default None
        frameDuration : float, optional
             frame refresh of the screen, duration in 1/HZ. Defaults to 1/60, by default 1/60
        """

        self.logger = logger
        self.frameDuration = frameDuration
        self.win = win

    def wait(self, time: float, start: float = None):
        """
        Wait for a given time.


        Parameters
        ----------
        time : float
            Time to wait, in seconds.
        start : float, optional
            Specify a different time, than the current one of the Logger, by default None
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


class BaseStimulus:
    """
    Base class for stimulus presentation. If called on its own it will flip the
    window.
    """

    def __init__(self, duration: float = None, name: str = None):
        """
        Stimulus presentation base class. The parameters do not really do anything.

        Parameters
        ----------
        duration : float, optional
            duration of the stimulus presentation, by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        """
        self.duration = duration
        self.name = name

    def setup(self, win: visual.Window, **kwargs):
        """
        Call this to setup the stimulus. This means associating the stimulus
        with a window (so there is something to flip).

        Parameters
        ----------
        win : visual.Window
            The psychopy window object that is used for displaying stimuli.
        """

        self.win = win

    def __call__(self, **kwargs) -> None:
        """
        Calls the stimulus object. In this case initiate a window flip.
        Should only return something, if there has been an action required.

        Returns
        -------
        None
            None
        """
        self.win.flip()

        return None


class TextStimulus(BaseStimulus):
    """
    A stimulus class for text display in psychopy.
    """

    def __init__(
        self,
        duration: float,
        text: str,
        position: Tuple[int, int] = None,
        name: str = None,
        text_color: str = "white",
    ):
        """
        Stimulus class for text displays.

        Parameters
        ----------
        duration : float
            Duration of the stimulus presentation.
        text : str
            The text that should be displayed on the screen.
        position : Tuple[int, int], optional
            Where to display the text (by default in px), by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        text_color : str, optional
            Color of the text string, by default "white"
        """

        super().__init__(name=name, duration=duration)

        self.text = text
        self.position = position
        self.text_color = text_color

    def setup(self, win: visual.Window, **kwargs):
        """
        Performs the setup for the stimulus object. Initiating a PsychoPy.TextStim,
        object, using the parameters given parameters.

        Parameters
        ----------
        win : visual.Window
            The psychopy window object that is used for displaying stimuli.
        """

        self.textStim = visual.TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )

    def __call__(
        self, win: visual.Window, logger: ExperimentLogger, wait: WaitTime, **kwargs
    ) -> None:
        """
        Calls the stimulus object. In this case drawing the text stim, flipping the window,
        waiting and logging.

         Parameters
         ----------
         win : visual.Window
             The psychopy window object that is used for displaying stimuli.
         logger : ExperimentLogger
             The logger associated with the experiment.
         wait : WaitTime
             The WaitTime object associated with the experiment.

         Returns
         -------
         None
             None
        """
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


class ImageStimulus(BaseStimulus):
    def __init__(
        self,
        duration: float,
        image_paths: List,
        positions: List = None,
        name: str = None,
    ):

        super().__init__(name=name, duration=duration)

        self.image_paths = image_paths
        self.positions = positions

    def setup(self, win: visual.Window, image_paths=None, **kwargs):

        if image_paths is not None:
            self.image_paths = image_paths

        self.imageStims = []
        for ip, pos in zip(self.image_paths, self.positions):
            self.imageStims.append(visual.ImageStim(win, image=ip, pos=pos))

    def __call__(
        self, win: visual.Window, logger: ExperimentLogger, wait: float, **kwargs
    ):

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


class ActionStim(BaseStimulus):
    def __init__(
        self,
        duration: float,
        key_dict: dict = {"left": 0, "right": 1},
        name: str = None,
        timeout_action: int = None,
    ):

        super().__init__(name=name, duration=duration)

        self.key_list = list(key_dict.keys())
        self.key_dict = key_dict
        self.timeout_action = timeout_action

    def setup(self, win: visual.Window, **kwargs):
        pass

    def __call__(
        self, win: visual.Window, logger: ExperimentLogger, wait: float, **kwargs
    ):

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


class FeedBackText(BaseStimulus):
    def __init__(
        self,
        duration: float,
        text: str,
        position: Tuple[int, int] = None,
        name: str = None,
        target: str = "reward",
        text_color: str = "white",
    ):

        super().__init__(name=name, duration=duration)

        self.text = text
        self.position = position
        self.text_color = text_color
        self.target = target

    def setup(self, win: visual.Window, **kwargs):

        self.textStim = visual.TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )
        self.textStim.setAutoDraw(False)

    def __call__(
        self,
        win: visual.Window,
        logger: ExperimentLogger,
        wait: float,
        reward: float,
        total_reward: float,
        **kwargs,
    ):

        if self.target == "reward":
            reward = f"+{reward}" if reward > 0 else f"{reward}"
            self.textStim.setText(self.text.format(reward))
        elif self.target == "total_reward":
            total_reward = f"+{total_reward}" if total_reward > 0 else f"{total_reward}"
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
