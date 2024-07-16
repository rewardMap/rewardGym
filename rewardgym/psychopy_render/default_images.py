import matplotlib.pyplot as plt

from .create_images import make_stimulus

win_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[0]])
lose_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[1]])
zero_color = tuple([int(i * 255) for i in plt.cm.Set2.colors[5]])


def fixation_cross(height=100, width=100, color=(150, 150, 150)):
    fix_cross = make_stimulus(
        height,
        width,
        1,
        ["diamond + neg-circle"],
        colors=[color],
        sizes=[1, 0.15],
        show_image=False,
        return_numpy=True,
    )

    return fix_cross


def win_cross(height=100, width=100, color=(150, 150, 150), cross_color=win_color):
    win_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + halfdiamond_u"],
        colors=[[color, cross_color]],
        sizes=[0.15, 1],
        show_image=False,
        return_numpy=True,
    )

    return win_cross


def lose_cross(height=100, width=100, color=(150, 150, 150), cross_color=lose_color):
    lose_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + halfdiamond_d"],
        colors=[[color, cross_color]],
        sizes=[0.15, 1],
        show_image=False,
        return_numpy=True,
    )

    return lose_cross


def zero_cross(height=100, width=100, color=(150, 150, 150), cross_color=zero_color):
    zero_cross = make_stimulus(
        height,
        width,
        1,
        ["circle + diamond + neg-hbar_0_25 + neg-hbar_75_100"],
        colors=[[color, cross_color, (0, 0, 0, 0), (0, 0, 0, 0)]],
        sizes=[0.15, 1, 1, 1],
        show_image=False,
        return_numpy=True,
    )

    return zero_cross
