try:
    from psychopy.core import quit
    from psychopy.gui import Dlg, DlgFromDict
except ModuleNotFoundError:
    from .psychopy_render.psychopy_stubs import (
        DlgFromDict,
        Dlg,
        quit,
    )

import os

from . import ENVIRONMENTS


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
