from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import (
    fixation_cross,
    gonogo_probe,
    make_card_stimulus,
    win_cross,
)


def gonogo_instructions():
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

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["0.0"] + instructions["gonogo"]["0.1"],
            letterHeight=24,
            pos=(0, 100),
        )

        part_0_0.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["1.0"],
            letterHeight=24,
            pos=(0, 150),
        )

        img_card = ImageStim(win=win, image=card, pos=(0, 0), size=(200, 200))
        img_card.draw()
        part_1_0.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["2.0"],
            letterHeight=24,
            pos=(0, 150),
        )

        img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
        img_fix.draw()
        part_2_0.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["3.0"],
            letterHeight=24,
            pos=(0, 150),
        )

        part_3_1 = TextBox2(
            win=win,
            text=instructions["gonogo"]["3.1"],
            letterHeight=24,
            pos=(0, -150),
        )

        img_fix = ImageStim(win=win, image=target, pos=(0, 0), size=target.shape[:2])
        img_fix.draw()
        part_3_0.draw()
        part_3_1.draw()

    def part_4(win, instructions):
        part_4_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["4.0"],
            letterHeight=24,
            pos=(0, 150),
        )

        img_fix = ImageStim(win=win, image=winning, pos=(0, 0), size=winning.shape[:2])
        img_fix.draw()
        part_4_0.draw()

    def part_5(win, instructions):
        part_5_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["5.0"],
            letterHeight=24,
            alignment="center",
        )
        part_5_0.draw()

    return [part_0, part_1, part_2, part_3, part_4, part_5]
