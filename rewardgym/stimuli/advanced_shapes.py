import math

from .default_images import draw_shape


def draw_centered_shape(draw, shape_name, bbox, bbox_padding, color, padding=0):
    padded_box = [
        bbox[0] + bbox_padding,
        bbox[1] + bbox_padding,
        bbox[2] - bbox_padding,
        bbox[3] - bbox_padding,
    ]

    draw_shape(
        draw=draw, shape=shape_name, bbox=padded_box, color=color, padding=padding
    )


def rotate_rectangle(cx, cy, w, h, angle):
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    hw, hh = w / 2, h / 2
    points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    rotated = [
        (cx + x * cos_a - y * sin_a, cy + x * sin_a + y * cos_a) for x, y in points
    ]
    return [tuple(map(int, rotated[i])) for i in range(4)]
