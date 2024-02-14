import os

import numpy as np
from psychopy.visual import ImageStim
from psychopy.visual.rect import Rect

from .stimuli import ActionStim, BaseStimuli, FeedBackText, ImageStimulus, TextStimulus

STIMPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../template_stimuli/")
)


reward_feedback = FeedBackText(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackText(
    1.0, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimuli(1)
fix = TextStimulus(text="+", duration=0.2)

image_shift = 400

final_step = [base_stim, reward_feedback, total_reward_feedback]


info_dict = {
    0: {
        "psychopy": [
            base_stim,
            fix,
            ImageStimulus(
                duration=0.1,
                image_paths=[
                    os.path.join(STIMPATH, "F000.png"),
                    os.path.join(STIMPATH, "F001.png"),
                ],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
            ActionStim(duration=2.0),
        ]
    },
    1: {
        "psychopy": [
            ImageStimulus(
                duration=0.25,
                image_paths=[os.path.join(STIMPATH, "F000.png")],
                positions=[(-image_shift, 0)],
            ),
            fix,
            ImageStimulus(
                duration=0.1,
                image_paths=[
                    os.path.join(STIMPATH, "F002.png"),
                    os.path.join(STIMPATH, "F003.png"),
                ],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
            ActionStim(duration=2.0),
        ]
    },
    2: {
        "psychopy": [
            ImageStimulus(
                duration=0.25,
                image_paths=[os.path.join(STIMPATH, "F001.png")],
                positions=[(image_shift, 0)],
            ),
            fix,
            ImageStimulus(
                duration=0.1,
                image_paths=[
                    os.path.join(STIMPATH, "F004.png"),
                    os.path.join(STIMPATH, "F000.png"),
                ],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
            ActionStim(duration=2.0),
        ]
    },
    3: {"psychopy": final_step},
    4: {"psychopy": final_step},
    5: {"psychopy": final_step},
    6: {"psychopy": final_step},
}
