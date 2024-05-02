from typing import Dict, List, Literal, Tuple, Union

try:
    from psychopy.visual import ImageStim, TextStim, Window
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim, ImageStim

from .logger import ExperimentLogger, SimulationLogger


class WaitTime:
    """
    WaitTime class. This a class used to put the PsychoPy experiment on hold
    for a given duration. While waiting, this class also checks if any buttons
    have been pressed, so that the experiment can be terminated or MRI triggers
    can be collected.
    """

    def __init__(
        self,
        win: Window,
        logger: ExperimentLogger = None,
        frameDuration: float = 1 / 60,
    ):
        """
        Class to wait for a given time. Logs keypresses in between.

        Parameters
        ----------
        win : Window
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
            start = self.logger.get_time()

        t_wait = start + time  # - self.frameDuration

        # Trying to avoid unecessary checks
        if self.logger is not None:
            while t_wait > self.logger.get_time():
                self.logger.key_strokes(self.win)

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

    def setup(self, win: Window, **kwargs):
        """
        Call this to setup the stimulus. This means associating the stimulus
        with a window (so there is something to flip).

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """

        self.win = win

    def display(self, **kwargs) -> None:
        """
        Calls the stimulus object. In this case initiate a window flip.
        Should only return something, if there has been an action required.

        Returns
        -------
        None
            Should return None

        """
        self.win.flip()

        return None

    def simulate(self, logger=ExperimentLogger, **kwargs) -> None:
        """
        Function to pretend that a stimulus has been shown. Logging and creating
        timing.

        Returns
        -------
        None
            Does not return anything, but logs the stimulus.
        """

        stim_onset = logger.get_time()

        logger.global_clock.time += self.duration

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )


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

    def setup(self, win: Window, **kwargs):
        """
        Performs the setup for the stimulus object. Initiating a PsychoPy.TextStim,
        object, using the parameters given parameters.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """

        self.textStim = TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )

    def display(
        self, win: Window, logger: ExperimentLogger, wait: WaitTime, **kwargs
    ) -> None:
        """
        Calls the stimulus object. In this case drawing the text stim, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.
        wait : WaitTime
            The WaitTime object associated with the experiment.

        Returns
        -------
        None
        Should return None

        """
        logger.key_strokes(win)

        stim_onset = logger.get_time()
        self.textStim.draw()
        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


class ImageStimulus(BaseStimulus):
    """
    A stimulus class to display (multiple) images in psychopy.
    """

    def __init__(
        self,
        duration: float,
        image_paths: List,
        positions: List = None,
        name: str = None,
    ):
        """
        Stimulus class for image displays.

        Parameters
        ----------
        duration : float
            Duration of the stimulus presentation.
        image_paths : List
            A list of paths to images that should be displayed on screen.
        positions : List, optional
            A list of positions (where the images should be displayed), by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        """

        super().__init__(name=name, duration=duration)

        self.image_paths = image_paths
        self.positions = positions

    def setup(self, win: Window, image_paths=None, **kwargs):
        """
        Performs the setup for the stimulus object. Initiating PsychoPy.ImageStim objects,
        given the provides paths and positions.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.

        image_paths : _type_, optional
            Image paths can be overwritten during setup, for example to allow for randomization, by default None
        """

        if image_paths is not None:
            self.image_paths = image_paths

        self.imageStims = []
        for ip, pos in zip(self.image_paths, self.positions):
            self.imageStims.append(ImageStim(win, image=ip, pos=pos))

    def display(self, win: Window, logger: ExperimentLogger, wait: float, **kwargs):
        """
        Calls the stimulus object. In this case drawing the images stims, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.
        wait : WaitTime
            The WaitTime object associated with the experiment.

        Returns
        -------
        None
        Should return None
        """
        logger.key_strokes(win)

        stim_onset = logger.get_time()

        for ii in self.imageStims:
            ii.draw()

        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


class ActionStimulus(BaseStimulus):
    """
    Stimulus class, for when actions are required by the participants.
    """

    def __init__(
        self,
        duration: float,
        key_dict: Dict = {"left": 0, "right": 1},
        name: str = None,
        timeout_action: int = None,
    ):
        """
        Setting up the action object.

        Parameters
        ----------
        duration : float
            Duration of the response window.
        key_dict : dict, optional
            Dictionary to map keyboard responses to actions recognized by the environment, by default {"left": 0, "right": 1}
        name : str, optional
            name of the object, will be used for logging, by default None
        timeout_action : int, optional
            Behavior of the object if the response window times out, making it possible that no response is also a distinc action, by default None
        """

        super().__init__(name=name, duration=duration)

        self.key_list = list(key_dict.keys())
        self.key_dict = key_dict
        self.timeout_action = timeout_action

    def setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """
        pass

    def display(
        self, win: Window, logger: ExperimentLogger, **kwargs
    ) -> Union[int, str]:
        """
        Calls the stimulus object. In this case waiting for a specific response,
        returning it and logging the process. Flipping the window in the end.


        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.

        Returns
        -------
        Union[int, str]
            The response issued by the participant, interpretable by the environment.
        """
        logger.key_strokes(win)

        response_window_onset = logger.get_time()
        response_window = response_window_onset + self.duration
        response_present = False
        remaining = None

        # Main loop, keeping time and waiting for response.
        while response_window > logger.get_time() and response_present is False:

            response = logger.key_strokes(win, keyList=self.key_list)

            if response:
                RT = response[1] - response_window_onset
                logger.log_event(
                    {
                        "event_type": "Response",
                        "response_button": response[0],
                        "response_time": RT,
                    },
                    onset=response_window_onset,
                )
                response_present = True
                response_key = self.key_dict[response[0]]

                remaining = self.duration - RT

        # What todo if response window timed out and now response has been given.
        if response_present is False:
            RT = None
            logger.log_event(
                {
                    "event_type": "ResponseTimeOut",
                    "response_late": True,
                    "response_time": RT,
                },
                onset=response_window_onset,
            )
            response_key = self.timeout_action

        win.flip()

        return response_key, remaining

    def simulate(
        self,
        win: Window,
        logger=SimulationLogger,
        key: str = None,
        rt: float = None,
        **kwargs,
    ):

        response_key, rt = logger.key_strokes(key, rt)
        response_window_onset = logger.get_time()
        logger.global_clock.time += rt

        if rt > self.duration:
            logger.log_event(
                {
                    "event_type": "ResponseTimeOut",
                    "response_late": True,
                    "response_time": rt,
                },
                onset=response_window_onset,
            )
            response_key = self.timeout_action
            remaining = None
        else:
            logger.log_event(
                {
                    "event_type": "Response",
                    "response_button": response_key,
                    "response_time": rt,
                },
                onset=response_window_onset,
            )
            remaining = self.duration - rt

        return response_key, remaining


