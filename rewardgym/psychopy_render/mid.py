from .default_images import fixation_cross, mid_stimuli
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None):
    reward_feedback = FeedBackStimulus(1.0, text="{0}", target="reward", name="reward")
    total_reward_feedback = FeedBackStimulus(
        1.0, text="Total: {0}", target="total_reward", name="reward-total"
    )

    fix = ImageStimulus(
        image_paths=[fixation_cross()], duration=1.5, name="fixation", autodraw=False
    )

    fix_isi = ImageStimulus(
        image_paths=[fixation_cross()], duration=1.5, name="isi", autodraw=False
    )

    delay = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.5, name="delay", autodraw=False
    )

    action_stim = ActionStimulus(duration=0.35, key_dict={"space": 0}, timeout_action=1)

    def first_step(img, img2):
        return [
            fix,
            ImageStimulus(
                duration=0.5,
                image_paths=[img],
                positions=[(0, 0)],
                name="cue",
            ),
            fix_isi,
            ImageStimulus(
                duration=0.01,
                image_paths=[img2],
                positions=[(0, 0)],
                name="target",
            ),
            action_stim,
        ]

    final_step = [
        delay,
        reward_feedback,
        total_reward_feedback,
        BaseStimulus(duration=1.5, name="iti"),
    ]

    info_dict = {
        1: {
            "psychopy": first_step(
                mid_stimuli("-5", shape="square", probe=False),
                mid_stimuli("-5", shape="square", probe=True),
            )
        },  # big lose
        2: {
            "psychopy": first_step(
                mid_stimuli("-1", shape="square", probe=False),
                mid_stimuli("-1", shape="square", probe=True),
            )
        },  # small lose
        3: {
            "psychopy": first_step(
                mid_stimuli("0", shape="triangle_u", probe=False),
                mid_stimuli("0", shape="triangle_u", probe=True),
            )
        },  # control
        4: {
            "psychopy": first_step(
                mid_stimuli("+1", shape="circle", probe=False),
                mid_stimuli("+1", shape="circle", probe=True),
            )
        },  # small win
        5: {
            "psychopy": first_step(
                mid_stimuli("+5", shape="circle", probe=False),
                mid_stimuli("+5", shape="circle", probe=True),
            )
        },  # big win
        6: {"psychopy": final_step},
        7: {"psychopy": final_step},
        8: {"psychopy": final_step},
        9: {"psychopy": final_step},
        10: {"psychopy": final_step},
    }

    return info_dict, None
