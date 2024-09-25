from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, make_card_stimulus


def risksensitive_instructions():
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

    card_shape = (300, 480)

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["risk-sensitive"]["0.0"],
            letterHeight=24,
            pos=(0, 100),
        )

        part_0_0.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["risk-sensitive"]["1.0"],
            letterHeight=24,
            pos=(0, 350),
        )

        img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
        img_card = ImageStim(win=win, image=card1, pos=(-350, 0), size=card_shape)
        img_card.draw()
        img_fix.draw()
        part_1_0.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["risk-sensitive"]["2.0"],
            letterHeight=24,
            pos=(0, 350),
        )

        img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
        img_card = ImageStim(win=win, image=card1, pos=(-350, 0), size=card_shape)
        img_card2 = ImageStim(win=win, image=card2, pos=(350, 0), size=card_shape)
        img_card2.draw()
        img_card.draw()
        img_fix.draw()
        part_2_0.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["risk-sensitive"]["3.0"],
            letterHeight=24,
            pos=(0, 0),
        )
        part_3_0.draw()

    return [part_0, part_1, part_2, part_3]
