from itertools import permutations

from .alien_images import draw_alien
from .default_images import (
    generate_stimulus_properties,
    make_card_stimulus,
    mid_stimuli,
    posner_target,
)
from .fixation_images import (
    fixation_cross,
    lose_cross,
    posner_cue,
    win_cross,
    zero_cross,
)
from .robot_images import draw_robot
from .spaceship_images import draw_spaceship

__all__ = [
    "draw_alien",
    "draw_robot",
    "draw_spaceship",
    "win_cross",
    "fixation_cross",
    "lose_cross",
    "zero_cross",
    "posner_cue",
    "posner_target",
    "mid_stimuli",
    "make_card_stimulus",
    "generate_stimulus_properties",
]


bg_color = (240, 240, 240)
shapes = ["square", "circle", "triangle_u", "triangle_d", "diamond"]
shapes_perm = shapes[:] + list(permutations(shapes, r=2))
patterns = [(2, 3), (4, 6), (1, 2)]

colors = [
    (1, 25, 89),
    (16, 63, 96),
    (28, 90, 98),
    (60, 109, 86),
    (104, 123, 62),
    (157, 137, 43),
    (210, 147, 67),
    (248, 161, 123),
    (253, 183, 188),
    (250, 204, 250),
] + [bg_color]  # batlow 10

STIMULUS_DEFAULTS = {"shapes": shapes_perm, "colors": colors, "patterns": patterns}
