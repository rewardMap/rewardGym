from itertools import permutations

import matplotlib.pyplot as plt
import numpy as np

from ..utils import check_seed
from .create_images import make_stimulus

win_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[0]])
lose_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[1]])
zero_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[5]])

bg_color = (240, 240, 240)
shapes = ["square", "circle", "triangle_u", "triangle_d", "diamond", "X", "cross"]
shapes_perm = shapes[:] + list(permutations(shapes, r=2))
patterns = [(2, 3), (4, 6)]
colors = [tuple([int(i * 255) for i in c]) for c in plt.cm.tab10.colors[:5]] + [
    bg_color
]


def fixation_cross(height=100, width=100, color=(150, 150, 150)):
    fix_cross = make_stimulus(
        height,
        width,
        1,
        ["diamond + neg-circle"],
        colors=[color],
        sizes=[1, 0.15],
        show_image=False,
        return_numpy=True,
    )

    return fix_cross


def win_cross(height=100, width=100, color=(150, 150, 150), cross_color=win_color):
    win_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + halfdiamond_u"],
        colors=[[color, cross_color]],
        sizes=[0.15, 1],
        show_image=False,
        return_numpy=True,
    )

    return win_cross


def lose_cross(height=100, width=100, color=(150, 150, 150), cross_color=lose_color):
    lose_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + halfdiamond_d"],
        colors=[[color, cross_color]],
        sizes=[0.15, 1],
        show_image=False,
        return_numpy=True,
    )

    return lose_cross


def zero_cross(height=100, width=100, color=(150, 150, 150), cross_color=zero_color):
    zero_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + diamond + neg-hbar_0_25 + neg-hbar_75_100"],
        colors=[[color, cross_color, (0, 0, 0, 0), (0, 0, 0, 0)]],
        sizes=[0.15, 1, 1, 1],
        show_image=False,
        return_numpy=True,
    )

    return zero_cross


def generate_stimulus_properties(
    random_state,
    colors=colors,
    shapes=shapes_perm,
    patterns=patterns,
    bg_color=bg_color,
):

    random_state = check_seed(random_state)

    gen_colors = colors[:]
    stim_shape = shapes[
        random_state.choice(np.arange(len(shapes)), 1).astype(int).item()
    ]

    stim_pattern = patterns[
        random_state.choice(np.arange(len(patterns)), 1).astype(int).item()
    ]

    pattern = ["alternating", "row", "col"]
    c_pattern = pattern[random_state.choice(np.arange(3), 1).astype(int).item()]
    s_pattern = pattern[random_state.choice(np.arange(3), 1).astype(int).item()]
    n_colors = random_state.choice([1, 2], 1).astype(int).item()
    if stim_shape == "square":
        n_colors = 2

    stim_colors = []

    for _ in range(n_colors):
        stim_colors.append(
            gen_colors.pop(
                random_state.choice(np.arange(len(gen_colors)), 1).astype(int).item()
            )
        )

    if len(stim_colors) == 1 and stim_colors[0] == bg_color:
        stim_colors.append(
            gen_colors.pop(
                random_state.choice(np.arange(len(gen_colors)), 1).astype(int).item()
            )
        )

    stimulus = {
        "num_tiles": stim_pattern,
        "colors": stim_colors,
        "shapes": stim_shape,
        "color_pattern": c_pattern,
        "shape_pattern": s_pattern,
    }

    return stimulus


def make_card_stimulus(stimulus):

    card = make_stimulus(
        320,
        480,
        num_tiles=stimulus["num_tiles"],
        shapes=stimulus["shapes"],
        colors=stimulus["colors"],
        sizes=[0.9],
        show_image=False,
        bg_color=(240, 240, 240),
        border_color="white",
        border=5,
        shape_pattern=stimulus["shape_pattern"],
        color_pattern=stimulus["color_pattern"],
        return_numpy=True,
    )

    return card
