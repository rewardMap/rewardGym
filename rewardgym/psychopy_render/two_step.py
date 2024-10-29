from copy import deepcopy

import numpy as np

from ..tasks import FULLPOINTS
from ..utils import check_seed
from .default_images import (
    STIMULUS_DEFAULTS,
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)
from .special_stimuli import TwoStimuliWithResponseAndSelection
from .stimuli import BaseStimulus, FeedBackStimulus, ImageStimulus


def twostep_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_seed(random_state)

    stim_defaults = deepcopy(stim_defaults)
    colors = stim_defaults["colors"]
    set_colors = random_state.choice(np.arange(len(colors[:-1])), 3, replace=False)

    stim_set = {}
    stim_properties = {}
    for n in range(3):
        stim_set[n] = []

        stimulus_properties = []
        for _ in range(2):
            st_p = generate_stimulus_properties(
                random_state=random_state,
                colors=[tuple(colors[set_colors[n]])] * 4,
                patterns=[(1, 1), (2, 2)],
                shapes=stim_defaults["shapes"],
            )
            stimulus_properties.append(st_p)
            stim_defaults["shapes"] = [
                i for i in stim_defaults["shapes"] if i != st_p["shapes"]
            ]

        stim_properties[n] = stimulus_properties
        stim_set[n] = [
            make_card_stimulus(stim_properties[n][k], width=250, height=250)
            for k in range(2)
        ]

    return stim_set, stim_properties


def get_info_dict(
    seed=None, key_dict={"left": 0, "right": 1}, external_stimuli=None, **kwargs
):
    seed = check_seed(seed)

    if external_stimuli is None:
        stim_set, stimuli = twostep_stimuli(seed)
    else:
        stim_set, stimuli = external_stimuli

    reward_feedback = FeedBackStimulus(
        1.0,
        text="{0}",
        target="reward",
        name="reward",
        bar_total=FULLPOINTS["two-step"],
    )

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

    def first_state(stim1, stim2, key_dict):
        tmp_list = [
            fix,
            TwoStimuliWithResponseAndSelection(
                duration=2.0,
                key_dict=key_dict,
                name_phase1="stage-1-decision",
                duration_phase1=0.1,
                name_phase2="stage-1-selection",
                duration_phase2=0.75,
                images=[stim1, stim2],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
        ]

        return tmp_list

    def second_state(s2_img1, s2_img2, key_dict):
        tmp_list = [
            fix2,
            TwoStimuliWithResponseAndSelection(
                duration=2.0,
                key_dict=key_dict,
                name_phase1="stage-2-decision",
                duration_phase1=0.1,
                name_phase2="stage-2-selection",
                duration_phase2=0.5,
                images=[s2_img1, s2_img2],
                positions=[(-image_shift, 0), (image_shift, 0)],
            ),
        ]

        return tmp_list

    info_dict = {
        0: {
            "psychopy": first_state(
                stim1=stim_set[0][0], stim2=stim_set[0][1], key_dict=key_dict
            )
        },
        1: {
            "psychopy": second_state(
                s2_img1=stim_set[1][0],
                s2_img2=stim_set[1][1],
                key_dict=key_dict,
            )
        },
        2: {
            "psychopy": second_state(
                s2_img1=stim_set[2][0],
                s2_img2=stim_set[2][1],
                key_dict=key_dict,
            )
        },
        3: {"psychopy": final_step},
        4: {"psychopy": final_step},
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
    }

    return info_dict, stimuli
