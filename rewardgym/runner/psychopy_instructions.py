import json

try:
    from psychopy.event import waitKeys
    from psychopy.visual import TextBox2
except ImportError:
    from ..psychopy_render.psychopy_stubs import TextBox2, waitKeys

import pathlib

from ..tasks.task_loader import get_instructions_psychopy


def show_instructions(task, win, key_map={"left": 0, "right": 1}):
    instructions_path = (
        pathlib.Path(__file__).parents[1].resolve() / "assets" / "instructions_en.json"
    )
    print(instructions_path)
    instructions = json.loads(instructions_path.read_text())

    def end_screen(win, instructions):
        end = TextBox2(
            win=win,
            text=instructions["instructions_end"],
            letterHeight=28,
            pos=(0, 0),
        )
        end.draw()

    def first_screen(win, instructions):
        end = TextBox2(
            win=win,
            text=instructions["instructions"],
            letterHeight=28,
            pos=(0, 0),
        )
        end.draw()

    instructions_list, instructions_dict = get_instructions_psychopy(task)
    instructions.update(instructions_dict)

    if instructions_list:
        instruction_screen = [first_screen] + instructions_list + [end_screen]
        max_slide = len(instruction_screen) - 1
        slide_index = 0
        running = True

        while running:
            instruction_screen[slide_index](win, instructions)
            win.flip()

            outkey = waitKeys(keyList=list(key_map.keys()))[0]

            if slide_index == max_slide:
                if key_map[outkey] == 1:
                    running = False
                elif key_map[outkey] == 0:
                    slide_index -= 1

            elif key_map[outkey] == 0:
                slide_index = max([0, slide_index - 1])
            elif key_map[outkey] == 1:
                slide_index = min([max_slide, slide_index + 1])
