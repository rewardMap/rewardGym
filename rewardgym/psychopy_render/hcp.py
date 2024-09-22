import importlib.util

import numpy as np

if importlib.util.find_spec("psychopy") is not None:
    from psychopy.visual import TextStim
    from psychopy.visual.rect import Rect
else:
    from .psychopy_stubs import TextStim, Rect

from .default_images import fixation_cross
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


class ShowCard(BaseStimulus):
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


def get_info_dict(seed=None, key_dict={"left": 0, "right": 1}, **kwargs):
    reward_feedback = FeedBackStimulus(1.0, text="{0}", target="reward", name="reward")

    base_stim_iti = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=1.5,
        autodraw=True,
        name="iti",
    )

    wait_after_response = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=1.5,
        autodraw=True,
        name="wait",
    )

    info_dict = {
        0: {
            "psychopy": [
                ShowCard(
                    "{0}",
                    {0: ["?"]},
                    name="response-cue",
                    duration=0.00,
                ),
                ActionStimulus(duration=1.5, key_dict=key_dict),
            ]
        },
        1: {
            "psychopy": [
                wait_after_response,
                ShowCard(
                    "{0}",
                    condition_text={1: [1, 2, 3, 4], -0.5: [6, 7, 8, 9], 0: [5]},
                    name="outcome",
                ),
                reward_feedback,
                base_stim_iti,
            ]
        },
        2: {
            "psychopy": [
                wait_after_response,
                ShowCard(
                    "{0}",
                    condition_text={-0.5: [1, 2, 3, 4], 1: [6, 7, 8, 9], 0: [5]},
                    name="outcome",
                ),
                reward_feedback,
                base_stim_iti,
            ]
        },
    }

    return info_dict, None
