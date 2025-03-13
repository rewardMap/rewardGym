import numpy as np
from PIL import Image, ImageDraw


def draw_alien(version: int, width=200, height=400, body_color="green"):
    if version == 0:
        image = create_alien_one(width=width, height=height, body_color=body_color)
    elif version == 1:
        image = create_alien_two(width=width, height=height, body_color=body_color)
    elif version == 2:
        image = create_alien_three(width=width, height=height, body_color=body_color)
    elif version == 3:
        image = create_alien_four(width=width, height=height, body_color=body_color)
    else:
        raise NotImplementedError(f"Alien {version} not implemented.")

    return image[::-1, :] / 255


def create_alien_one(width, height, body_color):
    # Create a new image with a transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Define the alien's features relative to the width and height
    body_radius = min(width, height) // 3
    body_position = (width // 2, height // 2)
    eye_size = width // 3.5
    eye_position = (width // 2 - eye_size // 2, height // 2 - eye_size // 2)

    # Draw the alien's antennas with angles
    antenna_length = body_radius // 2
    antenna_positions = [
        (body_position[0] - body_radius // 2, body_position[1] - body_radius * 0.85),
        (body_position[0] + body_radius // 2, body_position[1] - body_radius * 0.85),
        (
            body_position[0] - body_radius * 1.75 // 2,
            body_position[1] - body_radius * 0.5,
        ),
        (
            body_position[0] + body_radius * 1.75 // 2,
            body_position[1] - body_radius * 0.5,
        ),
        (body_position[0], body_position[1] - body_radius),
    ]

    sign = -1.0
    for antenna_position in antenna_positions:
        sign *= -1.0
        # Draw the first segment of the antenna
        draw.line(
            [
                antenna_position,
                (
                    antenna_position[0] - sign * antenna_length // 4,
                    antenna_position[1] - antenna_length // 2,
                ),
                (
                    antenna_position[0] + sign * antenna_length // 4,
                    antenna_position[1] - antenna_length,
                ),
            ],
            fill=body_color,
            width=width // 20,
            joint="curve",
        )

    # Draw the alien's body
    draw.ellipse(
        [
            body_position[0] - body_radius,
            body_position[1] - body_radius,
            body_position[0] + body_radius,
            body_position[1] + body_radius,
        ],
        fill=body_color,
        outline="black",
        width=3,
    )

    # Draw the alien's eye
    draw.ellipse(
        [
            eye_position[0],
            eye_position[1],
            eye_position[0] + eye_size,
            eye_position[1] + eye_size,
        ],
        fill="white",
        outline="black",
        width=3,
    )

    # Draw the alien's pupil
    pupil_size = eye_size // 3
    pupil_position = (eye_position[0] + eye_size // 4, eye_position[1] + eye_size // 4)
    draw.ellipse(
        [
            pupil_position[0],
            pupil_position[1],
            pupil_position[0] + pupil_size,
            pupil_position[1] + pupil_size,
        ],
        fill="black",
    )

    # Draw the alien's mouth
    mouth_position = (width // 2 - body_radius // 4, height // 1.75 + body_radius // 4)
    draw.arc(
        [
            mouth_position[0],
            mouth_position[1],
            mouth_position[0] + body_radius // 2,
            mouth_position[1] + body_radius // 4,
        ],
        start=0,
        end=180,
        fill="black",
        width=5,
    )

    return np.array(image)


def create_alien_two(width, height, body_color):
    # Create a new image with a transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Define the alien's body as a larger central square
    body_points = [
        (0.1 * width, 0.1 * height),
        (0.9 * width, 0.1 * height),
        (0.9 * width, 0.6 * height),
        (0.1 * width, 0.6 * height),
    ]

    # Draw the alien's body
    draw.polygon(body_points, fill=body_color, outline="black", width=3)

    # Define the alien's eyes with increased size
    left_eye = [(0.2 * width, 0.2 * height), (0.4 * width, 0.4 * height)]
    right_eye = [(0.6 * width, 0.2 * height), (0.8 * width, 0.4 * height)]

    # Draw the alien's eyes
    draw.ellipse(left_eye, fill="yellow", outline="black", width=3)
    draw.ellipse(right_eye, fill="yellow", outline="black", width=3)
    # draw.ellipse(center_eye, fill='yellow', outline='black', width=3)

    # Draw the pupils
    pupil_size = 0.05 * width
    draw.ellipse(
        [
            (0.28 * width - pupil_size / 2, 0.28 * height - pupil_size / 2),
            (0.28 * width + pupil_size / 2, 0.28 * height + pupil_size / 2),
        ],
        fill="black",
    )
    draw.ellipse(
        [
            (0.72 * width - pupil_size / 2, 0.28 * height - pupil_size / 2),
            (0.72 * width + pupil_size / 2, 0.28 * height + pupil_size / 2),
        ],
        fill="black",
    )
    # draw.ellipse([(0.5 * width - pupil_size / 2, 0.38 * height - pupil_size / 2),
    #             (0.5 * width + pupil_size / 2, 0.38 * height + pupil_size / 2)], fill='black')

    # Define the alien's legs with space between the body
    leg_points = [
        (0.3 * width, 0.65 * height),
        (0.35 * width, 0.85 * height),
        (0.7 * width, 0.65 * height),
        (0.65 * width, 0.85 * height),
    ]

    # Draw the alien's legs
    draw.line([leg_points[0], leg_points[1]], fill=body_color, width=int(0.06 * width))
    draw.line([leg_points[2], leg_points[3]], fill=body_color, width=int(0.06 * width))

    return np.array(image)


def create_alien_three(width, height, body_color):
    # Create a new image with a transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Define the alien's body as two overlapping ellipses
    left_body = [(0.05 * width, 0.1 * height), (0.55 * width, 0.6 * height)]
    right_body = [(0.45 * width, 0.1 * height), (0.95 * width, 0.6 * height)]

    w_left_body = [(0.03 * width, 0.08 * height), (0.57 * width, 0.62 * height)]
    w_right_body = [(0.43 * width, 0.08 * height), (0.97 * width, 0.62 * height)]

    draw.ellipse(w_left_body, fill=body_color, outline="black", width=10)
    draw.ellipse(w_right_body, fill=body_color, outline="black", width=10)

    # Draw the alien's body
    draw.ellipse(left_body, fill=body_color)
    draw.ellipse(right_body, fill=body_color)

    # Define the alien's eyes
    left_eye = [(0.22 * width, 0.22 * height), (0.38 * width, 0.38 * height)]
    right_eye = [(0.62 * width, 0.22 * height), (0.78 * width, 0.38 * height)]

    # Draw the alien's eyes
    draw.ellipse(left_eye, fill="yellow", outline="black", width=3)
    draw.ellipse(right_eye, fill="yellow", outline="black", width=3)

    # Draw the pupils
    pupil_size = 0.05 * width
    draw.ellipse(
        [
            (0.28 * width - pupil_size / 2, 0.28 * height - pupil_size / 2),
            (0.28 * width + pupil_size / 2, 0.28 * height + pupil_size / 2),
        ],
        fill="black",
    )
    draw.ellipse(
        [
            (0.72 * width - pupil_size / 2, 0.28 * height - pupil_size / 2),
            (0.72 * width + pupil_size / 2, 0.28 * height + pupil_size / 2),
        ],
        fill="black",
    )

    # Define the alien's legs
    leg_positions = [0.2, 0.4, 0.6, 0.8]  # Positions as fractions of the width
    leg_points = []
    sign = 1

    for pos in leg_positions:
        sign *= -1
        leg_points.append((pos * width, 0.6 * height))
        leg_points.append((pos * width + width * 0.05 * sign, 0.75 * height))

    # Draw the alien's legs
    for i in range(0, len(leg_points), 2):
        draw.line(
            [leg_points[i], leg_points[i + 1]], fill=body_color, width=int(0.03 * width)
        )

    # Draw the alien's mouth
    mouth_start = (0.45 * width, 0.48 * height)
    mouth_end = (0.55 * width, 0.48 * height)
    draw.line([mouth_start, mouth_end], fill="black", width=int(0.02 * width))

    return np.array(image)


def create_alien_four(width, height, body_color):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Define the alien's body parts as proportions of the image size
    head_size = (0.6 * width, 0.5 * height)
    eye_size = (0.2 * width, 0.2 * height)
    pupil_size = (0.05 * width, 0.1 * height)
    arm_thickness = 0.05 * width

    head_size_borders = tuple([i + 10 for i in head_size])
    # Draw the head (two ellipses)
    head_top_left = ((width - head_size_borders[0]) / 2 - 2.5, 0.1 * height - 5)
    head_bottom_right = (
        head_top_left[0] + head_size_borders[0] + 5,
        head_top_left[1] + head_size_borders[1] + 5,
    )
    draw.ellipse(
        [head_top_left, head_bottom_right], fill="black", outline="black", width=5
    )

    # Legs
    draw.line(
        [(head_top_left[0] + 50, head_bottom_right[1]), (0.1 * width, 0.99 * height)],
        fill="gray",
        width=int(arm_thickness),
    )  # Right leg
    draw.line(
        [
            (head_top_left[0] + head_size[0] - 50, head_bottom_right[1]),
            (width * 0.9, 0.99 * height),
        ],
        fill="gray",
        width=int(arm_thickness),
    )  # Left leg

    # Draw the lower part of the head
    lower_head_top_left = ((width - head_size_borders[0]) / 2 - 2.5, 0.6 * height - 5)
    lower_head_bottom_right = (
        lower_head_top_left[0] + head_size_borders[0] + 5,
        lower_head_top_left[1] + 0.2 * height + 10,
    )
    draw.ellipse(
        [lower_head_top_left, lower_head_bottom_right],
        fill="black",
        outline="black",
        width=5,
    )

    # Draw the head (two ellipses)
    head_top_left = ((width - head_size[0]) / 2, 0.1 * height)
    head_bottom_right = (
        head_top_left[0] + head_size[0],
        head_top_left[1] + head_size[1],
    )
    draw.ellipse([head_top_left, head_bottom_right], fill=body_color)

    # Draw the lower part of the head
    lower_head_top_left = ((width - head_size[0]) / 2, 0.6 * height)
    lower_head_bottom_right = (
        lower_head_top_left[0] + head_size[0],
        lower_head_top_left[1] + 0.2 * height,
    )
    draw.ellipse([lower_head_top_left, lower_head_bottom_right], fill=body_color)

    # Draw the eye
    eye_top_left = (
        (width - eye_size[0]) / 2,
        (height - eye_size[1]) / 2 - 0.2 * height,
    )
    eye_bottom_right = (eye_top_left[0] + eye_size[0], eye_top_left[1] + eye_size[1])
    draw.ellipse(
        [eye_top_left, eye_bottom_right], fill="white", outline="black", width=3
    )

    # Draw the pupil
    pupil_top_left = (eye_top_left[0] + 0.1 * width, eye_top_left[1] + 0.05 * height)
    pupil_bottom_right = (
        pupil_top_left[0] + pupil_size[0],
        pupil_top_left[1] + pupil_size[1],
    )
    draw.ellipse([pupil_top_left, pupil_bottom_right], fill="black")

    # Draw the antenna
    antenna_top = (width / 2, 15)
    draw.ellipse(
        [
            (antenna_top[0] - 0.045 * width, antenna_top[1] - 0.045 * height),
            (antenna_top[0] + 0.045 * width, antenna_top[1] + 0.045 * height),
        ],
        fill=body_color,
        outline="black",
        width=3,
    )

    # Draw the smiley mouth
    mouth_top_left = (
        head_top_left[0] + 0.2 * width,
        lower_head_bottom_right[1] - 0.1 * height,
    )
    mouth_top_right = (
        head_top_left[0] + 0.4 * width,
        lower_head_bottom_right[1] - 0.1 * height,
    )
    mouth_bottom = (width / 2, lower_head_bottom_right[1] - 0.05 * height)
    draw.arc(
        [mouth_top_left, (mouth_top_right[0], mouth_bottom[1])],
        start=0,
        end=180,
        fill="black",
        width=int(0.05 * width),
    )

    return np.array(image)
