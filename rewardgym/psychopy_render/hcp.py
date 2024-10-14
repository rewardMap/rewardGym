from .default_images import fixation_cross
from .special_stimuli import TextWithBorder
from .stimuli import ActionStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None, key_dict={"left": 0, "right": 1}, **kwargs):
    reward_feedback = FeedBackStimulus(1.0, text="{0}", target="reward", name="reward")

    base_stim_iti = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=1.5,
        autodraw=True,
        name="iti",
    )

    wait_after_response = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=1.5,
        autodraw=True,
        name="delay",
    )

    info_dict = {
        0: {
            "psychopy": [
                TextWithBorder(
                    "{0}",
                    {0: ["?"]},
                    name="cue",
                    duration=0.00,
                ),
                ActionStimulus(duration=1.5, key_dict=key_dict),
            ]
        },
        1: {
            "psychopy": [
                wait_after_response,
                TextWithBorder(
                    "{0}",
                    condition_text={1: [1, 2, 3, 4], -0.5: [6, 7, 8, 9], 0: [5]},
                    name="selection",
                ),
                reward_feedback,
                base_stim_iti,
            ]
        },
        2: {
            "psychopy": [
                wait_after_response,
                TextWithBorder(
                    "{0}",
                    condition_text={-0.5: [1, 2, 3, 4], 1: [6, 7, 8, 9], 0: [5]},
                    name="selection",
                ),
                reward_feedback,
                base_stim_iti,
            ]
        },
    }

    return info_dict, None
