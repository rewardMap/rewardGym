import os

from . import STIMPATH
from .default_images import fixation_cross
from .stimuli import (
    ActionStimulus,
    BaseStimulus,
    FeedBackStimulus,
    ImageStimulus,
    TextStimulus,
)


def get_info_dict(stimulus_set=None, **kwargs):

    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )

    fix = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.1,
        autodraw=True,
        name="initial-fixation",
    )
    fix_iti = BaseStimulus(duration=1.5, name="iti")

    image_shift = 250

    final_step = [reward_feedback, total_reward_feedback, fix_iti]

    info_dict = {
        0: {
            "psychopy": [
                fix,
                ImageStimulus(
                    duration=0.1,
                    name="decision-0",
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
                    name="environment-select",
                    image_paths=[
                        os.path.join(STIMPATH, "two_step", "stim11.png"),
                        os.path.join(STIMPATH, "two_step", "stim12.png"),
                    ],
                    positions=[(0, image_shift), (image_shift, 0)],
                ),
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
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
                    name="environment-select",
                    image_paths=[
                        os.path.join(STIMPATH, "two_step", "stim11.png"),
                        os.path.join(STIMPATH, "two_step", "stim12.png"),
                    ],
                    positions=[(-image_shift, 0), (0, image_shift)],
                ),
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
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
                    name="stimulus-select",
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
                    name="stimulus-select",
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
                    name="stimulus-select",
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
                    name="stimulus-select",
                    image_paths=[os.path.join(STIMPATH, "two_step", "stim32.png")],
                    positions=[(0, image_shift)],
                )
            ]
            + final_step
        },
    }

    return info_dict, None
