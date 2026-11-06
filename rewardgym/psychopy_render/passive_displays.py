from __future__ import annotations

from typing import TYPE_CHECKING, Literal

try:
    from psychopy.visual import ImageStim, TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import ImageStim, Rect, TextStim, Window

import warnings

import numpy as np

if TYPE_CHECKING:
    from ..environments import StepContext

from ..render import PresentationRoutine, log_event
from ..stimuli import (
    generate_stimulus_properties,
    lose_cross,
    make_card_stimulus,
    win_cross,
    zero_cross,
)
from ..timing import simulation_wait, wait


class BaseStimulus(PresentationRoutine):
    """
    Base class for stimulus presentation. If called on its own it will flip the
    window.
    """

    def __init__(
        self,
        duration: float | None = None,
        name: str | None = None,
        poll_keys=True,
        rl_label=None,
        noflip=False,
        wait_no_keys=None,
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
        super().__init__(name=name, duration=duration, rl_label=rl_label, noflip=noflip)

        self.poll_keys = poll_keys

        if wait_no_keys is not None:
            warnings.warn(
                "wait_no_keys will be removed in favor of poll_keys", DeprecationWarning
            )
            self.poll_keys = not wait_no_keys

    def _setup(self, win: Window, **kwargs):
        """
        Call this to setup the stimulus. This means associating the stimulus
        with a window (so there is something to flip).

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        """
        self.is_setup = True

    def display(
        self,
        context: StepContext,
    ) -> None:
        """
        Calls the stimulus object. In this case initiate a window flip.
        Should only return something, if there has been an action required.

        Returns
        -------
        None
            Should return None

        """

        if self.duration is not None:
            stim_onset = context.logger.get_time()

            if not self.noflip:
                context.win.flip()

            wait(
                logger=context.logger,
                input_handler=context.input_handler,
                time=self.duration,
                start=stim_onset,
                poll_keys=self.poll_keys,
            )
        else:
            stim_onset = None

        log_event(self, logger=context.logger, onset=stim_onset)

    def simulate(self, context: StepContext) -> None:
        """
        Function to pretend that a stimulus has been shown. Logging and creating
        timing.

        Returns
        -------
        None
            Does not return anything, but logs the stimulus.
        """

        if self.duration is not None:
            stim_onset = context.logger.get_time()

            simulation_wait(context.logger.clock, time=self.duration, start=stim_onset)
        else:
            stim_onset = None

        log_event(self, logger=context.logger, onset=stim_onset)


class TextStimulus(BaseStimulus):
    """
    A stimulus class for text display in psychopy.
    """

    def __init__(
        self,
        duration: float,
        text: str,
        position: tuple[int, int] | None = None,
        name: str | None = None,
        text_color: str = "white",
        rl_label: str | None = None,
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

    def display(self, context: StepContext) -> None:
        """
        Calls the stimulus object. In this case drawing the text stim, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
            The logger associated with the experiment.

        Returns
        -------
        None
        Should return None

        """
        stim_onset = context.logger.get_time()
        self.textStim.draw()
        context.win.flip()

        wait(
            logger=context.logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=context.logger, onset=stim_onset)


class ImageStimulus(BaseStimulus):
    """
    A stimulus class to display (multiple) images in psychopy.
    """

    def __init__(
        self,
        duration: float,
        image_paths: list,
        positions: list | None = None,
        name: str | None = None,
        width: float | None = None,
        height: float | None = None,
        autodraw: bool = False,
        poll_keys: bool = False,
        rl_label: str | None = None,
        wait_no_keys: bool | None = None,
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
        poll_keys : str, optional
            If the logger's wait function should get key presses - only set to True if presses that are too early should be used, by default False
        """

        super().__init__(
            name=name,
            duration=duration,
            poll_keys=poll_keys,
            rl_label=rl_label,
            wait_no_keys=wait_no_keys,
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

    def display(self, context: StepContext):
        """
        Calls the stimulus object. In this case drawing the images stims, flipping the window,
        waiting and logging.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
            The logger associated with the experiment.

        Returns
        -------
        None
        Should return None
        """
        stim_onset = context.logger.get_time()

        # So that images are drawn on top
        for ii in self.imageStims:
            ii.autoDraw = True

        context.win.flip()

        for ii in self.imageStims:
            ii.autoDraw = self.autodraw

        wait(
            logger=context.logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=context.logger, onset=stim_onset)


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
        position: tuple[int, int] = (0, 125),
        name: str | None = None,
        target: Literal["reward", "total_reward"] = "reward",
        text_color: str = "white",
        font_height: float = 50,
        feedback_stim: dict | bool = True,
        simple: bool = False,
        bar_total: float | None = None,
        bar_labels: dict | None = None,
        rl_label: str | None = None,
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

        if name is None:
            name = ""

        if bar_labels is None:
            bar_labels = {"left": "0 kr", "right": "75 kr"}
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
                name=self.name + "-total_bar",
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
                name=self.name + "-total_indicator",
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

        for kk in self.feedback_stim:
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

    def display(self, context: StepContext) -> None:
        """
        Calls the stimulus object, to display the reward. Uses reward or total_reward
        depending on the target that has been defined.

        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
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
        reward = context.reward
        total_reward = context.total_reward
        win = context.win
        logger = context.logger

        if reward > 0:
            feedback_img = "win"
        elif reward < 0:
            feedback_img = "lose"
        else:
            feedback_img = "zero"

        reward_outcome = f"+{reward:5.1f}" if reward > 0 else f"{reward:5.1f}"

        self.reward_text.setText(self.text.format(reward_outcome))

        if feedback_img in self.feedback_image:
            self.feedback_image[feedback_img].setAutoDraw(True)

        self.reward_text.setAutoDraw(True)

        if not self.simple:
            if self.bar_total is None:
                self._draw_total_reward(total_reward=total_reward, win=win)
            else:
                self._update_reward_bar(total_reward=total_reward)

        stim_onset = logger.get_time()
        win.flip()
        wait(
            logger=logger,
            input_handler=context.input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        if feedback_img in self.feedback_image:
            self.feedback_image[feedback_img].setAutoDraw(False)

        self.reward_text.setAutoDraw(False)

        if not self.simple:
            self.total_reward_ind.setAutoDraw(True)

        win.flip()

        log_event(
            self,
            logger=logger,
            onset=stim_onset,
            extra_info={"total_reward": total_reward, "reward": reward},
        )

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

    def simulate(self, context: StepContext) -> None:
        """
        Function to pretend that a stimulus has been shown. Logging and creating
        timing.

        Returns
        -------
        None
            Does not return anything, but logs the stimulus.
        """
        stim_onset = context.logger.get_time()

        simulation_wait(context.logger.clock, time=self.duration, start=stim_onset)

        log_event(
            self,
            logger=context.logger,
            onset=stim_onset,
            extra_info={
                "total_reward": context.total_reward,
                "reward": context.reward,
            },
        )


class ConditionBasedDisplay(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        image_position=(0, 0),
        image_shift=350,
        with_action=False,
        image_map=None,
        rl_label: str | None = None,
    ):
        if image_map is None:
            image_map = {
                1: make_card_stimulus(generate_stimulus_properties(1)),
                2: make_card_stimulus(generate_stimulus_properties(2)),
                3: make_card_stimulus(generate_stimulus_properties(3)),
                4: make_card_stimulus(generate_stimulus_properties(4)),
                5: make_card_stimulus(generate_stimulus_properties(5)),
            }
        super().__init__(name=name, duration=duration, rl_label=rl_label)

        self.image_position = image_position
        self.image_map = image_map
        self.image_shift = image_shift
        self.with_action = with_action

    def _setup(self, win, **kwargs):
        self.image_dict = {}

        for kk in self.image_map:
            if isinstance(self.image_map[kk], str):
                self.image_dict[kk] = ImageStim(win=win, image=self.image_map[kk])
            else:
                self.image_dict[kk] = ImageStim(
                    win,
                    image=self.image_map[kk],
                    size=(self.image_map[kk].shape[1], self.image_map[kk].shape[0]),
                )

    def display(self, context: StepContext):
        condition = context.condition
        win = context.win
        logger = context.logger
        input_handler = context.input_handler

        state1 = condition[0][next(iter(condition[0].keys()))]
        state2 = condition[0][list(condition[0].keys())[1]]

        input_handler.key_strokes(logger=logger)
        stim_onset = logger.get_time()

        if state1 is not None:
            imgA = self.image_dict[state1]
            imgA.pos = (-self.image_shift, self.image_position[1])
            imgA.setOpacity(1.0)
        else:
            imgA = None

        if state2 is not None:
            imgB = self.image_dict[state2]
            imgB.pos = (self.image_shift, self.image_position[1])
            imgB.setOpacity(1.0)
        else:
            imgB = None

        if self.with_action:
            if context.previous_action == next(iter(condition[0].keys())):
                feedback = Rect(
                    win=win,
                    width=imgA.size[0],
                    height=imgA.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgA.pos,
                )

                if imgB is not None:
                    imgB.setOpacity(0.25)

            else:
                feedback = Rect(
                    win=win,
                    width=imgB.size[0],
                    height=imgB.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgB.pos,
                )

                if imgA is not None:
                    imgA.setOpacity(0.25)

            feedback.draw()

        if imgA is not None:
            imgA.draw()

        if imgB is not None:
            imgB.draw()

        win.flip()

        wait(
            logger,
            input_handler=input_handler,
            time=self.duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=logger, onset=stim_onset)


class TextWithBorder(BaseStimulus):
    def __init__(
        self,
        text,
        condition_text,
        duration=1.0,
        width=250,
        height=350,
        lineWidth=3,
        lineColor="white",
        fillColor="grey",
        textColor="white",
        target="reward",
        font_height=150,
        name=None,
        rl_label: str | None = None,
    ):
        if name is None:
            name = ""

        super().__init__(name=name, duration=duration, rl_label=rl_label)

        self.height = height
        self.width = width
        self.lineWidth = lineWidth
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.textColor = textColor
        self.text = text
        self.target = target
        self.condition_text = condition_text
        self.font_height = font_height

    def _setup(self, win, **kwargs):
        self.textStim = TextStim(
            win=win,
            name=self.name + "_text",
            text=self.text,
            color=self.textColor,
            height=self.font_height,
        )

        self.rectStim = Rect(
            win=win,
            width=self.width,
            height=self.height,
            fillColor=self.fillColor,
            lineWidth=self.lineWidth,
            lineColor=self.lineColor,
            name=self.name + "_rect",
        )

    def display(self, context: StepContext):
        reward = context.reward
        action = context.previous_action
        input_handler = context.input_handler
        logger = context.logger
        win = context.win

        if self.target == "action":
            reward = action

        input_handler.key_strokes(logger=logger)

        card = np.random.choice(self.condition_text[reward])
        display_text = self.text.format(card)
        self.textStim.setText(display_text)

        self.rectStim.autoDraw = True
        self.textStim.autoDraw = True
        stim_onset = logger.get_time()
        win.flip()

        self.rectStim.autoDraw = False
        self.textStim.autoDraw = False

        wait(
            logger,
            time=self.duration,
            start=stim_onset,
            input_handler=input_handler,
            poll_keys=self.poll_keys,
        )

        log_event(self, logger=logger, onset=stim_onset)
