import json

import numpy as np
from psychopy.event import waitKeys
from psychopy.visual import ImageStim, Line, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, make_card_stimulus


def twostep_instructions(win, key_map={"left": 0, "right": 1}, show_training=True):
    fix = fixation_cross()

    card1 = make_card_stimulus(
        {
            "num_tiles": (1, 1),
            "shapes": ["cross"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((200, 0, 0), (200, 0, 0)),
        },
        height=250,
        width=250,
    )

    card2 = make_card_stimulus(
        {
            "num_tiles": (1, 1),
            "shapes": ["X"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((200, 0, 0), (200, 0, 0)),
        },
        height=250,
        width=250,
    )

    card3 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["circle"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((0, 0, 200), (0, 0, 200)),
        },
        height=250,
        width=250,
    )
    card4 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["diamond"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((0, 0, 200), (0, 0, 200)),
        },
        height=250,
        width=250,
    )
    card5 = make_card_stimulus(
        {
            "num_tiles": (1, 1),
            "shapes": ["triangle_u"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((200, 200, 0), (200, 200, 0)),
        },
        height=250,
        width=250,
    )
    card6 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["diamond", "circle"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((200, 200, 0), (200, 200, 0)),
        },
        height=250,
        width=250,
    )
    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    instructions = instructions["two-step"]

    key_list = list(key_map.keys())

    part_0_0 = TextBox2(
        win=win,
        text=instructions["0.0"],
        letterHeight=22,
        pos=(0, 100),
    )

    img_card1 = ImageStim(win=win, image=card1, pos=(-325, 0), size=card1.shape[:2])
    img_card2 = ImageStim(win=win, image=card2, pos=(325, 0), size=card1.shape[:2])
    fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])

    for i in [img_card1, img_card2, fix, part_0_0]:
        i.draw()

    win.flip()
    waitKeys()

    part_1_0 = TextBox2(
        win=win,
        text=instructions["1.0"],
        letterHeight=22,
        pos=(0, 150),
    )
    part_1_1 = TextBox2(
        win=win,
        text=instructions["1.1"],
        letterHeight=22,
        pos=(0, -150),
    )

    img_card3 = ImageStim(win=win, image=card3, pos=(-325, 0), size=card1.shape[:2])
    img_card4 = ImageStim(win=win, image=card4, pos=(325, 0), size=card1.shape[:2])

    for i in [img_card3, img_card4, fix, part_1_0, part_1_1]:
        i.draw()

    win.flip()
    waitKeys()

    part_2_0 = TextBox2(
        win=win,
        text=instructions["2.0"],
        letterHeight=22,
        pos=(0, 250),
    )

    small_shape = np.array(card1.shape[:2]) // 2

    img_card1 = ImageStim(win=win, image=card1, pos=(-75, 150), size=small_shape)
    img_card2 = ImageStim(win=win, image=card2, pos=(75, 150), size=small_shape)

    img_card3 = ImageStim(win=win, image=card3, pos=(-300, -125), size=small_shape)
    img_card4 = ImageStim(win=win, image=card4, pos=(-150, -125), size=small_shape)

    img_card5 = ImageStim(win=win, image=card5, pos=(150, -125), size=small_shape)
    img_card6 = ImageStim(win=win, image=card6, pos=(300, -125), size=small_shape)

    line1 = Line(
        win=win,
        start=(-80, 70),
        end=((-450) // 2 - 5, -60),
        lineWidth=20,
        color=[0.25, 0.25, 0.25],
    )
    line2 = Line(
        win=win,
        start=(-70, 70),
        end=((450) // 2 - 5, -60),
        lineWidth=10,
        color=[0.25, 0.25, 0.25],
    )
    line3 = Line(
        win=win,
        start=(70, 70),
        end=((-450) // 2 + 5, -60),
        lineWidth=10,
        color=[0.25, 0.25, 0.25],
    )
    line4 = Line(
        win=win,
        start=(80, 70),
        end=((450) // 2 + 5, -60),
        lineWidth=20,
        color=[0.25, 0.25, 0.25],
    )

    part_2_1 = TextBox2(
        win=win,
        text=instructions["2.1"] + instructions["2.2"],
        letterHeight=22,
        pos=(0, -100),
    )

    for i in [
        line1,
        line2,
        line3,
        line4,
        img_card1,
        img_card2,
        img_card3,
        img_card4,
        img_card5,
        img_card6,
        part_2_0,
        part_2_1,
    ]:
        i.draw()

    win.flip()
    waitKeys()

    if show_training:
        part_3_0 = TextBox2(
            win=win,
            text=instructions["3.0"],
            letterHeight=22,
            pos=(0, 75),
        )
        part_3_0.draw()
        win.flip()
        waitKeys()

    return key_list
