from typing import Dict, List, Literal, Tuple, Union

try:
    from psychopy.visual import ImageStim, TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim, ImageStim, Rect

import warnings

from ..stimuli import lose_cross, win_cross, zero_cross
from .logger import ExperimentLogger, SimulationLogger


class BaseStimulus:
    """
    Base class for stimulus presentation. If called on its own it will flip the
    window.
    """

    def __init__(
        self,
        duration: float = None,
        name: str = None,
        wait_no_keys=False,
        rl_label=None,
        noflip=False,
    ):
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
        self.entity = "base"
        self.wait_no_keys = wait_no_keys
        self.is_setup = False
        self.rl_label = rl_label
        self.noflip = noflip

    def setup(self, win: Window, **kwargs):
        """
        Call this to setup the stimulus. This means associating the stimulus
        with a window (so there is something to flip).

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """

        self._setup(win, **kwargs)
        self.is_setup = True

    def display(self, win: Window, logger: ExperimentLogger, **kwargs) -> None:
        """
        Calls the stimulus object. In this case initiate a window flip.
        Should only return something, if there has been an action required.

        Returns
        -------
        None
            Should return None

        """

        stim_onset = logger.get_time()

        if not self.noflip:
            win.flip()

        logger.wait(win, self.duration, stim_onset, self.wait_no_keys)

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

        logger.wait(win=None, time=self.duration, start=stim_onset)

        self._log_event(logger=logger, stim_onset=stim_onset)

    def _log_event(
        self, logger: ExperimentLogger, stim_onset=None, extra_info={}, **kwargs
    ):
        base_dict = {
            "event_type": self.name,
            "expected_duration": self.duration,
            "rl_label": self.rl_label,
        }

        base_dict.update(extra_info)

        logger.log_event(base_dict, onset=stim_onset, **kwargs)

    def _setup(self, win: Window, **kwargs):
        pass


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
        rl_label: str = None,
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

        super().__init__(name=name, duration=duration, rl_label=rl_label)

        self.text = text
        self.position = position
        self.text_color = text_color

    def _setup(self, win: Window, **kwargs):
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
        stim_onset = logger.get_time()
        self.textStim.draw()
        win.flip()

        logger.wait(win, self.duration, stim_onset)

        self._log_event(logger=logger, stim_onset=stim_onset)

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
        wait_no_keys: bool = False,
        rl_label: str = None,
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
        wait_no_keys : str, optional
            If the logger's wait function should get key presses - only set to True if presses that are too early should be used, by default False
        """

        super().__init__(
            name=name, duration=duration, wait_no_keys=wait_no_keys, rl_label=rl_label
        )

        self.image_paths = image_paths

        if positions is None:
            positions = [(0, 0)] * len(image_paths)

        self.positions = positions
        self.width = width
        self.height = height
        self.autodraw = autodraw

    def _setup(self, win: Window, image_paths=None, **kwargs):
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
        stim_onset = logger.get_time()

        # So that images are drawn on top
        for ii in self.imageStims:
            ii.autoDraw = True

        win.flip()

        for ii in self.imageStims:
            ii.autoDraw = self.autodraw

        logger.wait(win, self.duration, stim_onset, self.wait_no_keys)

        self._log_event(logger=logger, stim_onset=stim_onset)

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
        rl_label: str = None,
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

        super().__init__(name=name, duration=duration, rl_label=rl_label)

        self.key_list = list(key_dict.keys())
        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.entity = "action"

    def _setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """
        pass

    def display(
        self, win: Window, logger: ExperimentLogger, info: Dict, **kwargs
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

        response = self._response_handling(
            win, logger, response_window_onset, info=info
        )

        win.flip()

        return response

    def _response_handling(
        self, win, logger, response_window_onset, key_dict=None, info=None
    ):
        response_window = response_window_onset + self.duration
        response_present = False
        remaining = None

        if key_dict is None:
            key_dict = self.key_dict

        # Main loop, keeping time and waiting for response.
        while response_window > logger.get_time() and response_present is False:
            response = logger.key_strokes(win, keyList=self.key_list)

            if response:
                RT = response[1] - response_window_onset
                response_present = True

                if info is not None and "behav_remap" in info.keys():
                    action = info["behav_remap"][key_dict[response[0]]]

                response_key = key_dict[response[0]]

                logger.log_event(
                    {
                        "event_type": self.name,
                        "response_button": response[0],
                        "response_time": RT,
                        "action": action,
                        "rl_label": self.rl_label,
                    },
                    onset=response_window_onset,
                )

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
                    "response_button": logger.na,
                    "action": self.timeout_action,
                    "rl_label": self.rl_label,
                },
                onset=response_window_onset,
            )

            if response_key == logger.na:
                return None

        return response_key, remaining

    def simulate(
        self,
        win: Window,
        logger=SimulationLogger,
        key: str = None,
        rt: float = None,
        info: Dict = None,
        **kwargs,
    ):
        response_window_onset = logger.get_time()
        response = self._simulate_response(
            logger,
            key,
            rt,
            response_window_onset=response_window_onset,
            info=info,
        )

        return response

    def _simulate_response(self, logger, key, rt, response_window_onset, info):
        response_key, rt = logger.key_strokes(key, rt)

        if info is not None and "behav_remap" in info.keys():
            response_button = [
                n for n, b in enumerate(info["behav_remap"]) if b == response_key
            ]
            if len(response_button) == 1:
                response_button = response_button[0]
            else:
                response_button = response_key

        else:
            response_button = response_key

        if rt is None:
            warnings.warn(
                "Simulating environment: Consider setting expose_last_stim=True during env setup."
            )

        logger.global_clock.time += min([rt, self.duration])

        if rt > self.duration:
            if response_key is None:
                response_key = logger.na
                response_button = logger.na

            logger.log_event(
                {
                    "event_type": self.name_timeout,
                    "response_late": True,
                    "response_time": rt,
                    "response_button": response_button,
                    "action": response_key,
                    "rl_label": self.rl_label,
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
                    "response_button": response_button,
                    "response_time": rt,
                    "action": response_key,
                    "rl_label": self.rl_label,
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
        simple: bool = False,
        bar_total: float = None,
        bar_labels: Dict = {"left": "0 kr", "right": "75 kr"},
        rl_label: str = None,
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

        super().__init__(name=name, duration=duration, rl_label=rl_label)

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
        self.simple = simple
        self.bar_total = bar_total
        self.bar_labels = bar_labels
        self.bar_length = 400
        self.bar_height = 50

    def _setup(self, win, **kwargs):
        self.is_setup = True
        self.reward_text = TextStim(
            win=win,
            name=self.name,
            text=self.text,
            color=self.text_color,
            height=self.font_height,
            pos=self.position,
            font="arial",
            alignText="center",
            anchorHoriz="center",
            units="pix",
        )

        if self.bar_total is None:
            self.total_reward_ind = TextStim(
                win=win,
                name=self.name + "2",
                text="Total: 0.0",
                font="arial",
                color=self.text_color,
                height=20,
                pos=(0, 350),
                alignText="center",
                anchorHoriz="center",
                units="pix",
            )
            self.total_reward_ind.autoDraw = True

        else:
            self.point_bar = Rect(
                win=win,
                name=self.name + "total_bar",
                width=self.bar_length,
                height=self.bar_height,
                lineColor="white",
                fillColor=[0.25, 0.25, 0.75],
                lineWidth=5,
                pos=(0, 350),
                units="pix",
            )

            self.total_reward_ind = Rect(
                win=win,
                name=self.name + "total_indicator",
                width=10,
                height=self.bar_height + 10,
                lineColor=None,
                fillColor="white",
                lineWidth=0,
                pos=(-self.bar_length // 2, 350),
            )

            self.text_left = TextStim(
                win=win,
                name="label_left",
                text=self.bar_labels["left"],
                color="white",
                height=25,
                pos=(-self.bar_length // 2 - 40, 350),
            )
            self.text_right = TextStim(
                win=win,
                name="label_right",
                text=self.bar_labels["right"],
                color="white",
                height=25,
                pos=(self.bar_length // 2 + 40, 350),
            )

            self.text_right.setAutoDraw(True)
            self.text_left.setAutoDraw(True)
            self.point_bar.autoDraw = True
            self.total_reward_ind.autoDraw = True

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
        # if self.target == "reward":
        if reward > 0:
            feedback_img = "win"
        elif reward < 0:
            feedback_img = "lose"
        else:
            feedback_img = "zero"

        reward_outcome = f"+{reward:5.1f}" if reward > 0 else f"{reward:5.1f}"

        self.reward_text.setText(self.text.format(reward_outcome))

        stim_onset = logger.get_time()
        if feedback_img in self.feedback_image.keys():
            self.feedback_image[feedback_img].setAutoDraw(True)

        self.reward_text.setAutoDraw(True)

        if not self.simple:
            if self.bar_total is None:
                self._draw_total_reward(total_reward=total_reward, win=win)
            else:
                self._update_reward_bar(total_reward=total_reward)

        win.flip()
        logger.wait(win, self.duration, stim_onset)

        if feedback_img in self.feedback_image.keys():
            self.feedback_image[feedback_img].setAutoDraw(False)

        self.reward_text.setAutoDraw(False)

        if not self.simple:
            self.total_reward_ind.setAutoDraw(True)

        win.flip()

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={"total_reward": total_reward},
            reward=reward,
        )

        return None

    def _draw_total_reward(self, total_reward, win):
        total_reward_outcome = (
            f"+{total_reward:5.1f}" if total_reward > 0 else f"{total_reward:5.1f}"
        )
        reward_stage2 = "Total: " + total_reward_outcome
        self.total_reward_ind.setText(reward_stage2)
        self.total_reward_ind.setAutoDraw(False)
        self.total_reward_ind.draw()

    def _update_reward_bar(self, total_reward):
        move_bar = int((total_reward / self.bar_total) * self.bar_length)
        move_bar = min([max([move_bar, 0]), self.bar_length])
        self.total_reward_ind.setPos((-self.bar_length // 2 + move_bar, 350))
        self.total_reward_ind.setAutoDraw(True)
        self.total_reward_ind.draw()

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

        logger.wait(win=None, time=self.duration, start=stim_onset)

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={"total_reward": total_reward},
            reward=reward,
        )