class FeedBackStimulus(BaseStimulus):
    """
    Class that possibly will be superseded or become obsolete at some point.

    Purpose of the class is to provide feedback to the participant, about the
    number of points they have received in a given trial or across the experiment.
    """

    def __init__(
        self,
        duration: float,
        text: str,
        position: Tuple[int, int] = None,
        name: str = None,
        target: Literal["reward", "total_reward"] = "reward",
        text_color: str = "white",
    ):
        """
        FeedBack class, provides feedback to the participant, by creating
        updatable TextStims.

        Parameters
        ----------
        duration : float
            Duration of the feedback.
        text : str
            The text that should be displayed on the screen. Should be a format string!
        position : Tuple[int, int], optional
            Where to display the text (by default in px), by default None
        name : str, optional
            name of the object, will be used for logging, by default None
        target : Literal[&quot;reward&quot;, &quot;total_reward&quot;], optional
            If the trial's reward or the total reward should be shown, by default "reward"
        text_color : str, optional
            Color of the text, by default "white"
        """

        super().__init__(name=name, duration=duration)

        self.text = text
        self.position = position
        self.text_color = text_color
        self.target = target

    def setup(self, win: Window, **kwargs):
        """
        Performs the setup for the stimulus object. Initiating a PsychoPy.TextStim,
        object, using the parameters given parameters.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """

        self.textStim = TextStim(
            win=win, name=self.name, text=self.text, color=self.text_color
        )
        self.textStim.setAutoDraw(False)

    def display(
        self,
        win: Window,
        logger: ExperimentLogger,
        wait: float,
        reward: float,
        total_reward: float,
        **kwargs,
    ) -> None:
        """
        Calls the stimulus object, to display the reward. Uses reward or total_reward
        depending on the target that has been defined.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.
        wait : WaitTime
            The WaitTime object associated with the experiment.
        reward : float
            Reward of the given trial, provided by the environment.
        total_reward : float
            Total reward, provided by the environment.

        Returns
        -------
        None
            Should return None

        """

        # Fills in the format string. Adds the + sign for positive rewards.
        if self.target == "reward":
            reward = f"+{reward}" if reward > 0 else f"{reward}"
            self.textStim.setText(self.text.format(reward))
        elif self.target == "total_reward":
            total_reward = f"+{total_reward}" if total_reward > 0 else f"{total_reward}"
            self.textStim.setText(self.text.format(total_reward))

        logger.key_strokes(win)

        stim_onset = logger.get_time()
        self.textStim.draw()
        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None
