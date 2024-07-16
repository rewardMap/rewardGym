from typing import List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageOps


def return_mod_pattern(pattern: str, x: int, y: int, select_list: List) -> str:
    """
    Return an element from select_list based on the pattern.

    Parameters
    ----------
    pattern : str
        The pattern type ("alternating", "row", or "col").
    x : int
        The x-coordinate of the tile.
    y : int
        The y-coordinate of the tile.
    select_list : list
        The list of elements to select from.

    Returns
    -------
    element : str
        The selected element from select_list.
    """
    n_elements = len(select_list)

    if pattern == "alternating":
        element = select_list[(x + y) % n_elements]
    elif pattern == "col":
        element = select_list[x % n_elements]
    elif pattern == "row":
        element = select_list[y % n_elements]

    return element


def draw_shape(
    draw: ImageDraw.ImageDraw,
    shape: str,
    bbox: List[int],
    color: Tuple[int, int, int],
    padding: int = 5,
    bg_color: Tuple[int, int, int] = (0, 0, 0, 0),
) -> None:
    """
    Draw a specified shape within a bounding box with optional padding.

    Parameters
    ----------
    draw : PIL.ImageDraw.ImageDraw
        The draw object to render the shape.
    shape : str
        The type of shape to draw. Options are "square", "triangle_d", "triangle_u", "circle", "diamond", "cross", "X",
        "hbar_start_end", "vbar_start_end", and "neg-shape" where `shape` is one of the previous options. The neg-shape
        uses the bg color to essentially delete previous shapes, if they are joined using "+".
    bbox : list of int
        The bounding box [left, top, right, bottom] within which the shape is drawn.
    color : tuple of int
        The RGB color of the shape.
    padding : int, optional
        The padding to apply within the bounding box. Default is 5.
    bg_color : tuple of int, optional
        The background color for negative shapes. Default is (0, 0, 0, 0).

    Returns
    -------
    None
    """

    if padding is None:
        padding = 0

    pad_bbox = [
        bbox[0] + padding,
        bbox[1] + padding,
        bbox[2] - padding,
        bbox[3] - padding,
    ]

    if shape.split("-")[0] == "neg":
        color = bg_color
        shape = shape.split("-")[1]

    cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2

    """Draw a specified shape within a bounding box."""
    if shape == "square":
        draw.rectangle(bbox, fill=color)
    elif shape == "triangle_d":
        draw.polygon(
            [(cx, bbox[3]), (bbox[0], bbox[1]), (bbox[2], bbox[1])], fill=color
        )
    elif shape == "triangle_u":
        draw.polygon(
            [(cx, bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3])], fill=color
        )
    elif shape == "circle":
        draw.ellipse(bbox, fill=color)
    elif shape == "diamond":
        draw.polygon(
            [(cx, bbox[1]), (bbox[2], cy), (cx, bbox[3]), (bbox[0], cy)], fill=color
        )
    elif shape == "halfdiamond_u":
        draw.polygon([(bbox[2], cy), (cx, bbox[3]), (bbox[0], cy)], fill=color)
    elif shape == "halfdiamond_d":
        draw.polygon([(cx, bbox[1]), (bbox[2], cy), (bbox[0], cy)], fill=color)
    elif shape == "cross":
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

    else:
        raise ValueError(f"{shape} is not in list of valid shapes.")


def add_border(image, border_size, border_color):
    """Add a border around the image."""
    return ImageOps.expand(image, border=border_size, fill=border_color)


