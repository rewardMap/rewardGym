import os

from . import STIMPATH
from .stimuli import (
    ActionStimulus,
    BaseStimulus,
    FeedBackStimulus,
    ImageStimulus,
    TextStimulus,
)

reward_feedback = FeedBackStimulus(
    1.0, text="You gain: {0}", target="reward", name="reward"
)
total_reward_feedback = FeedBackStimulus(
    1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
)

base_stim = BaseStimulus(0)
fix = TextStimulus(text="+", duration=0.2, name="fixation")
fix_iti = TextStimulus(text="+", duration=1.5, name="iti")

image_shift = 250

final_step = [base_stim, reward_feedback, total_reward_feedback, fix_iti]

info_dict = {
    0: {
        "psychopy": [
            base_stim,
            fix,
            ImageStimulus(
                duration=0.1,
                name="step1",
                image_paths=[
                    os.path.join(STIMPATH, "two_step", "stim11.png"),
                    os.path.join(STIMPATH, "two_step", "stim12.png"),
                ],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
            ActionStimulus(duration=2.0),
        ]
    },
    1: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="step1-select",
                image_paths=[
                    os.path.join(STIMPATH, "two_step", "stim11.png"),
                    os.path.join(STIMPATH, "two_step", "stim12.png"),
                ],
                positions=[(0, image_shift), (image_shift, 0)],
            ),
            ImageStimulus(
                duration=0.1,
                name="step21",
                image_paths=[
                    os.path.join(STIMPATH, "two_step", "stim11.png"),
                    os.path.join(STIMPATH, "two_step", "stim21.png"),
                    os.path.join(STIMPATH, "two_step", "stim22.png"),
                ],
                positions=[(0, image_shift), (-image_shift, 0), (image_shift, 0)],
            ),
            ActionStimulus(duration=2.0),
        ]
    },
    2: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="step2-select",
                image_paths=[
                    os.path.join(STIMPATH, "two_step", "stim11.png"),
                    os.path.join(STIMPATH, "two_step", "stim12.png"),
                ],
                positions=[(-image_shift, 0), (0, image_shift)],
            ),
            ImageStimulus(
                duration=0.1,
                name="step22",
                image_paths=[
                    os.path.join(STIMPATH, "two_step", "stim12.png"),
                    os.path.join(STIMPATH, "two_step", "stim31.png"),
                    os.path.join(STIMPATH, "two_step", "stim32.png"),
                ],
                positions=[(0, image_shift), (-image_shift, 0), (image_shift, 0)],
            ),
            ActionStimulus(duration=2.0),
        ]
    },
    3: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="stim21",
                image_paths=[os.path.join(STIMPATH, "two_step", "stim21.png")],
                positions=[(0, image_shift)],
            )
        ]
        + final_step
    },
    4: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="stim22",
                image_paths=[os.path.join(STIMPATH, "two_step", "stim22.png")],
                positions=[(0, image_shift)],
            )
        ]
        + final_step
    },
    5: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="stim31",
                image_paths=[os.path.join(STIMPATH, "two_step", "stim31.png")],
                positions=[(0, image_shift)],
            )
        ]
        + final_step
    },
    6: {
        "psychopy": [
            ImageStimulus(
                duration=0.5,
                name="stim32",
                image_paths=[os.path.join(STIMPATH, "two_step", "stim32.png")],
                positions=[(0, image_shift)],
            )
        ]
        + final_step
    },
}
