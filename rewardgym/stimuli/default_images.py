from itertools import permutations

import matplotlib.font_manager
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..utils import check_seed
from .create_images import draw_centered_shape, draw_shape, make_stimulus

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


def make_card_stimulus(stimulus, width=300, height=480):
    card = make_stimulus(
        width,
        height,
        num_tiles=stimulus["num_tiles"],
        shapes=stimulus["shapes"],
        colors=stimulus["colors"],
        sizes=[0.9],
        show_image=False,
        bg_color=(240, 240, 240),
        border_color="black",
        border=3,
        shape_pattern=stimulus["shape_pattern"],
        color_pattern=stimulus["color_pattern"],
        return_numpy=True,
    )

    return card


def mid_stimuli(
    amount="+5",
    shape="circle",
    shape_dim=300,
    border_width=10,
    probe=False,
    probe_color=(0, 0, 0),
    other_color=None,
):
    pattern = Image.new("RGBA", (shape_dim, shape_dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    if shape == "circle":
        stim_color = (221, 2, 211)
    elif shape == "square":
        stim_color = (255, 255, 2)
    else:
        stim_color = (1, 176, 240)

    if other_color is not None:
        stim_color = other_color

    draw_shape(draw, shape, [0, 0, shape_dim, shape_dim], probe_color, 0)

    if not probe:
        offset = 4 if shape == "triangle_u" else 0

        draw_centered_shape(
            draw,
            shape,
            [0, 0, shape_dim, shape_dim + offset],
            bbox_padding=border_width,
            color=stim_color,
            padding=0,
        )

        offset = 30 if shape == "triangle_u" else 0
        matplotlib_font = matplotlib.font_manager.findfont("arial")
        fnt = ImageFont.truetype(matplotlib_font, 70)

        draw.text(
            [150, 150 + offset],
            amount,
            align="center",
            anchor="mm",
            font=fnt,
            fill=(0, 0, 0),
        )

    pattern = np.array(pattern) / 255
    pattern = pattern[::-1, :]

    return pattern


def posner_target(target=True):
    pattern = Image.new("RGBA", (151, 151), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 150, 150], color=(0, 0, 0), padding=0)

    if target:
        draw_shape(
            draw, "neg-hbar_85_100", [0, 0, 150, 150], color=(0, 0, 0), padding=0
        )

    return np.array(pattern)[::-1, :] / 255
