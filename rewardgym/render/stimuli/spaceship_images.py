import numpy as np
from PIL import Image, ImageDraw


def draw_spaceship(version=1, width=400, height=400, body_color="blue"):
    if version == 0:
        img = draw_spaceship_one(width=width, height=height, body_color=body_color)
    elif version == 1:
        img = draw_spaceship_two(width=width, height=height, body_color=body_color)
    else:
        raise NotImplementedError(f"Alien {version} not implemented.")

    return img[::-1, :] / 255


def draw_spaceship_one(
    width=400, height=400, body_color="gray", border_color="black", border_width=5
):
    # Create an image with a black background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define proportions
    center_x = width // 2
    center_y = height // 2
    size_factor = min(width, height) / 250

    # Draw the spaceship body (a rounded oval shape) with border
    body_top = (center_x - 50 * size_factor, center_y - 100 * size_factor)
    body_bottom = (center_x + 50 * size_factor, center_y + 50 * size_factor)
    draw.ellipse(
        [body_top, body_bottom],
        fill=body_color,
        outline=border_color,
        width=border_width,
    )

    # Draw the spaceship windows (a small circle) with border
    window_top = (center_x - 15 * size_factor, center_y - 70 * size_factor)
    window_bottom = (center_x + 15 * size_factor, center_y - 40 * size_factor)
    draw.ellipse(
        [window_top, window_bottom],
        fill="white",
        outline=border_color,
        width=border_width,
    )

    # Draw the spaceship wings (two rounded wings) with border
    left_wing_top = (center_x - 80 * size_factor, center_y - 20 * size_factor)
    left_wing_bottom = (center_x - 30 * size_factor, center_y + 40 * size_factor)
    right_wing_top = (center_x + 30 * size_factor, center_y - 20 * size_factor)
    right_wing_bottom = (center_x + 80 * size_factor, center_y + 40 * size_factor)
    draw.ellipse(
        [left_wing_top, left_wing_bottom],
        fill="darkgray",
        outline=border_color,
        width=border_width,
    )
    draw.ellipse(
        [right_wing_top, right_wing_bottom],
        fill="darkgray",
        outline=border_color,
        width=border_width,
    )

    # Draw the central thruster as an inverted trapezoid
    thruster_points = [
        (center_x - 10 * size_factor, center_y + 50 * size_factor),  # Top-left
        (center_x + 10 * size_factor, center_y + 50 * size_factor),  # Top-right
        (center_x + 20 * size_factor, center_y + 80 * size_factor),  # Bottom-right
        (center_x - 20 * size_factor, center_y + 80 * size_factor),  # Bottom-left
    ]
    draw.polygon(
        thruster_points, fill="darkgray", outline=border_color, width=border_width
    )

    # Draw the thruster flame as an ellipse below the thruster
    flame_top = (center_x - 15 * size_factor, center_y + 80 * size_factor)
    flame_bottom = (center_x + 15 * size_factor, center_y + 120 * size_factor)
    draw.ellipse([flame_top, flame_bottom], fill="red")

    return np.array(img)


def draw_spaceship_two(width=400, height=400, body_color="blue"):
    # Create an image with a black background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define proportions
    center_x = width // 2
    center_y = height // 2
    size_factor = min(width, height) / 375

    # Draw the rectangular body (more rocket-like)
    body_width = 100 * size_factor
    body_height = 200 * size_factor
    # Draw the triangular top
    top_triangle = [
        (center_x, center_y - body_height // 2 - 50 * size_factor),
        (center_x - body_width // 2, center_y - body_height // 2 + 15),
        (center_x + body_width // 2, center_y - body_height // 2 + 15),
    ]
    draw.polygon(top_triangle, fill="darkgray", outline="black", width=4)

    # Draw the wings
    wing_size = 60 * size_factor
    left_wing = [
        (center_x - body_width // 2 + 10, center_y - 20),
        (center_x - body_width // 2 - wing_size, center_y + body_height // 2),
        (center_x - body_width // 2 + 10, center_y + body_height // 2 - 10),
    ]
    right_wing = [
        (center_x + body_width // 2 - 10, center_y - 20),
        (center_x + body_width // 2 + wing_size, center_y + body_height // 2),
        (center_x + body_width // 2 - 10, center_y + body_height // 2 - 10),
    ]
    draw.polygon(left_wing, fill="darkgray", outline="black", width=4)
    draw.polygon(right_wing, fill="darkgray", outline="black", width=4)

    # Draw the thruster exhaust as a trapezoid
    thruster_top_left = (center_x - 20 * size_factor, center_y + body_height // 2 - 15)
    thruster_top_right = (center_x + 20 * size_factor, center_y + body_height // 2 - 15)
    thruster_bottom_left = (
        center_x - 40 * size_factor,
        center_y + body_height // 2 + 40 * size_factor,
    )
    thruster_bottom_right = (
        center_x + 40 * size_factor,
        center_y + body_height // 2 + 40 * size_factor,
    )
    thruster_points = [
        thruster_top_left,
        thruster_top_right,
        thruster_bottom_right,
        thruster_bottom_left,
    ]
    draw.polygon(thruster_points, fill="darkgray", outline="black", width=4)

    # Draw the rectangular body (more rocket-like)
    body_top_left = (center_x - body_width // 2, center_y - body_height // 2)
    body_bottom_right = (center_x + body_width // 2, center_y + body_height // 2)
    draw.rounded_rectangle(
        [body_top_left, body_bottom_right],
        fill="darkgray",
        outline="black",
        width=4,
        radius=20,
    )

    body_top_left = (center_x - body_width // 2 + 12, center_y - body_height // 2 + 12)
    body_bottom_right = (
        center_x + body_width // 2 - 12,
        center_y + body_height // 2 - 12,
    )
    draw.rounded_rectangle(
        [body_top_left, body_bottom_right],
        fill=body_color,
        outline="black",
        width=2,
        radius=25,
    )

    # Draw windows
    window_size = 30 * size_factor

    full_height = body_top_left[1]

    for n in [1, 3, 5]:
        top_window_top_left = (
            center_x - window_size // 2,
            full_height + n * window_size - window_size // 2,
        )
        top_window_bottom_right = (
            center_x + window_size // 2,
            full_height + n * window_size + window_size // 2,
        )
        draw.ellipse(
            [top_window_top_left, top_window_bottom_right],
            fill="white",
            outline="black",
            width=4,
        )

    plume_top_left = (
        center_x - 30 * size_factor,
        center_y + body_height // 2 + 40 * size_factor,
    )
    plume_bottom_right = (
        center_x + 30 * size_factor,
        center_y + body_height // 2 + 80 * size_factor,
    )
    draw.ellipse([plume_top_left, plume_bottom_right], fill="orange")

    return np.array(img)
