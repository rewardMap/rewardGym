import numpy as np
from psychopy.visual import TextStim
from psychopy.visual.rect import Rect

from .stimuli import ActionStim, BaseStimuli, FeedBackText, TextStimulus


class ShowCard(BaseStimuli):
    def __init__(
        self,
        text,
        condition_text,
        duration=1.0,
        width=200,
        height=300,
        lineWidth=2,
        lineColor="white",
        fillColor="grey",
        textColor="white",
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
        self.condition_text = condition_text

    def setup(self, win, **kwargs):

        self.textStim = TextStim(
            win=win, name=self.name + "_text", text=self.text, color=self.textColor
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

    def __call__(self, win, logger, wait, condition, **kwargs):

        logger.keyStrokes(win)

        stim_onset = logger.getTime()

        card = np.random.choice(self.condition_text[condition])
        display_text = self.text.format(card)
        self.textStim.setText(display_text)

        self.rectStim.draw()
        self.textStim.draw()
        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.logEvent(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )


reward_feedback = FeedBackText(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackText(
    1.0, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimuli(1000, name="iti")

info_dict = {
    0: {
        "psychopy": [
            base_stim,
            ShowCard("{0}", {0: ["?"], 1: ["?"], 2: ["?"]}, name="Cue"),
            ActionStim(duration=1.0),
        ]
    },
    1: {
        "psychopy": [
            ShowCard("{0}", {0: ["<"], 1: ["<"], 2: ["<"]}, name="select"),
            ShowCard(
                "{0}", {1: 5, 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]}, name="Outcome_l5"
            ),
            reward_feedback,
            total_reward_feedback,
            base_stim,
        ]
    },
    2: {
        "psychopy": [
            ShowCard("{0}", {0: [">"], 1: [">"], 2: [">"]}, name="select"),
            ShowCard(
                "{0}", {1: 5, 2: [1, 2, 3, 4], 0: [6, 7, 8, 9]}, name="Outcome_g5"
            ),
            reward_feedback,
            total_reward_feedback,
            base_stim,
        ]
    },
}
