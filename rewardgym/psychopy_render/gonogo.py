import os

from ..utils import check_seed
from . import STIMPATH
from .default_images import (
    fixation_cross,
    generate_stimulus_properties,
    gonogo_probe,
    make_card_stimulus,
)
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None):

    random_state = check_seed(seed)
    stim_properties = [
        generate_stimulus_properties(random_state, patterns=[(2, 2), (3, 3)])
        for _ in range(4)
    ]
    image_map = {}
    stimuli = {}

    for n in range(4):
        image_map[n] = make_card_stimulus(stim_properties[n], height=350, width=350)
        stimuli[n] = stim_properties[n]

    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )

    base_stim = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.3, name="fixation", autodraw=True
    )

    fix_isi = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.3, name="isi", autodraw=False
    )

    def first_step(img):
        return [
            base_stim,
            ImageStimulus(
                duration=1.0,
                image_paths=[img],
                positions=[(0, 0)],
                name="cue",
            ),
            fix_isi,
            ImageStimulus(
                duration=0.001,
                image_paths=[gonogo_probe()],
                positions=[(0, 0)],
                name="target",
            ),
            ActionStimulus(duration=1.0, key_dict={"space": 0}, timeout_action=1),
        ]

    final_step = [
        BaseStimulus(duration=1.0, name="feedback-delay"),
        reward_feedback,
        total_reward_feedback,
        BaseStimulus(name="iti", duration=1.0),
    ]

    info_dict = {
        0: {"psychopy": []},
        1: {"psychopy": first_step(image_map[0])},
        2: {"psychopy": first_step(image_map[1])},
        3: {"psychopy": first_step(image_map[2])},
        4: {"psychopy": first_step(image_map[3])},
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
        7: {"psychopy": final_step},
        8: {"psychopy": final_step},
    }

    return info_dict, stimuli
