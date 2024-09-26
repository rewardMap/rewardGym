import numpy as np
from psychopy.visual import ImageStim, Line, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, make_card_stimulus


def twostep_instructions():
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

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.0"],
            letterHeight=24,
            pos=(0, 250),
        )

        img_card1 = ImageStim(win=win, image=card1, pos=(-325, 0), size=card1.shape[:2])
        img_card2 = ImageStim(win=win, image=card2, pos=(325, 0), size=card1.shape[:2])
        fixation = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])

        for i in [img_card1, img_card2, fixation, part_0_0]:
            i.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["1.0"],
            letterHeight=24,
            pos=(0, 250),
        )
        part_1_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["1.1"],
            letterHeight=24,
            pos=(0, -250),
        )

        fixation = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
        img_card3 = ImageStim(win=win, image=card3, pos=(-325, 0), size=card1.shape[:2])
        img_card4 = ImageStim(win=win, image=card4, pos=(325, 0), size=card1.shape[:2])

        for i in [img_card3, img_card4, fixation, part_1_0, part_1_1]:
            i.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["2.0"],
            letterHeight=24,
            pos=(0, 325),
        )

        y_offset = 75
        small_shape = np.array(card1.shape[:2]) // 2

        img_card1 = ImageStim(
            win=win, image=card1, pos=(-75, 150 + y_offset), size=small_shape
        )
        img_card2 = ImageStim(
            win=win, image=card2, pos=(75, 150 + y_offset), size=small_shape
        )

        img_card3 = ImageStim(
            win=win, image=card3, pos=(-300, -125 + y_offset), size=small_shape
        )
        img_card4 = ImageStim(
            win=win, image=card4, pos=(-150, -125 + y_offset), size=small_shape
        )

        img_card5 = ImageStim(
            win=win, image=card5, pos=(150, -125 + y_offset), size=small_shape
        )
        img_card6 = ImageStim(
            win=win, image=card6, pos=(300, -125 + y_offset), size=small_shape
        )

        line1 = Line(
            win=win,
            start=(-80, 70 + y_offset),
            end=((-450) // 2 - 5, -60 + y_offset),
            lineWidth=20,
            color=[0.25, 0.25, 0.25],
        )
        line2 = Line(
            win=win,
            start=(-70, 70 + y_offset),
            end=((450) // 2 - 5, -60 + y_offset),
            lineWidth=10,
            color=[0.25, 0.25, 0.25],
        )
        line3 = Line(
            win=win,
            start=(70, 70 + y_offset),
            end=((-450) // 2 + 5, -60 + y_offset),
            lineWidth=10,
            color=[0.25, 0.25, 0.25],
        )
        line4 = Line(
            win=win,
            start=(80, 70 + y_offset),
            end=((450) // 2 + 5, -60 + y_offset),
            lineWidth=20,
            color=[0.25, 0.25, 0.25],
        )

        part_2_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["2.1"] + instructions["two-step"]["2.2"],
            letterHeight=24,
            pos=(0, -250),
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

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["3.0"],
            letterHeight=24,
            pos=(0, 75),
        )
        part_3_0.draw()

    return [part_0, part_1, part_2, part_3]
