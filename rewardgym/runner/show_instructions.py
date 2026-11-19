import json

from .. import ASSETS_PATH
from ..render.contexts import EnvironmentContext
from ..render.routines.passive_routines import InstructionRoutine
from ..render.stimulus_definitions import TextDefinition
from ..tasks.task_loader import get_instructions_psychopy


def show_instructions(task, win, mode="pygame", key_map=None):
    context = EnvironmentContext(window=win, mode=mode)

    if key_map is None:
        key_map = {"left": 0, "right": 1, "q": "quit"}
    instructions_path = ASSETS_PATH / "instructions_en.json"
    print(instructions_path)
    instructions = json.loads(instructions_path.read_text())

    end = InstructionRoutine(
        name="end",
        stimulus_definitions=[
            TextDefinition(name="end", text=instructions["instructions_end"], height=28)
        ],
    )

    start = InstructionRoutine(
        name="start",
        stimulus_definitions=[
            TextDefinition(name="start", text=instructions["instructions"], height=28)
        ],
    )

    instructions_list, instructions_dict = get_instructions_psychopy(task)
    instructions.update(instructions_dict)

    if instructions_list:
        instruction_screen = [start] + instructions_list + [end]
        for ii in instruction_screen:
            ii.setup(context=context)

        max_slide = len(instruction_screen) - 1
        slide_index = 0
        running = True

        while running:
            instruction_screen[slide_index].present(context=context)

            response = context.input_handler.get_keys()
            for resp in response:
                outkey = resp[0]

                if outkey in key_map:
                    if slide_index == max_slide:
                        if key_map[outkey] == 1:
                            running = False
                        elif key_map[outkey] == 0:
                            slide_index -= 1

                    elif key_map[outkey] == 0:
                        slide_index = max([0, slide_index - 1])
                    elif key_map[outkey] == 1:
                        slide_index = min([max_slide, slide_index + 1])

                    if key_map[outkey] == "quit":
                        context.window.close()
