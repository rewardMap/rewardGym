import numpy as np
from PIL import Image, ImageDraw

from .create_images import rotate_rectangle


def draw_robot(
    width=250,
    height=250,
    body_color="orange",
    second_color="orange",
    button_color="white",
):
    # Scaling factors
    scale_x = width / 250
    scale_y = height / 250

    img_size = (width + 1, height + 1)
    img = Image.new("RGBA", img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    gray = "gray"
    black = "black"
    orange = body_color

    def scale_coords(coords):
        return [
            int(coords[0] * scale_x),
            int(coords[1] * scale_y),
            int(coords[2] * scale_x),
            int(coords[3] * scale_y),
        ]

    left_arm = rotate_rectangle(
        50 * scale_x, 140 * scale_y, 45 * scale_x, 20 * scale_y, -70
    )
    right_arm = rotate_rectangle(
        200 * scale_x, 140 * scale_y, 45 * scale_x, 20 * scale_y, 70
    )
    draw.polygon(
        left_arm, fill=gray, outline=black, width=int(3 * min(scale_x, scale_y))
    )
    draw.polygon(
        right_arm, fill=gray, outline=black, width=int(3 * min(scale_x, scale_y))
    )

    left_arm = rotate_rectangle(
        65 * scale_x, 115 * scale_y, 45 * scale_x, 20 * scale_y, -45
    )
    right_arm = rotate_rectangle(
        185 * scale_x, 115 * scale_y, 45 * scale_x, 20 * scale_y, 45
    )
    draw.polygon(
        left_arm, fill=gray, outline=black, width=int(3 * min(scale_x, scale_y))
    )
    draw.polygon(
        right_arm, fill=gray, outline=black, width=int(3 * min(scale_x, scale_y))
    )

    draw.ellipse(
        scale_coords([39, 115, 39 + 25, 115 + 25]),
        outline=black,
        fill=body_color,
        width=int(3 * min(scale_x, scale_y)),
    )

    draw.ellipse(
        scale_coords([250 - 39 - 25, 115, 250 - 39, 115 + 25]),
        outline=black,
        fill=body_color,
        width=int(3 * min(scale_x, scale_y)),
    )

    # Robot body
    draw.rectangle(
        scale_coords([75, 50 - 10, 175, 180]),
        fill=gray,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )

    # Eyes
    draw.rectangle(
        scale_coords([105 - 10, 20 + 40 - 5, 120 - 10 + 5, 35 + 40]),
        fill=second_color,
        outline=black,
        width=int(2 * min(scale_x, scale_y)),
    )
    draw.rectangle(
        scale_coords([130 + 10 - 5, 20 + 40 - 5, 145 + 10, 35 + 40]),
        fill=second_color,
        outline=black,
        width=int(2 * min(scale_x, scale_y)),
    )

    # Mouth
    draw.rectangle(
        scale_coords([115, 40 + 40, 135, 45 + 45]),
        fill=second_color,
        outline=black,
        width=int(2 * min(scale_x, scale_y)),
    )

    # Antenna
    draw.rectangle(scale_coords([123, 10, 127, 20]), fill=black)
    draw.rectangle(
        scale_coords([121, 20, 129, 30]),
        fill=gray,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )
    draw.rectangle(
        scale_coords([119, 30, 131, 40]),
        fill=gray,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )

    draw.ellipse(scale_coords([120, 0, 130, 10]), fill=black)

    # Chest panel
    draw.rectangle(
        scale_coords([85, 100, 165, 170]),
        fill=orange,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )
    draw.ellipse(
        scale_coords([105, 115, 145, 155]),
        fill=button_color,
        outline=black,
        width=int(5 * min(scale_x, scale_y)),
    )

    # Legs Left
    # draw.rectangle(scale_coords([85, 200, 115, 210]), fill=black, outline=black)
    draw.rectangle(
        scale_coords([85, 180, 115, 230]),
        fill=gray,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )
    draw.rounded_rectangle(
        scale_coords([83, 195, 117, 205]), fill=black, outline=black, radius=15
    )

    # 75, 50, 175, 180
    # Legs Right
    draw.rectangle(
        scale_coords([135, 180, 165, 230]),
        fill=gray,
        outline=black,
        width=int(3 * min(scale_x, scale_y)),
    )
    draw.rounded_rectangle(
        scale_coords([133, 195, 167, 205]), fill=black, outline=black, radius=15
    )

    # Save the image
    return np.array(img)[::-1] / 255
