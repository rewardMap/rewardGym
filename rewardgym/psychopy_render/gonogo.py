from copy import deepcopy

from ..tasks import FULLPOINTS
from ..utils import check_seed
from .default_images import (
    STIMULUS_DEFAULTS,
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
    mid_stimuli,
)
from .gonogo_images import draw_robot
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


def gonogo_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_seed(random_state)
    stim_properties = []

    stim_defaults = deepcopy(stim_defaults)

    for _ in range(4):
        st_p = generate_stimulus_properties(
            random_state,
            patterns=[(2, 2), (3, 3)],
            colors=stim_defaults["colors"],
            shapes=stim_defaults["shapes"],
        )
        stim_properties.append(st_p)
        stim_defaults["colors"] = [
            i for i in stim_defaults["colors"] if i not in st_p["colors"]
        ]
        stim_defaults["shapes"] = [
            i for i in stim_defaults["shapes"] if i != st_p["shapes"]
        ]

    image_map = {}
    stimuli = {}

    for n in range(4):
        image_map[n] = make_card_stimulus(stim_properties[n], height=350, width=350)
        stimuli[n] = stim_properties[n]

    return image_map, stimuli


def gonogo_robots(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_seed(random_state)
    colors = stim_defaults["colors"][:-1]
    no_colors = len(colors)
    allow_set = colors + colors

    start_color = random_state.integers(0, no_colors)

    color_set = colors[start_color::2][:4]
    color_set = random_state.permutation(color_set)

    image_map = {}
    for n in range(4):
        image_map[n] = draw_robot(
            height=450,
            width=450,
            body_color=allow_set[n],
            second_color=allow_set[n],
            button_color="gray",
        )

    return image_map, None


def get_info_dict(seed=None, key_dict={"space": 0}, external_stimuli=None, **kwargs):
    random_state = check_seed(seed)

    if external_stimuli is None:
        image_map, stimuli = gonogo_robots(random_state)
    else:
        image_map, stimuli = external_stimuli

    reward_feedback = FeedBackStimulus(
        1.0, text="{0}", target="reward", name="reward", bar_total=FULLPOINTS["gonogo"]
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
                image_paths=[
                    mid_stimuli(
                        other_color="gray",
                        shape="circle",
                        probe=False,
                        amount="",
                        shape_dim=250,
                    )
                ],
                positions=[(0, 0)],
                name="target",
            ),
            ActionStimulus(duration=1.0, key_dict=key_dict, timeout_action=1),
        ]

    final_step = [
        BaseStimulus(duration=1.0, name="reward-delay"),
        reward_feedback,
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
