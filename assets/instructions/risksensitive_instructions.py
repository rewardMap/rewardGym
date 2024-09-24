import json

from psychopy.event import waitKeys
from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, make_card_stimulus


def risksensitive_instructions(
    win, key_map={"left": 0, "right": 1}, show_training=True
):
    fix = fixation_cross()
    card1 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["cross", "X"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((0, 125, 125), (125, 125, 0)),
        },
        height=480,
        width=300,
    )

    card2 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["X", "circle"],
            "shape_pattern": "col",
            "color_pattern": "row",
            "colors": ((125, 0, 125), (125, 125, 0)),
        },
        height=480,
        width=300,
    )

    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    instructions = instructions["risk-sensitive"]

    key_list = list(key_map.keys())

    part_0_0 = TextBox2(
        win=win,
        text=instructions["0.0"],
        letterHeight=24,
        pos=(0, 100),
    )

    part_0_0.draw()
    win.flip()
    waitKeys()

    part_1_0 = TextBox2(
        win=win,
        text=instructions["1.0"],
        letterHeight=24,
        pos=(0, 350),
    )
    part_1_0.draw()

    card_shape = (300, 480)

    img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
    img_fix.draw()

    img_card = ImageStim(win=win, image=card1, pos=(-350, 0), size=card_shape)
    img_card.draw()
    win.flip()
    waitKeys()

    part_2_0 = TextBox2(
        win=win,
        text=instructions["2.0"],
        letterHeight=24,
        pos=(0, 350),
    )
    part_2_0.draw()

    img_card2 = ImageStim(win=win, image=card2, pos=(350, 0), size=card_shape)
    img_card2.draw()
    img_card.draw()
    img_fix.draw()
    win.flip()
    waitKeys()

    part_3_0 = TextBox2(
        win=win,
        text=instructions["3.0"],
        letterHeight=24,
        pos=(0, 0),
    )
    part_3_0.draw()

    win.flip()
    waitKeys()

    return key_list
