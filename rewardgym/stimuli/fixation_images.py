import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from .advanced_shapes import draw_centered_shape
from .create_images import draw_shape

win_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[0]])
lose_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[1]])
zero_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[5]])


def fixation_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
    kind=None,
):
    pattern = Image.new("RGBA", (height + 1, width + 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pattern)

    center_x = width // 2
    center_y = height // 2

    draw_shape(draw, "diamond", [0, 0, height, width], (0, 0, 0), 0)
    draw_centered_shape(
        draw, "diamond", [0, 0, height, width], border_width, color=color
    )

    if kind == "win":
        draw_centered_shape(
            draw, "halfdiamond_u", [0, 0, height, width], border_width, color=win_color
        )
    elif kind == "lose":
        draw_centered_shape(
            draw, "halfdiamond_d", [0, 0, height, width], border_width, color=lose_color
        )

    draw_centered_shape(
        draw,
        "circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_outer,
        color=(0, 0, 0),
    )
    draw_centered_shape(
        draw,
        "neg-circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_inner,
        color=(120, 0, 0),
    )

    fix_cross = np.array(pattern) / 255
    return fix_cross


def win_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    win_c = fixation_cross(
        height=height,
        width=width,
        color=color,
        border_width=border_width,
        circle_radius_inner=circle_radius_inner,
        circle_radius_outer=circle_radius_outer,
        kind="win",
    )

    return win_c


def lose_cross(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
):
    lose_c = fixation_cross(
        height=height,
        width=width,
        color=color,
        border_width=border_width,
        circle_radius_inner=circle_radius_inner,
        circle_radius_outer=circle_radius_outer,
        kind="lose",
    )

    return lose_c


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
    draw_centered_shape(
        draw, "diamond", [0, 0, height, width], border_width, color=cross_color
    )

    draw_shape(
        draw,
        "triangle_u",
        np.array(
            [
                center_x - center_x // 2 - 1,
                border_width,
                center_x + center_x // 2 + 1,
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
                center_x + center_x // 2 + 1,
                center_y + center_y // 2 - border_width,
                center_x - center_x // 2 - 1,
                height - border_width,
            ]
        ),
        color,
        0,
    )

    draw_centered_shape(
        draw,
        "circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_outer,
        color=(0, 0, 0),
    )
    draw_centered_shape(
        draw,
        "neg-circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_inner,
        color=(120, 0, 0),
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
    under_shape="diamond",
    return_pattern=False,
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
        under_shape,
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
    draw_centered_shape(
        draw,
        "diamond",
        bbox=[outer_border, outer_border, width + outer_border, height + outer_border],
        bbox_padding=border_width,
        color=color,
    )

    draw_centered_shape(
        draw,
        "circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_outer,
        color=(0, 0, 0),
    )
    draw_centered_shape(
        draw,
        "neg-circle",
        bbox=[center_x, center_y, center_x, center_y],
        bbox_padding=-circle_radius_inner,
        color=(120, 0, 0),
    )

    if return_pattern:
        return pattern
    else:
        probe = np.array(pattern) / 255
        return probe


def posner_cue(
    height=150,
    width=150,
    color=(150, 150, 150),
    border_width=10,
    circle_radius_outer=20,
    circle_radius_inner=15,
    outer_border=20,
    left=True,
):
    pattern = gonogo_probe(
        height=height,
        width=width,
        color=color,
        border_width=border_width,
        circle_radius_inner=circle_radius_inner,
        circle_radius_outer=circle_radius_outer,
        outer_border=outer_border,
        under_shape="halfdiamond_u",
        return_pattern=True,
    )

    if left:
        pattern = pattern.transpose(Image.ROTATE_270)
    else:
        pattern = pattern.transpose(Image.ROTATE_90)

    return np.array(pattern) / 255
