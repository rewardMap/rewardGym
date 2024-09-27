from copy import deepcopy

import numpy as np

from ..utils import check_seed
from .default_images import (
    STIMULUS_DEFAULTS,
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)
from .special_stimuli import TwoStimuliWithSelection
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def get_info_dict(seed=None, key_dict={"left": 0, "right": 1}, **kwargs):
    seed = check_seed(seed)

    stim_defaults = deepcopy(STIMULUS_DEFAULTS)
    colors = stim_defaults["colors"]
    set_colors = seed.choice(np.arange(len(colors[:-1])), 3, replace=False)

    stim_set = {}
    for n in range(3):
        stim_set[n] = []

        stimulus_properties = []
        for _ in range(2):
            st_p = generate_stimulus_properties(
                random_state=seed,
                colors=[tuple(colors[set_colors[n]])] * 4,
                patterns=[(1, 1), (2, 2)],
                shapes=stim_defaults["shapes"],
            )
            stimulus_properties.append(st_p)
            stim_defaults["shapes"] = [
                i for i in stim_defaults["shapes"] if i != st_p["shapes"]
            ]

        stim_set[n] = stimulus_properties
        stim_set[n] = [
            make_card_stimulus(stim_set[n][k], width=250, height=250) for k in range(2)
        ]

    reward_feedback = FeedBackStimulus(1.0, text="{0}", target="reward", name="reward")

    fix = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.1,
        autodraw=True,
        name="initial-fixation",
    )
    fix_iti = BaseStimulus(duration=1.0, name="iti")

    fix2 = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.5,
        autodraw=True,
        name="transition",
    )

    image_shift = 325

    final_step = [reward_feedback, fix_iti]

    info_dict = {
        0: {
            "psychopy": [
                fix,
                TwoStimuliWithSelection(
                    duration=0.1,
                    name="decision-0",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0, key_dict=key_dict),
            ]
        },
        1: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.75,
                    name="environment-select",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                fix2,
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
                    image_paths=[stim_set[1][0], stim_set[1][1]],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0, key_dict=key_dict),
            ]
        },
        2: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.75,
                    name="environment-select",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                fix2,
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
                    image_paths=[stim_set[2][0], stim_set[2][1]],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0, key_dict=key_dict),
            ]
        },
        3: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[1][0],
                        stim_set[1][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        4: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[1][0],
                        stim_set[1][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        5: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[2][0],
                        stim_set[2][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        6: {
            "psychopy": [
                TwoStimuliWithSelection(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[2][0],
                        stim_set[2][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
    }

    return info_dict, None
