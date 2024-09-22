import json

from psychopy.event import waitKeys
from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import (
    fixation_cross,
    gonogo_probe,
    make_card_stimulus,
    win_cross,
)


def gonogo_instructions(win, key_map={"left": 0, "right": 1}):
    fix = fixation_cross()
    winning = win_cross()
    target = gonogo_probe()

    card = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["cross", "X"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((0, 125, 125), (125, 125, 0)),
        },
        height=350,
        width=350,
    )
    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    instructions = instructions["gonogo"]

    key_list = list(key_map.keys())

    part_0_0 = TextBox2(
        win=win,
        text=instructions["0.0"] + instructions["0.1"],
        letterHeight=22,
        pos=(0, 100),
    )

    part_0_0.draw()
    win.flip()
    waitKeys()

    part_1_0 = TextBox2(
        win=win,
        text=instructions["1.0"],
        letterHeight=22,
        pos=(0, 150),
    )
    part_1_0.draw()

    img_card = ImageStim(win=win, image=card, pos=(0, 0), size=card.shape[:2])
    img_card.draw()
    win.flip()
    waitKeys()

    part_2_0 = TextBox2(
        win=win,
        text=instructions["2.0"],
        letterHeight=22,
        pos=(0, 150),
    )
    part_2_0.draw()

    img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
    img_fix.draw()
    win.flip()
    waitKeys()

    part_3_0 = TextBox2(
        win=win,
        text=instructions["3.0"],
        letterHeight=22,
        pos=(0, 75),
    )
    part_3_0.draw()

    part_3_1 = TextBox2(
        win=win,
        text=instructions["3.1"],
        letterHeight=22,
        pos=(0, -75),
    )
    part_3_1.draw()

    img_fix = ImageStim(win=win, image=target, pos=(0, 0), size=target.shape[:2])
    img_fix.draw()
    win.flip()
    waitKeys()

    part_4_0 = TextBox2(
        win=win,
        text=instructions["4.0"],
        letterHeight=22,
        pos=(0, 75),
    )
    part_4_0.draw()

    part_4_1 = TextBox2(
        win=win,
        text=instructions["4.1"],
        letterHeight=22,
        pos=(0, -75),
    )
    part_4_1.draw()

    img_fix = ImageStim(win=win, image=winning, pos=(0, 0), size=winning.shape[:2])
    img_fix.draw()
    win.flip()
    waitKeys()

    part_5_0 = TextBox2(
        win=win, text=instructions["5.0"], letterHeight=22, alignment="center"
    )
    part_5_0.draw()
    win.flip()

    waitKeys()

    return key_list
