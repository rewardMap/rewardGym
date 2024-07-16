import numpy as np
from PIL import Image, ImageDraw, ImageOps


def draw_shape(draw, shape, bbox, color, padding=5, padding_color=(0, 255, 0)):

    if padding is None:
        padding = 0

    pad_bbox = [
        bbox[0] + padding,
        bbox[1] + padding,
        bbox[2] - padding,
        bbox[3] - padding,
    ]
    """Draw a specified shape within a bounding box."""
    if shape == "square":
        draw.rectangle(bbox, fill=color)
    elif shape == "triangle_d":
        cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        draw.polygon(
            [(cx, bbox[3]), (bbox[0], bbox[1]), (bbox[2], bbox[1])], fill=color
        )
    elif shape == "triangle_u":
        cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        draw.polygon(
            [(cx, bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3])], fill=color
        )
    elif shape == "circle":
        draw.ellipse(bbox, fill=color)
    elif shape == "diamond":
        cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        draw.polygon(
            [(cx, bbox[1]), (bbox[2], cy), (cx, bbox[3]), (bbox[0], cy)], fill=color
        )
    elif shape == "cross":
        cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        draw.line(
            [cx, bbox[1], cx, bbox[3]], fill=color, width=(bbox[2] - bbox[0]) // 4
        )
        draw.line(
            [bbox[0], cy, bbox[2], cy], fill=color, width=(bbox[3] - bbox[1]) // 4
        )
    elif shape == "X":
        draw.line(
            [bbox[0], bbox[1], bbox[2], bbox[3]],
            fill=color,
            width=(bbox[2] - bbox[0]) // 5,
        )
        draw.line(
            [bbox[0], bbox[3], bbox[2], bbox[1]],
            fill=color,
            width=(bbox[2] - bbox[0]) // 5,
        )
    elif shape.startswith("hbar"):
        _, start_pct, end_pct = shape.split("_")
        start_pct, end_pct = float(start_pct) / 100, float(end_pct) / 100
        top = pad_bbox[1] + start_pct * (pad_bbox[3] - pad_bbox[1])
        bottom = pad_bbox[1] + end_pct * (pad_bbox[3] - pad_bbox[1])
        draw.rectangle([pad_bbox[0], top, pad_bbox[2], bottom], fill=color)
    elif shape.startswith("vbar"):
        _, start_pct, end_pct = shape.split("_")
        start_pct, end_pct = float(start_pct) / 100, float(end_pct) / 100
        left = pad_bbox[0] + start_pct * (pad_bbox[2] - pad_bbox[0])
        right = pad_bbox[0] + end_pct * (pad_bbox[2] - pad_bbox[0])
        draw.rectangle([left, pad_bbox[1], right, pad_bbox[3]], fill=color)


def add_border(image, border_size, border_color):
    """Add a border around the image."""
    return ImageOps.expand(image, border=border_size, fill=border_color)


def create_pattern(
    width,
    height,
    num_tiles,
    shapes,
    sizes,
    colors,
    bg_color=(0, 0, 0, 0),
    padding=None,
    color_pattern="alternating",
    shape_pattern="alternating",
):
    def return_mod_pattern(pattern, x, y, select_list):
        n_elements = len(select_list)

        if pattern == "alternating":
            element = select_list[(x + y) % n_elements]
        elif pattern == "col":
            element = select_list[x % n_elements]
        elif pattern == "row":
            element = select_list[y % n_elements]

        return element

    pos_pattern = ["alternating", "row", "col"]

    if isinstance(sizes, int) or isinstance(sizes, float):
        sizes = [sizes]

    if isinstance(shapes, str):
        shapes = [shapes]

    max_shapes_len = max(len(shape.split("+")) for shape in shapes)
    if len(sizes) == 1:
        sizes *= max_shapes_len

    if color_pattern not in pos_pattern:
        raise ValueError(f"color_pattern should be in {pos_pattern}")
    if shape_pattern not in pos_pattern:
        raise ValueError(f"shape_pattern should be in {pos_pattern}")

    tile_size = min(width, height) // num_tiles
    num_tiles_x = width // tile_size
    num_tiles_y = height // tile_size

    pattern = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(pattern)

    for y in range(num_tiles_y):
        for x in range(num_tiles_x):

            color = return_mod_pattern(color_pattern, x, y, colors)
            shape = return_mod_pattern(shape_pattern, x, y, shapes)

            center_x = (x + 0.5) * tile_size
            center_y = (y + 0.5) * tile_size

            for sh, sz in zip(shape.split("+"), sizes):
                shape_size = tile_size * sz
                bbox = [
                    int(center_x - shape_size // 2),
                    int(center_y - shape_size // 2),
                    int(center_x + shape_size // 2),
                    int(center_y + shape_size // 2),
                ]

                draw_shape(draw, sh.strip(" "), bbox, color, padding)

    return pattern


def make_stimulus(
    width,
    height,
    num_tiles,
    shapes,
    colors,
    sizes,
    color_pattern="alternating",
    shape_pattern="alternating",
    padding=None,
    border=None,
    show_image=False,
    equalize=False,
    border_color="white",
    bg_color=(0, 0, 0, 0),
    return_numpy=False,
):

    if border is not None:
        width = width - border * 2
        height = height - border * 2

    pattern_image = create_pattern(
        width,
        height,
        num_tiles,
        shapes,
        sizes,
        colors,
        color_pattern=color_pattern,
        shape_pattern=shape_pattern,
        bg_color=bg_color,
        padding=padding,
    )

    if equalize:
        pattern_image = ImageOps.equalize(pattern_image)

    if border is not None:
        pattern_image = add_border(pattern_image, 5, border_color)

    if show_image:
        pattern_image.show()

    if return_numpy:
        return np.array(pattern_image)
    else:
        return pattern_image
