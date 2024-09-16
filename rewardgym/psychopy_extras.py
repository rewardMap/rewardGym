try:
    from psychopy.core import quit
    from psychopy.event import getKeys
    from psychopy.gui import Dlg, DlgFromDict
    from psychopy.visual import ImageStim, TextStim
except ModuleNotFoundError:
    from .psychopy_render.psychopy_stubs import (
        TextStim,
        ImageStim,
        DlgFromDict,
        Dlg,
        getKeys,
        quit,
    )

import os

import matplotlib.pyplot as plt

from . import ENVIRONMENTS


def show_instructions(
    win,
    image_path,
    view_height=500,
    scroll_speed=50,
    width_scale=1.0,
    key_map=["left", "right", "down"],
    mode="behavior",
):
    image = plt.imread(image_path)[::-1, :, :]

    img_shape = image.shape
    y_pos = img_shape[0] - view_height

    button = ImageStim(
        win, image="assets/instructions/buttonbox.png", pos=(0, -view_height // 2 - 50)
    )
    button.setAutoDraw(True)

    if mode == "behavior":
        press_button = key_map[-1]
    elif mode == "fmri":
        press_button = "\n the third button (ring finger)."

    text = TextStim(
        win,
        text=f"To begin the task press {press_button}",
        pos=(0, -view_height // 2 - 100),
        height=20,
    )

    trigger = False

    while True:
        # Draw the image
        img = ImageStim(
            win,
            image=image[y_pos : view_height + y_pos, :],
            size=(int(img_shape[1] * width_scale), view_height),
        )
        img.draw()
        win.flip()

        # Check for keypresses
        keys = getKeys()

        if key_map[0] in keys:
            if (y_pos + view_height + scroll_speed) <= img_shape[0]:
                y_pos += scroll_speed

        elif key_map[1] in keys:
            if (y_pos - scroll_speed) >= 0:
                y_pos -= scroll_speed
            else:
                trigger = True

        elif key_map[2] in keys:
            # Exit the loop
            break

        if trigger:
            text.draw()

    button.setAutoDraw(False)
    win.flip()


def set_up_experiment(outdir="data/"):
    exp_dict = {
        "participant_id": "001",
        "run": 1,
        "task": ENVIRONMENTS,
        "session": "01",
        "stimulus_set": 22,
        "mode": ["behavior", "fmri"],
        "fullscreen": False,
        "instructions": True,
        "outdir": outdir,
    }

    dlg = DlgFromDict(
        exp_dict,
        order=[
            "participant_id",
            "task",
            "run",
            "session",
            "stimulus_set",
            "mode",
            "fullscreen",
            "instructions",
            "outdir",
        ],
    )

    outdir = exp_dict["outdir"]

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if dlg.OK is False:
        quit()  # user pressed cancel

    if exp_dict["mode"] == "fmri":
        extension = "events"
        key_dict = {"9": 0, "8": 1}
        key_map = ["9", "8", "7"]

    elif exp_dict["mode"] == "behavior":
        extension = "beh"
        key_dict = {"left": 0, "right": 1, "space": 0}  # Just use default
        key_map = ["left", "right", "space"]

    exp_dict["key_map"] = key_map

    logger_name = "sub-{0}_ses-{1}_task-{2}_run-{3}_{4}.tsv".format(
        exp_dict["participant_id"],
        exp_dict["session"],
        exp_dict["task"],
        exp_dict["run"],
        extension,
    )
    logger_name = os.path.join(outdir, logger_name)

    config_save = "sub-{0}_ses-{1}_task-{2}_run-{3}_config.json".format(
        exp_dict["participant_id"],
        exp_dict["session"],
        exp_dict["task"],
        exp_dict["run"],
    )
    config_save = os.path.join(outdir, config_save)

    if os.path.isfile(logger_name):
        warning_dialog = Dlg(title=f"File Already Exists: {logger_name}")
        warning_dialog.addField("Overwrite", choices=["Yes", "No"])
        warning_data = warning_dialog.show()
        # Step 4: Handle the user's response
        if warning_data[0] == "Yes":
            pass
        else:
            quit()

    return (
        logger_name,
        config_save,
        key_dict,
        exp_dict["task"],
        exp_dict["fullscreen"],
        exp_dict["mode"],
        exp_dict["stimulus_set"],
        exp_dict,
    )
