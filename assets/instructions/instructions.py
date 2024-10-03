import json
import warnings

from psychopy.event import waitKeys
from psychopy.visual import TextStim

from .gonogo_instructions import gonogo_instructions
from .hcp_instructions import hcp_instructions
from .mid_instructions import mid_instructions
from .posner_instructions import posner_instructions
from .risksensitive_instructions import risksensitive_instructions
from .twostep_instructions import twostep_instructions


def get_instructions(task: str):
    if task == "two-step":
        return twostep_instructions
    elif task == "hcp":
        return hcp_instructions
    elif task == "gonogo":
        return gonogo_instructions
    elif task == "mid":
        return mid_instructions
    elif task == "posner":
        return posner_instructions
    elif task == "risk-sensitive":
        return risksensitive_instructions
    else:
        warnings.warn("Instructions are not yet implemented.")
        return False


def show_instructions(task, win, key_map={"left": 0, "right": 1}):
    with open("assets/instructions/instructions_en.json") as f:
        instructions = json.load(f)

    def end_screen(win, instructions):
        end = TextStim(
            win=win,
            text=instructions["instructions_end"],
            height=28,
            pos=(0, 0),
        )
        end.draw()

    def first_screen(win, instructions):
        end = TextStim(
            win=win,
            text=instructions["instructions"],
            height=28,
            pos=(0, 0),
        )
        end.draw()

    instruction_funs = get_instructions(task)

    if instruction_funs:
        instruction_screen = [first_screen] + instruction_funs() + [end_screen]
        max_slide = len(instruction_screen) - 1
        slide_index = 0
        running = True

        while running:
            instruction_screen[slide_index](win, instructions)
            win.flip()

            outkey = waitKeys(keyList=list(key_map.keys()))[0]

            if slide_index == max_slide:
                if key_map[outkey] == 0:
                    running = False
                elif key_map[outkey] == 1:
                    slide_index -= 1

            elif key_map[outkey] == 0:
                slide_index = max([0, slide_index - 1])
            elif key_map[outkey] == 1:
                slide_index = min([max_slide, slide_index + 1])
