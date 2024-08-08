import os

from . import STIMPATH
from .stimuli import (
    ActionStimulus,
    BaseStimulus,
    FeedBackStimulus,
    ImageStimulus,
    TextStimulus,
)


def get_info_dict(stimulus_set=None):
    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )
    base_stim = BaseStimulus(0)
    fix_isi = TextStimulus(text="+", duration=1.5, name="isi")
    fix = TextStimulus(text="+", duration=1.5, name="fixation")

    action_stim = ActionStimulus(duration=0.25, key_dict={"space": 0}, timeout_action=1)

    def first_step(img, img2):
        return [
            base_stim,
            fix,
            ImageStimulus(
                duration=0.5,
                image_paths=[os.path.join(STIMPATH, img)],
                positions=[(0, 0)],
                name="cue",
            ),
            fix_isi,
            ImageStimulus(
                duration=0.01,
                image_paths=[os.path.join(STIMPATH, img2)],
                positions=[(0, 0)],
                name="target",
            ),
            action_stim,
        ]

    final_step = [
        reward_feedback,
        total_reward_feedback,
        BaseStimulus(duration=1.5, name="iti"),
    ]

    info_dict = {
        1: {"psychopy": first_step("mid/stim1_high.png", "mid/probe1.png")},  # big lose
        2: {
            "psychopy": first_step("mid/stim1_low.png", "mid/probe1.png")
        },  # small lose
        3: {"psychopy": first_step("mid/stim3_neut.png", "mid/probe3.png")},  # control
        4: {"psychopy": first_step("mid/stim2_low.png", "mid/probe2.png")},  # small win
        5: {"psychopy": first_step("mid/stim2_high.png", "mid/probe2.png")},  # big win
        6: {"psychopy": final_step},
        7: {"psychopy": final_step},
        8: {"psychopy": final_step},
        9: {"psychopy": final_step},
        10: {"psychopy": final_step},
    }

    return info_dict, None
