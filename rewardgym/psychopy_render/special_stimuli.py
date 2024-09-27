from typing import Dict, Union

from .stimuli import ActionStimulus, BaseStimulus

try:
    from psychopy.visual import ImageStim, TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim, ImageStim, Rect

import numpy as np

from .default_images import generate_stimulus_properties, make_card_stimulus
from .logger import ExperimentLogger


class ActionStimulusTooEarly(ActionStimulus):
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
        name_tooearly="response-too-early",
        text_tooearly={
            "text": "Don't press too early!",
            "pos": (0, -150),
            "height": 28,
            "color": "white",
        },
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

        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
        )

        self.name_tooearly = name_tooearly
        self.text_tooearly = text_tooearly

    def setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """

        self.text_stim = TextStim(win=win, **self.text_tooearly)

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

        response_window_onset = logger.get_time()
        response_window = response_window_onset + self.duration
        response_present = False
        remaining = None

        response = logger.key_strokes(win, keyList=self.key_list)

        if response:
            RTE = response[1] - response_window_onset
            logger.log_event(
                {
                    "event_type": self.name_tooearly,
                    "response_button": response[0],
                    "response_time": RTE,
                },
                onset=response_window_onset,
            )
            self.text_stim.draw()
        else:
            RTE = False

        # clearing buffer
        logger.key_strokes(win)

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

        if RTE:
            response_key = self.timeout_action
            self.text_stim.draw()
        else:
            win.flip()

        return response_key, remaining


class ConditionBasedDisplay(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        image_position=(0, 0),
        image_shift=350,
        with_action=False,
        image_map={
            1: make_card_stimulus(generate_stimulus_properties(1)),
            2: make_card_stimulus(generate_stimulus_properties(2)),
            3: make_card_stimulus(generate_stimulus_properties(3)),
            4: make_card_stimulus(generate_stimulus_properties(4)),
            5: make_card_stimulus(generate_stimulus_properties(5)),
        },
    ):
        super().__init__(name=name, duration=duration)

        self.image_position = image_position
        self.image_map = image_map
        self.image_shift = image_shift
        self.with_action = with_action

    def setup(self, win, **kwargs):
        self.image_dict = {}

        for kk in self.image_map.keys():
            if isinstance(self.image_map[kk], str):
                self.image_dict[kk] = ImageStim(win=win, image=self.image_map[kk])
            else:
                self.image_dict[kk] = ImageStim(
                    win,
                    image=self.image_map[kk],
                    size=(self.image_map[kk].shape[1], self.image_map[kk].shape[0]),
                )

    def display(self, win, logger, condition, action=None, **kwargs):
        state1 = condition[0][0] if 0 in condition[0].keys() else None
        state2 = condition[0][1] if 1 in condition[0].keys() else None

        logger.key_strokes(win)
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
            if action == 0:
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

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


class TwoStimuliWithSelection(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        positions=((0, 0), (0, 0)),
        selected=None,
        images=[
            make_card_stimulus(generate_stimulus_properties(12)),
            make_card_stimulus(generate_stimulus_properties(23)),
        ],
    ):
        super().__init__(name=name, duration=duration)

        self.positions = positions
        self.images = images
        self.selected = selected

    def setup(self, win, **kwargs):
        self.image_class = []
        for img, pos in zip(self.images, self.positions):
            if isinstance(img, str):
                self.image_class.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.image_class.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

    def display(self, win, logger, action, **kwargs):
        logger.key_strokes(win)
        stim_onset = logger.get_time()

        # Reset image positions
        for im, po in zip(self.image_class, self.positions):
            im.setPos(po)

        imgA = self.image_class[0]
        imgA.setOpacity(1.0)

        imgB = self.image_class[1]
        imgB.setOpacity(1.0)

        if action is not None:
            if action == 0:
                feedback = Rect(
                    win=win,
                    width=imgA.size[0],
                    height=imgA.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgA.pos,
                )

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

                imgA.setOpacity(0.25)

            feedback.draw()

        imgA.draw()
        imgB.draw()

        for img in self.image_class[2:]:
            img.draw()

        win.flip()

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


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
        position=(0, 0),
        name=None,
    ):
        super().__init__(name=name, duration=duration)

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

    def setup(self, win, **kwargs):
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

    def display(self, win, logger, reward, action, **kwargs):
        if self.target == "action":
            reward = action

        logger.key_strokes(win)

        stim_onset = logger.get_time()

        card = np.random.choice(self.condition_text[reward])
        display_text = self.text.format(card)
        self.textStim.setText(display_text)

        self.rectStim.autoDraw = True
        self.textStim.autoDraw = True
        win.flip()

        self.rectStim.autoDraw = False
        self.textStim.autoDraw = False

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )
