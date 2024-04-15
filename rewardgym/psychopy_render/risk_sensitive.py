import os

from psychopy.visual import ImageStim
from psychopy.visual.rect import Rect

from . import STIMPATH
from .stimuli import ActionStim, BaseStimulus, FeedBackText


class RiskSensitiveDisplay(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        image_position=(0, 0),
        image_shift=250,
        with_action=False,
        image_map={
            0: os.path.join(STIMPATH, "risk_sensitive", "stim1.png"),
            1: os.path.join(STIMPATH, "risk_sensitive", "stim2.png"),
            2: os.path.join(STIMPATH, "risk_sensitive", "stim3.png"),
            3: os.path.join(STIMPATH, "risk_sensitive", "stim4.png"),
            4: os.path.join(STIMPATH, "risk_sensitive", "stim5.png"),
        },
    ):

        super().__init__(name=name, duration=duration)

        self.image_position = image_position
        self.image_map = image_map
        self.image_shift = image_shift
        self.condition_dict = None
        self.with_action = with_action

    def setup(self, win, action_map, **kwargs):
        self.image_dict = {}
        self.condition_dict = action_map

        for kk in self.image_map.keys():
            self.image_dict[kk] = ImageStim(win=win, image=self.image_map[kk])

    def __call__(self, win, logger, wait, condition=None, action=None, **kwargs):

        logger.keyStrokes(win)
        stim_onset = logger.getTime()

        if len(self.condition_dict[condition].keys()) == 1:
            imgA = self.image_dict[self.condition_dict[condition][0]]
            imgB = None
            imgA.pos = self.image_position
        else:
            imgA = self.image_dict[self.condition_dict[condition][0]]
            imgB = self.image_dict[self.condition_dict[condition][1]]
            imgA.pos = (-self.image_shift, self.image_position[1])
            imgB.pos = (self.image_shift, self.image_position[1])

        if self.with_action:
            if action == 0:
                feedback = Rect(
                    win=win,
                    width=imgA.size[0],
                    height=imgA.size[1],
                    lineColor="white",
                    lineWidth=5,
                    pos=imgA.pos,
                )
            else:
                feedback = Rect(
                    win=win,
                    width=imgB.size[0],
                    height=imgB.size[1],
                    lineColor="white",
                    lineWidth=5,
                    pos=imgB.pos,
                )

            feedback.draw()

        imgA.draw()

        if imgB is not None:
            imgB.draw()

        win.flip()

        wait.wait(self.duration, stim_onset)

        logger.logEvent(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


reward_feedback = FeedBackText(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackText(
    1.0, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimulus(1)

cue_disp = RiskSensitiveDisplay(0.05, name="Stimulus")
sel_disp = RiskSensitiveDisplay(0.5, with_action=True, name="StimulusSelection")

final_step = [
    sel_disp,
    reward_feedback,
    total_reward_feedback,
    base_stim,
]

info_dict = {
    0: {
        "psychopy": [
            base_stim,
            cue_disp,
            ActionStim(duration=1.0),
        ]
    },
    1: {"psychopy": final_step},
    2: {"psychopy": final_step},
    3: {"psychopy": final_step},
    4: {"psychopy": final_step},
    5: {"psychopy": final_step},
}
