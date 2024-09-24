import json

from psychopy.event import waitKeys
from psychopy.visual import ImageStim, TextBox2

from rewardgym.psychopy_render.default_images import (
    fixation_cross,
    posner_cue,
    posner_target,
)


def posner_instructions(win, key_map={"left": 0, "right": 1}, show_training=True):
    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    instructions = instructions["posner"]
    fix = fixation_cross()
    key_list = list(key_map.keys())

    part_0_0 = TextBox2(
        win=win,
        text=instructions["0.0"],
        letterHeight=24,
        pos=(0, 200),
    )

    fix = ImageStim(win=win, image=fix, size=fix.shape[:2])

    fix.draw()
    part_0_0.draw()
    win.flip()
    waitKeys()

    part_1_0 = TextBox2(
        win=win,
        text=instructions["1.0"],
        letterHeight=24,
        pos=(0, 250),
    )

    cue_up = posner_cue(up=True)
    cue_down = posner_cue(up=False)

    cue_up_stim = ImageStim(win=win, pos=(-200, 0), image=cue_up, size=cue_up.shape[:2])
    cue_down_stim = ImageStim(
        win=win, pos=(200, 0), image=cue_down, size=cue_down.shape[:2]
    )

    for i in [part_1_0, cue_up_stim, cue_down_stim]:
        i.draw()

    win.flip()
    waitKeys()

    pt = posner_target()
    pt_left = ImageStim(win=win, pos=(-300, 0), image=pt, size=pt.shape[:2])
    pt_right = ImageStim(win=win, pos=(300, 0), image=pt, size=pt.shape[:2])

    part_2_0 = TextBox2(
        win=win,
        text=instructions["2.0"],
        letterHeight=24,
        pos=(0, 200),
    )

    for ii in [part_2_0, pt_left, pt_right]:
        ii.draw()

    win.flip()
    waitKeys()

    part_3_0 = TextBox2(
        win=win,
        text=instructions["3.0"],
        letterHeight=24,
        pos=(0, 0),
    )

    for ii in [part_3_0]:
        ii.draw()

    win.flip()
    waitKeys()

    if show_training:
        part_3_0 = TextBox2(
            win=win, text=instructions["4.0"], letterHeight=24, alignment="center"
        )
        part_3_0.draw()
        win.flip()

        waitKeys()

    return key_list
