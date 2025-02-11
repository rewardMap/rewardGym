from ..tasks import FULLPOINTS
from .default_images import fixation_cross, posner_cue, posner_target
from .special_stimuli import StimuliWithResponse
from .stimuli import ActionStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None, key_dict={"left": 0, "right": 1}, **kwargs):
    reward_feedback = FeedBackStimulus(
        1.0,
        text="{0}",
        target="reward",
        name="reward",
        position=(0, 150),
        bar_total=FULLPOINTS["posner"],
    )

    fix = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.5, name="fixation", autodraw=True
    )

    fix_isi = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.4, name="isi", autodraw=False
    )

    def first_step(img):
        return [
            fix,
            ImageStimulus(
                image_paths=[img],
                duration=0.4,
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

    def second_step(img1, img2, image_shift, to=1):
        return [
            StimuliWithResponse(
                duration=2.0,
                key_dict=key_dict,
                name="response",
                target_name="target",
                target_duration=0.35,
                timeout_action=None,
                positions=((-image_shift, 0), (image_shift, 0)),
                images=[img1, img2],
                flip_probability=0.5,
                seed=seed,
            )
        ]

    final_step = [
        reward_feedback,
        ImageStimulus(
            image_paths=[fixation_cross()], duration=0.4, name="iti", autodraw=False
        ),
    ]

    info_dict = {
        0: {"psychopy": []},
        1: {"psychopy": first_step(posner_cue(left=True))},
        2: {"psychopy": first_step(posner_cue(left=False))},
        3: {
            "psychopy": second_step(
                posner_target(target=True),
                posner_target(target=False),
                image_shift=550,
                to=None,
            )
        },
        4: {
            "psychopy": second_step(
                posner_target(target=False),
                posner_target(target=True),
                image_shift=550,
                to=None,
            )
        },
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
    }

    return info_dict, None
