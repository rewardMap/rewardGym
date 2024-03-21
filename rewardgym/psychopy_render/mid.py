import os

import numpy as np
from psychopy.visual import ImageStim
from psychopy.visual.rect import Rect

from . import STIMPATH
from .stimuli import ActionStim, BaseStimuli, FeedBackText, ImageStimulus, TextStimulus

reward_feedback = FeedBackText(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackText(
    1.0, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimuli(1)
fix = TextStimulus(text="isi", duration=1.5)

image_shift = 0


action_stim = ActionStim(duration=0.5, timeout_action=1)


def first_step(img, img2):
    return [
        base_stim,
        fix,
        ImageStimulus(
            duration=0.5,
            image_paths=[os.path.join(STIMPATH, img)],
            positions=[(image_shift, 0)],
        ),
        fix,
        ImageStimulus(
            duration=0.01,
            image_paths=[os.path.join(STIMPATH, img2)],
            positions=[(image_shift, 0)],
        ),
        action_stim,
    ]


final_step = [
    reward_feedback,
    total_reward_feedback,
    BaseStimuli(duration=1.5, name="iti"),
]

info_dict = {
    0: {"psychopy": first_step("F000.png", "fix.png")},
    1: {"psychopy": first_step("F001.png", "fix.png")},
    2: {"psychopy": first_step("F002.png", "fix.png")},
    3: {"psychopy": first_step("F003.png", "fix.png")},
    4: {"psychopy": first_step("F004.png", "fix.png")},
    5: {"psychopy": final_step},
    6: {"psychopy": final_step},
    7: {"psychopy": final_step},
    8: {"psychopy": final_step},
    9: {"psychopy": final_step},
}
