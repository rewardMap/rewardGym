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


def fixation_cross(height=100, width=100, color=(150, 150, 150)):
    pattern = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 10, 190, 190], color, 0)
    draw_shape(draw, "circle", [75, 75, 125, 125], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 80, 120, 120], (120, 0, 0), 0)

    fix_cross = np.array(pattern) / 255
    return fix_cross


def win_cross(height=100, width=100, color=(150, 150, 150), cross_color=win_color):
    pattern = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 10, 190, 190], color, 0)
    draw_shape(draw, "halfdiamond_u", [10, 10, 190, 190], win_color)
    draw_shape(draw, "circle", [75, 75, 125, 125], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 80, 120, 120], (120, 0, 0), 0)

    win_cross = np.array(pattern) / 255

    return win_cross


def lose_cross(height=100, width=100, color=(150, 150, 150), cross_color=lose_color):
    pattern = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 10, 190, 190], color, 0)
    draw_shape(draw, "halfdiamond_d", [10, 10, 190, 190], cross_color)
    draw_shape(draw, "circle", [75, 75, 125, 125], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 80, 120, 120], (120, 0, 0), 0)

    lose_cross = np.array(pattern) / 255

    return lose_cross


def zero_cross(height=100, width=100, color=(150, 150, 150), cross_color=zero_color):
    pattern = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 10, 190, 190], cross_color, 0)
    draw_shape(draw, "triangle_u", np.array([50, 10, 150, 60]), color, 0)
    draw_shape(draw, "triangle_d", np.array([50, 140, 150, 190]), color, 0)

    draw_shape(draw, "circle", [75, 75, 125, 125], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 80, 120, 120], (120, 0, 0), 0)

    zero_cross = np.array(pattern) / 255
    return zero_cross


def gonogo_probe(height=200, width=200, color=(150, 150, 150)):
    # left bottom right top
    pattern = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 0, 220, 220], (250, 250, 250), 0)

    draw_shape(draw, "diamond", [10, 10, 210, 210], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [20, 20, 200, 200], color, 0)

    draw_shape(draw, "circle", [85, 85, 135, 135], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [90, 90, 130, 130], (120, 0, 0), 0)

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


def posner_cue_up(color=(150, 150, 150)):
    pattern = Image.new("RGBA", (200, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 10, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 20, 190, 190], color, 0)

    draw_shape(draw, "circle", [75, 85, 125, 135], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 90, 120, 130], (120, 0, 0), 0)

    draw_shape(draw, "circle", [75, 170, 125, 220], (0, 0, 0), 0)
    draw_shape(draw, "circle", [80, 175, 120, 215], color, 0)

    return np.array(pattern)[::-1, :] / 255


def posner_cue_down(color=(150, 150, 150)):
    pattern = Image.new("RGBA", (200, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "diamond", [0, 10, 200, 200], (0, 0, 0), 0)
    draw_shape(draw, "diamond", [10, 20, 190, 190], color, 0)

    draw_shape(draw, "circle", [75, 85, 125, 135], (0, 0, 0), 0)
    draw_shape(draw, "neg-circle", [80, 90, 120, 130], (120, 0, 0), 0)

    draw_shape(draw, "circle", [75, 0, 125, 50], (0, 0, 0), 0)
    draw_shape(draw, "circle", [80, 5, 120, 45], color, 0)

    return np.array(pattern)[::-1, :] / 255


def posner_target():
    pattern = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    draw_shape(draw, "circle", [0, 0, 100, 100], (75, 75, 75), 0)
    draw_shape(draw, "neg-circle", [10, 10, 90, 90], (0, 0, 0, 0), 0)

    return np.array(pattern)[::-1, :] / 255
