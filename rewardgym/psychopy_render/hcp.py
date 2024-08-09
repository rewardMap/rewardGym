import numpy as np

try:
    from psychopy.visual import TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import TextStim, Rect

from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus


class ShowCard(BaseStimulus):
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
        target="reward",
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

    def display(self, win, logger, reward, action, **kwargs):

        if self.target == "action":
            reward = action

        logger.key_strokes(win)

        stim_onset = logger.get_time()

        card = np.random.choice(self.condition_text[reward])
        display_text = self.text.format(card)
        self.textStim.setText(display_text)

        self.rectStim.draw()
        self.textStim.draw()
        win.flip()

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )


def get_info_dict(seed=None):
    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )
    base_stim_iti = BaseStimulus(1.0, name="iti")

    info_dict = {
        0: {
            "psychopy": [
                ShowCard("{0}", {0: [""]}, name="fix", duration=1.0),
                ShowCard(
                    "{0}",
                    {0: ["?\n< or >"]},
                    name="cue",
                    duration=0.01,
                ),
                ActionStimulus(duration=1.0),
            ]
        },
        1: {
            "psychopy": [
                ShowCard(
                    "{0}",
                    condition_text={0: ["< 5"], 1: ["> 5"]},
                    name="select",
                    target="action",
                ),
                ShowCard(
                    "{0}",
                    condition_text={1: [1, 2, 3, 4], -0.5: [6, 7, 8, 9], 0: [5]},
                    name="lose",
                ),
                reward_feedback,
                total_reward_feedback,
                base_stim_iti,
            ]
        },
        2: {
            "psychopy": [
                ShowCard(
                    "{0}",
                    condition_text={0: ["< 5"], 1: ["> 5"]},
                    name="select",
                    target="action",
                ),
                ShowCard(
                    "{0}",
                    condition_text={-0.5: [1, 2, 3, 4], 1: [6, 7, 8, 9], 0: [5]},
                    name="neutral",
                ),
                reward_feedback,
                total_reward_feedback,
                base_stim_iti,
            ]
        },
    }

    return info_dict, None
