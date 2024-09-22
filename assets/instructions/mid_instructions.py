import json

from psychopy.event import waitKeys
from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import fixation_cross, mid_stimuli


def mid_instructions(win, key_map={"left": 0, "right": 1}, show_training=True):
    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    instructions = instructions["mid"]
    fix = fixation_cross()
    key_list = list(key_map.keys())

    part_0_0 = TextBox2(
        win=win,
        text=instructions["0.0"],
        letterHeight=22,
        pos=(0, 200),
    )

    stims = [
        mid_stimuli(am, shap)
        for am, shap in zip(
            ["-5", "-1", "0", "+1", "+5"],
            ["square", "square", "triangle_u", "circle", "circle"],
        )
    ]

    left_pos = [-260, -135, 0, 135, 260]

    size = (125, 125)

    stims = [
        ImageStim(win=win, image=i, pos=(lp, 0), size=size)
        for i, lp in zip(stims, left_pos)
    ]
    part_0_1 = TextBox2(
        win=win,
        text=instructions["0.1"],
        letterHeight=22,
        pos=(0, -200),
    )

    for ii in stims + [part_0_0, part_0_1]:
        ii.draw()

    win.flip()
    waitKeys()

    part_1_0 = TextBox2(
        win=win,
        text=instructions["1.0"],
        letterHeight=22,
        pos=(0, 250),
    )

    fix = ImageStim(win=win, image=fix, size=fix.shape[:2])

    for i in [part_1_0, fix]:
        i.draw()

    win.flip()

    waitKeys()

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
        text=instructions["2.0"],
        letterHeight=22,
        pos=(0, 200),
    )

    part_2_1 = TextBox2(
        win=win,
        text=instructions["2.1"],
        letterHeight=22,
        pos=(0, -200),
    )
    for ii in stims + [part_2_0, part_2_1]:
        ii.draw()

    win.flip()
    waitKeys()

    if show_training:
        part_3_0 = TextBox2(
            win=win, text=instructions["3.0"], letterHeight=22, alignment="center"
        )
        part_3_0.draw()
        win.flip()

        waitKeys()

    return key_list
