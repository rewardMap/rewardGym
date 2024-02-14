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
fix = TextStimulus(text="+", duration=0.2)

image_shift = 0


action_stim = ActionStim(duration=0.5, key_dict={"left": 0, "right": 1})


def first_step(img, img2, image_shift2, to=1):
    return [
        base_stim,
        fix,
        TextStimulus(text=img, duration=0.5),
        # ImageStimulus(duration=0.5,
        #              image_paths=[os.path.join(STIMPATH, img)],
        #              positions=[(image_shift, 0)]),
        fix,
        ImageStimulus(
            duration=0.01,
            image_paths=[os.path.join(STIMPATH, img2)],
            positions=[(image_shift2, 0)],
        ),
        ActionStim(duration=0.5, key_dict={"left": 0, "right": 1}, timeout_action=to),
    ]


final_step = [reward_feedback, total_reward_feedback, base_stim]

info_dict = {
    0: {"psychopy": first_step("<", "F000.png", image_shift2=-500, to=1)},
    1: {"psychopy": first_step("<", "F000.png", image_shift2=500, to=0)},
    2: {"psychopy": first_step(">", "F000.png", image_shift2=-500, to=1)},
    3: {"psychopy": first_step("<", "F000.png", image_shift2=500, to=0)},
    4: {"psychopy": final_step},
    5: {"psychopy": final_step},
}