def create_pattern(
    width: int,
    height: int,
    num_tiles: int,
    shapes: Union[str, List[str]],
    sizes: Union[int, float, List[Union[int, float]]],
    colors: List[Tuple[int, int, int]],
    bg_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
    padding: Union[int, None] = None,
    color_pattern: str = "alternating",
    shape_pattern: str = "alternating",
) -> Image.Image:
    """
    Create a repeating pattern of various shapes with specified colors.

    Parameters
    ----------
    width : int
        The width of the image.
    height : int
        The height of the image.
    num_tiles : int
        The number of tiles along the shorter dimension of the image.
    shapes : str or list of str
        The shapes to be drawn. Can be a single shape or a list of shapes. Shapes can be joined by using a "+"
    sizes : int, float or list of int, float
        The sizes of the shapes relative to the tile size. Can be a single size or a list of sizes.
    colors : list of tuple of int
        The colors to be used for the shapes.
    bg_color : tuple of int, optional
        The background color of the image. Default is transparent (0, 0, 0, 0).
    padding : int or None, optional
        The padding inside each tile. Default is None.
    color_pattern : str, optional
        The pattern for color assignment. Options are "alternating", "row", "col". Default is "alternating".
    shape_pattern : str, optional
        The pattern for shape assignment. Options are "alternating", "row", "col". Default is "alternating".

    Returns
    -------
    PIL.Image.Image
        The generated pattern image.

    Raises
    ------
    ValueError
        If `color_pattern` or `shape_pattern` is not one of the allowed values.

    Examples
    --------
    >>> pattern = create_pattern(
    ...     width=800,
    ...     height=800,
    ...     num_tiles=10,
    ...     shapes=["circle", "square"],
    ...     sizes=[0.5, 0.3],
    ...     colors=[(255, 0, 0), (0, 255, 0)],
    ...     bg_color=(255, 255, 255, 255),
    ...     padding=5,
    ...     color_pattern="row",
    ...     shape_pattern="col"
    ... )
    >>> pattern.show()
    """

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

            if not isinstance(color, list):
                color = [color] * len(sizes)

            for sh, sz, c in zip(shape.split("+"), sizes, color):
                shape_size = tile_size * sz
                bbox = [
                    int(center_x - shape_size // 2),
                    int(center_y - shape_size // 2),
                    int(center_x + shape_size // 2),
                    int(center_y + shape_size // 2),
                ]

                draw_shape(draw, sh.strip(" "), bbox, c, padding, bg_color=bg_color)

    return pattern


def make_stimulus(
    width: int,
    height: int,
    num_tiles: int,
    shapes: Union[str, List[str]],
    colors: List[Tuple[int, int, int]],
    sizes: Union[int, float, List[Union[int, float]]],
    color_pattern: str = "alternating",
    shape_pattern: str = "alternating",
    padding: Union[int, None] = None,
    border: Union[int, None] = None,
    show_image: bool = False,
    equalize: bool = False,
    border_color: str = "white",
    bg_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
    return_numpy: bool = False,
    normalize_color_space: bool = True,
) -> Union[Image.Image, np.ndarray]:
    """
    Create a stimulus image with a pattern of shapes and optional border.

    Parameters
    ----------
    width : int
        The width of the image.
    height : int
        The height of the image.
    num_tiles : int
        The number of tiles along the shorter dimension of the image.
    shapes : str or list of str
        The shapes to be drawn. Can be a single shape or a list of shapes.
    colors : list of tuple of int
        The colors to be used for the shapes.
    sizes : int, float or list of int, float
        The sizes of the shapes relative to the tile size. Can be a single size or a list of sizes.
    color_pattern : str, optional
        The pattern for color assignment. Options are "alternating", "row", "col". Default is "alternating".
    shape_pattern : str, optional
        The pattern for shape assignment. Options are "alternating", "row", "col". Default is "alternating".
    padding : int or None, optional
        The padding inside each tile. Default is None.
    border : int or None, optional
        The width of the border around the image. Default is None.
    show_image : bool, optional
        Whether to display the generated image. Default is False.
    equalize : bool, optional
        Whether to equalize the image histogram. Default is False.
    border_color : str, optional
        The color of the border. Default is "white".
    bg_color : tuple of int, optional
        The background color of the image. Default is transparent (0, 0, 0, 0).
    return_numpy : bool, optional
        Whether to return the image as a NumPy array. Default is False.

    Returns
    -------
    PIL.Image.Image or numpy.ndarray
        The generated stimulus image, either as a PIL image or a NumPy array."""

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
        if normalize_color_space:
            return np.array(pattern_image) / 255
        else:
            return np.array(pattern_image)
    else:
        return pattern_image
