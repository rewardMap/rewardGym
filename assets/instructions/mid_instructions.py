from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, mid_stimuli


def mid_instructions():
    size = (125, 125)

    def part_0(win, instructions, size=size):
        left_pos = [-260, -135, 0, 135, 260]

        part_0_0 = TextBox2(
            win=win,
            text=instructions["mid"]["0.0"],
            letterHeight=24,
            pos=(0, 200),
        )

        stims = [
            mid_stimuli(am, shap)
            for am, shap in zip(
                ["-5", "-1", "0", "+1", "+5"],
                ["square", "square", "triangle_u", "circle", "circle"],
            )
        ]

        stims = [
            ImageStim(win=win, image=i, pos=(lp, 0), size=size)
            for i, lp in zip(stims, left_pos)
        ]
        part_0_1 = TextBox2(
            win=win,
            text=instructions["mid"]["0.1"],
            letterHeight=24,
            pos=(0, -200),
        )

        for ii in stims + [part_0_0, part_0_1]:
            ii.draw()

    def part_1(win, instructions):
        fix = fixation_cross()

        part_1_0 = TextBox2(
            win=win,
            text=instructions["mid"]["1.0"],
            letterHeight=24,
            pos=(0, 250),
        )

        fix = ImageStim(win=win, image=fix, size=fix.shape[:2])

        for i in [part_1_0, fix]:
            i.draw()

    def part_2(win, instructions, size=size):
        left_pos = [-130, 0, 130]

        stims = [
            mid_stimuli(am, shap, probe=True)
            for am, shap in zip(["", "", ""], ["square", "triangle_u", "circle"])
        ]

        stims = [
            ImageStim(win=win, image=i, pos=(lp, 0), size=size)
            for i, lp in zip(stims, left_pos)
        ]
        part_2_0 = TextBox2(
            win=win,
            text=instructions["mid"]["2.0"],
            letterHeight=24,
            pos=(0, 200),
        )

        part_2_1 = TextBox2(
            win=win,
            text=instructions["mid"]["2.1"],
            letterHeight=24,
            pos=(0, -200),
        )
        for ii in stims + [part_2_0, part_2_1]:
            ii.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["mid"]["3.0"],
            letterHeight=24,
            alignment="center",
        )
        part_3_0.draw()

    return [part_0, part_1, part_2, part_3]
