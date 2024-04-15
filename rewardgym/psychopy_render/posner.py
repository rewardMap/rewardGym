import os

import numpy as np
from psychopy.visual import ImageStim
from psychopy.visual.rect import Rect

from . import STIMPATH
from .stimuli import ActionStim, BaseStimulus, FeedBackText, ImageStimulus, TextStimulus

reward_feedback = FeedBackText(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackText(
    1.0, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimulus(1)
fix = ImageStimulus(
    image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
    positions=[(0, 0)],
    duration=0.4,
)
fix_isi = ImageStimulus(
    image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
    positions=[(0, 0)],
    duration=0.4,
    name="isi",
)

image_shift = 0


action_stim = ActionStim(duration=0.5, key_dict={"left": 0, "right": 1})


def first_step(img, img2, image_shift2, to=1):
    return [
        base_stim,
        fix,
        ImageStimulus(
            image_paths=[os.path.join(STIMPATH, img)], duration=0.5, positions=[(0, 0)]
        ),
        fix_isi,
        ImageStimulus(
            duration=0.1,
            image_paths=[
                os.path.join(STIMPATH, "posner/fix.png"),
                os.path.join(STIMPATH, img2),
            ],
            positions=[(0, 0), (image_shift2, 0)],
        ),
        ImageStimulus(
            image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
            positions=[(0, 0)],
            duration=0.001,
        ),
        ActionStim(duration=1.0, key_dict={"left": 0, "right": 1}, timeout_action=to),
    ]


final_step = [
    reward_feedback,
    total_reward_feedback,
    BaseStimulus(name="iti", duration=2.0),
]

info_dict = {
    0: {
        "psychopy": first_step(
            "posner/fix_left.png", "posner/target.png", image_shift2=-500, to=None
        )
    },
    1: {
        "psychopy": first_step(
            "posner/fix_left.png", "posner/target.png", image_shift2=500, to=None
        )
    },
    2: {
        "psychopy": first_step(
            "posner/fix_right.png", "posner/target.png", image_shift2=-500, to=None
        )
    },
    3: {
        "psychopy": first_step(
            "posner/fix_right.png", "posner/target.png", image_shift2=500, to=None
        )
    },
    4: {"psychopy": final_step},
    5: {"psychopy": final_step},
}
