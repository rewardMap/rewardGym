from psychopy.visual import ImageStim, TextBox2

from rewardgym.stimuli.default_images import (
    fixation_cross,
    gonogo_probe,
    lose_cross,
    make_card_stimulus,
    win_cross,
    zero_cross,
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

    nothing = zero_cross(
        width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
    )
    winning = win_cross(
        width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
    )
    lose = lose_cross(
        width=100, height=100, circle_radius_inner=10, circle_radius_outer=15
    )

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["0.0"] + instructions["gonogo"]["0.1"],
            letterHeight=28,
            pos=(0, 100),
        )

        part_0_0.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["1.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        img_card = ImageStim(win=win, image=card, pos=(0, 0), size=(200, 200))
        img_card.draw()
        part_1_0.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["2.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        img_fix = ImageStim(win=win, image=fix, pos=(0, 0), size=fix.shape[:2])
        img_fix.draw()
        part_2_0.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["3.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        img_fix = ImageStim(win=win, image=target, pos=(0, 0), size=target.shape[:2])
        img_fix.draw()
        part_3_0.draw()

    def part_4(win, instructions):
        start_pos = 280

        start_pos -= 65

        part_4_1 = TextBox2(
            win=win,
            text=instructions["gonogo"]["4.1"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 75
        img2 = ImageStim(
            win=win, image=winning, pos=(0, start_pos), size=winning.shape[:2]
        )

        start_pos -= 85

        part_4_2 = TextBox2(
            win=win,
            text=instructions["gonogo"]["4.2"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 65
        img3 = ImageStim(win=win, image=lose, pos=(0, start_pos), size=lose.shape[:2])

        start_pos -= 85
        part_4_3 = TextBox2(
            win=win,
            text=instructions["gonogo"]["4.3"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 65
        img4 = ImageStim(
            win=win, image=nothing, pos=(0, start_pos), size=nothing.shape[:2]
        )

        for ii in [part_4_1, part_4_2, part_4_3, img2, img3, img4]:
            ii.draw()

    def part_5(win, instructions):
        part_5_0 = TextBox2(
            win=win,
            text=instructions["gonogo"]["5.0"],
            letterHeight=28,
            alignment="center",
            pos=(0, 150),
        )
        part_5_0.draw()

        img_fix = ImageStim(win=win, image=target, pos=(0, -150), size=target.shape[:2])
        img_fix.draw()

    return [part_0, part_1, part_2, part_3, part_4, part_5]
