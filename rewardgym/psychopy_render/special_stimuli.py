from typing import Dict, List, Union

from .stimuli import ActionStimulus, BaseStimulus, ImageStimulus

try:
    from psychopy.visual import ImageStim, TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim, ImageStim, Rect

import numpy as np

from ..utils import check_seed
from .default_images import generate_stimulus_properties, make_card_stimulus
from .logger import ExperimentLogger, SimulationLogger


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

        response = self._response_handling(win, logger, response_window_onset)

        if response is not None:
            response_key, remaining = response

            if RTE:
                response_key = self.timeout_action
                self.text_stim.draw()
            else:
                win.flip()

            return response_key, remaining

        else:
            return response


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


class TwoStimuliWithResponseAndSelection(ActionStimulus):
    def __init__(
        self,
        duration: float,
        key_dict: Dict = {"left": 0, "right": 1},
        name: str = "response",
        name_phase1: str = None,
        name_phase2: str = None,
        duration_phase1: float = 0.0,
        duration_phase2: float = 0.0,
        timeout_action: int = None,
        name_timeout="response-time-out",
        positions=((0, 0), (0, 0)),
        images=[
            make_card_stimulus(generate_stimulus_properties(12)),
            make_card_stimulus(generate_stimulus_properties(23)),
        ],
        flip_probability=0.5,
        seed=111,
    ):
        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
        )

        self.images = images
        self.positions = positions
        self.name_phase1 = name_phase1
        self.name_phase2 = name_phase2
        self.duration_phase1 = duration_phase1
        self.duration_phase2 = duration_phase2
        self.flip_probability = flip_probability
        self.seed = check_seed(seed)

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

    def display(self, win, logger, **kwargs):
        if self.seed.random() < self.flip_probability:
            flip = True
            flip_key_dict = {key: 1 - value for key, value in self.key_dict.items()}

        else:
            flip_key_dict = self.key_dict
            flip = False

        self._draw_stimulus(
            win,
            logger,
            action=None,
            name=self.name_phase1,
            duration=self.duration_phase1,
            flip=flip,
        )

        logger.key_strokes(win)

        response_window_onset = logger.get_time()

        response = self._response_handling(
            win, logger, response_window_onset, key_dict=flip_key_dict
        )

        if response is not None:
            self._draw_stimulus(
                win,
                logger,
                action=response[0],
                name=self.name_phase2,
                duration=self.duration_phase2,
                flip=flip,
            )

        return response

    def simulate(
        self,
        win: Window,
        logger=SimulationLogger,
        key: str = None,
        rt: float = None,
        **kwargs,
    ):
        stim_onset = logger.get_time()

        logger.wait(win=None, time=self.duration_phase1, start=stim_onset)

        logger.log_event(
            {"event_type": self.name_phase1, "expected_duration": self.duration_phase1},
            onset=stim_onset,
        )

        response_key, remaining = self._simulate_response(logger, key, rt)

        stim_onset = logger.get_time()

        logger.wait(win=None, time=self.duration_phase2, start=stim_onset)

        logger.log_event(
            {"event_type": self.name_phase2, "expected_duration": self.duration_phase2},
            onset=stim_onset,
        )

        return response_key, remaining

    def _draw_stimulus(self, win, logger, action, name, duration, flip=False):
        stim_onset = logger.get_time()

        # Reset image positions
        for im, po in zip(self.image_class, self.positions):
            im.setPos(po)

        imgA = self.image_class[0]
        imgA.setOpacity(1.0)

        imgB = self.image_class[1]
        imgB.setOpacity(1.0)

        if flip:
            posA = imgA.pos
            posB = imgB.pos
            imgA.setPos(posB)
            imgB.setPos(posA)

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
            feedback.draw()

        elif action == 1:
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

        logger.wait(win, duration, stim_onset)

        logger.log_event(
            {"event_type": name, "expected_duration": duration, "misc": f"flip-{flip}"},
            onset=stim_onset,
        )


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


class FlipImageStimulus(ImageStimulus):
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
        seed: float = 111,
        flip_dir: str = "horiz",
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
        seed:
            Randome seed for the presentation
        """

        super().__init__(
            name=name,
            duration=duration,
            wait_no_keys=wait_no_keys,
            image_paths=image_paths,
            positions=positions,
            width=width,
            height=height,
            autodraw=autodraw,
        )

        self.rng = check_seed(seed)
        self.flip_dir = flip_dir

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

        flip = self.rng.random() < 0.5

        # So that images are drawn on top
        for ii in self.imageStims:
            ii.autoDraw = True
            if self.flip_dir == "vert":
                ii.flip = [flip, False]
            elif self.flip_dir == "horiz":
                ii.flip = [False, flip]

        win.flip()

        for ii in self.imageStims:
            ii.autoDraw = self.autodraw

        logger.wait(win, self.duration, stim_onset, self.wait_no_keys)

        logger.log_event(
            {
                "event_type": self.name + "_" + str(flip),
                "expected_duration": self.duration,
            },
            onset=stim_onset,
        )

        return None
