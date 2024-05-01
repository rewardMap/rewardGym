import os

from . import STIMPATH
from .stimuli import (
    ActionStimulus,
    BaseStimulus,
    FeedBackStimulus,
    ImageStimulus,
    TextStimulus,
)

reward_feedback = FeedBackStimulus(1.0, text="You gain: {0}", target="reward")
total_reward_feedback = FeedBackStimulus(
    0.75, text="You have gained: {0}", target="total_reward"
)
base_stim = BaseStimulus(0)
fix = TextStimulus(text="+", duration=0.2)
fix_isi = TextStimulus(text="+", duration=0.2, name="isi")


def first_step(img):
    return [
        base_stim,
        fix,
        ImageStimulus(
            duration=1.0,
            image_paths=[os.path.join(STIMPATH, img)],
            positions=[(0, 0)],
        ),
        fix_isi,
        ImageStimulus(
            duration=0.001,
            image_paths=[os.path.join(STIMPATH, "gonogo/probe.png")],
            positions=[(0, 0)],
        ),
        ActionStimulus(duration=1.0, key_dict={"space": 0}, timeout_action=1),
    ]


final_step = [
    reward_feedback,
    total_reward_feedback,
    BaseStimulus(name="iti", duration=1.0),
]

info_dict = {
    0: {"psychopy": first_step("gonogo/F000.png")},
    1: {"psychopy": first_step("gonogo/F001.png")},
    2: {"psychopy": first_step("gonogo/F002.png")},
    3: {"psychopy": first_step("gonogo/F003.png")},
    4: {"psychopy": final_step},
    5: {"psychopy": final_step},
    6: {"psychopy": final_step},
    7: {"psychopy": final_step},
}
