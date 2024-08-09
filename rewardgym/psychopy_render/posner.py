import os

from . import STIMPATH
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None):

    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )
    base_stim = BaseStimulus(0)

    fix = ImageStimulus(
        image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
        positions=[(0, 0)],
        duration=0.4,
        name="fixation",
    )

    fix_isi = ImageStimulus(
        image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
        positions=[(0, 0)],
        duration=0.4,
        name="isi",
    )

    def first_step(img):
        return [
            base_stim,
            fix,
            ImageStimulus(
                image_paths=[os.path.join(STIMPATH, img)],
                duration=0.5,
                positions=[(0, 0)],
                name="cue",
            ),
            fix_isi,
            ActionStimulus(
                duration=0.0,
                key_dict={"space": 0},
                timeout_action=0,
                name="dummy",
                name_timeout="dummy",
            ),
        ]

    def second_step(img2, image_shift2, to=1):
        return [
            ImageStimulus(
                duration=0.1,
                image_paths=[
                    os.path.join(STIMPATH, "posner/fix.png"),
                    os.path.join(STIMPATH, img2),
                ],
                positions=[(0, 0), (image_shift2, 0)],
                name="target",
            ),
            ImageStimulus(
                image_paths=[os.path.join(STIMPATH, "posner/fix.png")],
                positions=[(0, 0)],
                duration=0.001,
                name="fixation",
            ),
            ActionStimulus(
                duration=1.0, key_dict={"left": 0, "right": 1}, timeout_action=to
            ),
        ]

    final_step = [
        reward_feedback,
        total_reward_feedback,
        BaseStimulus(name="iti", duration=2.0),
    ]

    info_dict = {
        0: {"psychopy": []},
        1: {
            "psychopy": first_step(
                "posner/fix_left.png",
            )
        },
        2: {
            "psychopy": first_step(
                "posner/fix_right.png",
            )
        },
        3: {"psychopy": second_step("posner/target.png", image_shift2=-500, to=None)},
        4: {"psychopy": second_step("posner/target.png", image_shift2=500, to=None)},
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
    }

    return info_dict, None
