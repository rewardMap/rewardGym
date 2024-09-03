from typing import Dict, List, Literal, Tuple, Union

try:
    from psychopy.visual import ImageStim, TextStim, Window
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim, ImageStim

from .default_images import lose_cross, win_cross, zero_cross
from .logger import ExperimentLogger, SimulationLogger


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

    def display(self, win: Window, logger: ExperimentLogger, **kwargs) -> None:
        """
        Calls the stimulus object. In this case initiate a window flip.
        Should only return something, if there has been an action required.

        Returns
        -------
        None
            Should return None

        """
        logger.key_strokes(win)

        stim_onset = logger.get_time()

        win.flip()

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None

    def simulate(self, logger: ExperimentLogger, **kwargs) -> None:
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

    def display(self, win: Window, logger: ExperimentLogger, **kwargs) -> None:
        """
        Calls the stimulus object. In this case drawing the text stim, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.

        Returns
        -------
        None
        Should return None

        """
        logger.key_strokes(win)

        stim_onset = logger.get_time()
        self.textStim.draw()
        win.flip()

        logger.wait(win, self.duration, stim_onset)

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
        width: float = None,
        height: float = None,
        autodraw: bool = False,
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

        if positions is None:
            positions = [(0, 0)] * len(image_paths)

        self.positions = positions
        self.width = width
        self.height = height
        self.autodraw = autodraw

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
            if isinstance(ip, str):
                self.imageStims.append(ImageStim(win, image=ip, pos=pos))

            else:
                width = ip.shape[1] if self.width is None else self.width
                height = ip.shape[0] if self.height is None else self.height
                self.imageStims.append(
                    ImageStim(win, image=ip, size=(width, height), pos=pos)
                )

        for ip in self.imageStims:
            ip.autoDraw = self.autodraw

    def display(self, win: Window, logger: ExperimentLogger, **kwargs):
        """
        Calls the stimulus object. In this case drawing the images stims, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.

        Returns
        -------
        None
        Should return None
        """
        logger.key_strokes(win)

        stim_onset = logger.get_time()

        # So that images are drawn on top
        for ii in self.imageStims:
            ii.autoDraw = True

        win.flip()

        for ii in self.imageStims:
            ii.autoDraw = self.autodraw

        logger.wait(win, self.duration, stim_onset)

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
        name: str = "response",
        timeout_action: int = None,
        name_timeout="response-time-out",
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
        self.name_timeout = name_timeout

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
                        "event_type": self.name,
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

            response_key = self.timeout_action

            if response_key is None:
                response_key = logger.na

            logger.log_event(
                {
                    "event_type": self.name_timeout,
                    "response_late": True,
                    "response_time": RT,
                    "response_button": response_key,
                },
                onset=response_window_onset,
            )

            if response_key == logger.na:
                return None

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
        logger.global_clock.time += min([rt, self.duration])

        if rt > self.duration:
            if response_key is None:
                response_key = logger.na

            logger.log_event(
                {
                    "event_type": self.name_timeout,
                    "response_late": True,
                    "response_time": rt,
                    "response_button": response_key,
                },
                onset=response_window_onset,
            )
            response_key = self.timeout_action
            remaining = None

            if response_key is None:
                return None

        else:
            logger.log_event(
                {
                    "event_type": self.name,
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
        position: Tuple[int, int] = (0, 125),
        name: str = None,
        target: Literal["reward", "total_reward"] = "reward",
        text_color: str = "white",
        font_height: float = 50,
        feedback_stim: Dict = True,
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
        feedback_stim : Dict, optional
            If the feedback_stim should be displayed, if True changes fixation cross,
            if None does not show an image as feedback. For other images populate the
            keys: win, lose, zero with a string to an image or a numpy array.
        """

        super().__init__(name=name, duration=duration)

        self.text = text
        self.position = position
        self.text_color = text_color
        self.target = target

        if feedback_stim is True:
            self.feedback_stim = {
                "win": win_cross(),
                "lose": lose_cross(),
                "zero": zero_cross(),
            }
        elif feedback_stim is None or feedback_stim is False:
            self.feedback_stim = {}
        else:
            self.feedback_stim = feedback_stim

        self.font_height = font_height

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
            win=win,
            name=self.name,
            text=self.text,
            color=self.text_color,
            height=self.font_height,
            pos=self.position,
        )
        self.textStim.setAutoDraw(False)

        self.feedback_image = {}

        for kk in self.feedback_stim.keys():
            if isinstance(self.feedback_stim[kk], str):
                self.feedback_image[kk] = ImageStim(
                    win=win, image=self.feedback_stim[kk]
                )
            else:
                self.feedback_image[kk] = ImageStim(
                    win,
                    image=self.feedback_stim[kk],
                    size=self.feedback_stim[kk].shape[:2],
                )

    def display(
        self,
        win: Window,
        logger: ExperimentLogger,
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
            if reward > 0:
                feedback_img = "win"
            elif reward < 0:
                feedback_img = "lose"
            else:
                feedback_img = "zero"

            reward = f"+{reward}" if reward > 0 else f"{reward}"
            self.textStim.setText(self.text.format(reward))

        elif self.target == "total_reward":
            total_reward = f"+{total_reward}" if total_reward > 0 else f"{total_reward}"
            self.textStim.setText(self.text.format(total_reward))
            feedback_img = "None"

        logger.key_strokes(win)

        stim_onset = logger.get_time()
        if feedback_img in self.feedback_image.keys():
            self.feedback_image[feedback_img].autoDraw = True

        self.textStim.draw()
        win.flip()

        if feedback_img in self.feedback_image.keys():
            self.feedback_image[feedback_img].autoDraw = False

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {
                "event_type": self.name,
                "expected_duration": self.duration,
                "total_reward": total_reward,
            },
            onset=stim_onset,
            reward=reward,
        )

        return None

    def simulate(
        self,
        logger=ExperimentLogger,
        reward: float = None,
        total_reward: float = None,
        **kwargs,
    ) -> None:
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
            {
                "event_type": self.name,
                "expected_duration": self.duration,
                "total_reward": total_reward,
            },
            onset=stim_onset,
            reward=reward,
        )
