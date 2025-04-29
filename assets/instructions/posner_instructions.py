from psychopy.visual import ImageStim, TextBox2

from rewardgym.stimuli.default_images import posner_target
from rewardgym.stimuli.fixation_images import fixation_cross, posner_cue


def posner_instructions():
    def part_0(win, instructions):
        fix = fixation_cross()
        part_0_0 = TextBox2(
            win=win,
            text=instructions["posner"]["0.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        fix = ImageStim(win=win, image=fix, size=fix.shape[:2])

        fix.draw()
        part_0_0.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["posner"]["1.0"],
            letterHeight=28,
            pos=(0, 250),
        )

        cue_left = posner_cue(left=True)
        cue_right = posner_cue(left=False)

        cue_left_stim = ImageStim(
            win=win, pos=(-200, 0), image=cue_left, size=cue_left.shape[:2]
        )
        cue_right_stim = ImageStim(
            win=win, pos=(200, 0), image=cue_right, size=cue_right.shape[:2]
        )

        for i in [part_1_0, cue_left_stim, cue_right_stim]:
            i.draw()

    def part_2(win, instructions):
        pt = posner_target(target=True)
        pt_left = ImageStim(
            win=win,
            pos=(-300, 100),
            image=posner_target(target=True),
            size=pt.shape[:2],
        )
        pt_right = ImageStim(
            win=win,
            pos=(300, 100),
            image=posner_target(target=True)[::-1],
            size=pt.shape[:2],
        )

        pt_dist = ImageStim(
            win=win,
            pos=(0, -125),
            image=posner_target(target=False)[::-1],
            size=pt.shape[:2],
        )

        part_2_0 = TextBox2(
            win=win,
            text=instructions["posner"]["2.0"],
            letterHeight=28,
            pos=(0, 250),
        )
        part_2_1 = TextBox2(
            win=win,
            text=instructions["posner"]["2.1"],
            letterHeight=28,
            pos=(0, -10),
        )

        part_2_2 = TextBox2(
            win=win,
            text=instructions["posner"]["2.2"],
            letterHeight=28,
            pos=(0, -250),
        )

        for ii in [part_2_0, part_2_1, part_2_2, pt_left, pt_right, pt_dist]:
            ii.draw()

    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["posner"]["3.0"],
            letterHeight=28,
            pos=(0, 0),
        )

        for ii in [part_3_0]:
            ii.draw()

    def part_4(win, instructions):
        part_4_0 = TextBox2(
            win=win,
            text=instructions["posner"]["4.0"],
            letterHeight=28,
            alignment="center",
        )
        part_4_0.draw()

    return [part_0, part_1, part_2, part_3, part_4]
