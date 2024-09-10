from itertools import permutations

import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..utils import check_seed
from .create_images import draw_shape, make_stimulus

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

STIMULUS_DEFAULTS = {"shapes": shapes_perm, "colors": colors, "patterns": patterns}


def fixation_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    pattern = Image.new("RGBA", (height + 1, width + 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = height // 2

    draw_shape(draw, "diamond", [0, 0, height, width], (0, 0, 0), 0)
    draw_shape(
        draw,
        "diamond",
        [border_width, border_width, width - border_width, height - border_width],
        color,
        0,
    )

    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )

    fix_cross = np.array(pattern) / 255
    return fix_cross


def win_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    cross_color=win_color,
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    pattern = Image.new("RGBA", (height + 1, width + 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = height // 2

    draw_shape(draw, "diamond", [0, 0, height, width], (0, 0, 0), 0)
    draw_shape(
        draw,
        "diamond",
        [border_width, border_width, width - border_width, height - border_width],
        color,
        0,
    )

    draw_shape(
        draw,
        "halfdiamond_u",
        [border_width, border_width, width - border_width, height - border_width],
        cross_color,
    )
    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )
    win_cross = np.array(pattern) / 255

    return win_cross


def lose_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    cross_color=lose_color,
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    pattern = Image.new("RGBA", (height + 1, width + 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = height // 2

    draw_shape(draw, "diamond", [0, 0, height, width], (0, 0, 0), 0)
    draw_shape(
        draw,
        "diamond",
        [border_width, border_width, width - border_width, height - border_width],
        color,
        0,
    )

    draw_shape(
        draw,
        "halfdiamond_d",
        [border_width, border_width, width - border_width, height - border_width],
        cross_color,
    )
    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )
    lose_cross = np.array(pattern) / 255

    return lose_cross


def zero_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    cross_color=zero_color,
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    pattern = Image.new("RGBA", (height + 1, width + 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = height // 2

    draw_shape(draw, "diamond", [0, 0, height, width], (0, 0, 0), 0)
    draw_shape(
        draw,
        "diamond",
        [border_width, border_width, width - border_width, height - border_width],
        cross_color,
        0,
    )

    draw_shape(
        draw,
        "triangle_u",
        np.array(
            [
                center_x - center_x // 2,
                border_width,
                center_x + center_x // 2,
                center_y - center_y // 2 + border_width,
            ]
        ),
        color,
        0,
    )
    draw_shape(
        draw,
        "triangle_d",
        np.array(
            [
                center_x + center_x // 2,
                center_y + center_y // 2 - border_width,
                center_x - center_x // 2,
                height - border_width,
            ]
        ),
        color,
        0,
    )

    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )

    zero_cross = np.array(pattern) / 255
    return zero_cross


def gonogo_probe(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
    outer_border=10,
):
    # left bottom right top
    pattern = Image.new(
        "RGBA",
        (height + outer_border * 2 + 1, width + outer_border * 2 + 1),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(pattern)

    center_x = (width + outer_border * 2) // 2
    center_y = (height + outer_border * 2) // 2

    draw_shape(
        draw,
        "diamond",
        [0, 0, height + outer_border * 2, width + outer_border * 2],
        (250, 250, 250),
        0,
    )

    draw_shape(
        draw,
        "diamond",
        [outer_border, outer_border, outer_border + height, outer_border + width],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "diamond",
        [
            border_width + outer_border,
            border_width + outer_border,
            outer_border + width - border_width,
            outer_border + height - border_width,
        ],
        color,
        0,
    )

    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )

    probe = np.array(pattern) / 255

    return probe


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


def mid_stimuli(amount="+5", shape="circle", probe=False):
    pattern = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    if shape == "circle":
        stim_color = (221, 2, 211)
    elif shape == "square":
        stim_color = (255, 255, 2)
    else:
        stim_color = (1, 176, 240)

    draw_shape(draw, shape, [0, 0, 300, 300], (0, 0, 0), 0)

    if not probe:
        offset = 4 if shape == "triangle_d" else 0

        draw_shape(draw, shape, [10, 10, 290, 290 + offset], stim_color, 0)

        offset = 30 if shape == "triangle_d" else 0
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


def posner_cue(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
    cue_outer_radius=20,
    cue_inner_width=10,
    up=True,
):
    pattern = Image.new(
        "RGBA", (width + 1, height + 2 * cue_outer_radius + 1), (0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = (height + 2 * cue_outer_radius) // 2

    draw_shape(
        draw,
        "diamond",
        [
            center_x - width // 2,
            center_y - height // 2,
            center_x + width // 2,
            center_y + width // 2,
        ],
        (0, 0, 0),
        0,
    )

    draw_shape(
        draw,
        "diamond",
        [
            center_x - width // 2 + border_width,
            center_y - height // 2 + border_width,
            center_x + width // 2 - border_width,
            center_y + width // 2 - border_width,
        ],
        color,
        0,
    )

    draw_shape(
        draw,
        "circle",
        [
            center_x - circle_radius_outer,
            center_y - circle_radius_outer,
            center_x + circle_radius_outer,
            center_y + circle_radius_outer,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "neg-circle",
        [
            center_x - circle_radius_inner,
            center_y - circle_radius_inner,
            center_x + circle_radius_inner,
            center_y + circle_radius_inner,
        ],
        (120, 0, 0),
        0,
    )

    draw_shape(
        draw,
        "circle",
        [
            center_x - cue_outer_radius,
            height - cue_outer_radius,
            center_x + cue_outer_radius,
            height + cue_outer_radius,
        ],
        (0, 0, 0),
        0,
    )
    draw_shape(
        draw,
        "circle",
        [
            center_x - cue_outer_radius + cue_inner_width,
            height - cue_outer_radius + cue_inner_width,
            center_x + cue_outer_radius - cue_inner_width,
            height + cue_outer_radius - cue_inner_width,
        ],
        color,
        0,
    )

    if up:
        return np.array(pattern)[::-1, :] / 255
    else:
        return np.array(pattern) / 255


def posner_target():
    pattern = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "circle", [0, 0, 100, 100], (75, 75, 75), 0)
    draw_shape(draw, "neg-circle", [10, 10, 90, 90], (0, 0, 0, 0), 0)

    return np.array(pattern)[::-1, :] / 255
