from copy import deepcopy

from ..tasks import FULLPOINTS
from ..utils import check_seed
from .default_images import (
    STIMULUS_DEFAULTS,
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)
from .special_stimuli import ConditionBasedDisplay
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def risksensitive_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_seed(random_state)

    stim_properties = []

    stim_defaults = deepcopy(stim_defaults)
    for _ in range(5):
        st_p = generate_stimulus_properties(
            random_state,
            colors=stim_defaults["colors"],
            shapes=stim_defaults["shapes"],
        )
        stim_properties.append(st_p)
        # Filtering colors used, but keeping background color (which is at -1,
        # not an ideal solution).
        stim_defaults["colors"] = [
            i
            for i in stim_defaults["colors"]
            if (i not in st_p["colors"] or i == stim_defaults["colors"][-1])
        ]
        stim_defaults["shapes"] = [
            i for i in stim_defaults["shapes"] if i != st_p["shapes"]
        ]

    image_map = {}
    stimuli = {}

    for n in range(5):
        image_map[n + 1] = make_card_stimulus(stim_properties[n])
        stimuli[n + 1] = stim_properties[n]

    return image_map, stimuli


def get_info_dict(
    seed=111, key_dict={"left": 0, "right": 1}, external_stimuli=None, **kwargs
):
    random_state = check_seed(seed)

    if external_stimuli is None:
        image_map, stimuli = risksensitive_stimuli(random_state=random_state)
    else:
        image_map, stimuli = external_stimuli

    reward_feedback = FeedBackStimulus(
        1.0,
        text="{0}",
        target="reward",
        name="reward",
        bar_total=FULLPOINTS["risk-sensitive"],
    )

    base_stim = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.1, name=None, autodraw=True
    )
    fix_iti = BaseStimulus(duration=1.5, name="iti")

    cue_disp = ConditionBasedDisplay(0.05, name="cue", image_map=image_map)
    sel_disp = ConditionBasedDisplay(
        1.5, with_action=True, name="selection", image_map=image_map
    )

    final_step = [
        sel_disp,
        ImageStimulus(
            image_paths=[fixation_cross()],
            duration=0.5,
            name="reward-delay",
            autodraw=False,
        ),
        reward_feedback,
        fix_iti,
    ]

    info_dict = {
        0: {
            "psychopy": [
                base_stim,
                cue_disp,
                ActionStimulus(duration=2.0, timeout_action=None, key_dict=key_dict),
            ]
        },
        1: {"psychopy": final_step},
        2: {"psychopy": final_step},
        3: {"psychopy": final_step},
        4: {"psychopy": final_step},
        5: {"psychopy": final_step},
    }

    return info_dict, stimuli
