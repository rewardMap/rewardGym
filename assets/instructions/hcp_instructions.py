from psychopy.visual import ImageStim, Rect, TextBox2, TextStim

from rewardgym.psychopy_render.default_images import lose_cross, win_cross, zero_cross


def hcp_instructions():
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
            text=instructions["hcp"]["0.0"],
            letterHeight=28,
            pos=(0, 250),
        )

        part_0_1 = TextBox2(
            win=win,
            text=instructions["hcp"]["0.1"],
            letterHeight=28,
            pos=(0, -250),
        )

        quest = TextStim(
            win=win,
            text="?",
            color=[244, 244, 244],
            height=150,
        )

        aspect_ratio = 250 / 350

        card = Rect(
            win=win,
            width=int(250 * aspect_ratio),
            height=250,
            fillColor="grey",
            lineWidth=3,
            lineColor="white",
        )

        for ii in [card, quest, part_0_0, part_0_1]:
            ii.draw()

    def part_1(win, instructions):
        start_pos = 280
        part_1_0 = TextBox2(
            win=win,
            text=instructions["hcp"]["1.0"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 65

        part_1_1 = TextBox2(
            win=win,
            text=instructions["hcp"]["1.1"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 75
        img2 = ImageStim(
            win=win, image=winning, pos=(0, start_pos), size=winning.shape[:2]
        )

        start_pos -= 85

        part_1_2 = TextBox2(
            win=win,
            text=instructions["hcp"]["1.2"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 65
        img3 = ImageStim(win=win, image=lose, pos=(0, start_pos), size=lose.shape[:2])

        start_pos -= 85
        part_1_3 = TextBox2(
            win=win,
            text=instructions["hcp"]["1.3"],
            letterHeight=28,
            pos=(0, start_pos),
        )

        start_pos -= 65
        img4 = ImageStim(
            win=win, image=nothing, pos=(0, start_pos), size=nothing.shape[:2]
        )

        for ii in [part_1_0, part_1_1, part_1_2, part_1_3, img2, img3, img4]:
            ii.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["hcp"]["2.0"],
            letterHeight=28,
            alignment="center",
        )
        part_2_0.draw()

    return [part_0, part_1, part_2]
