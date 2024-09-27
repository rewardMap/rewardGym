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


def make_bids_name(
    subid: str,
    session: str = None,
    task: str = None,
    run: str = None,
    acquisition: str = None,
    extension: str = "beh.tsv",
):
    # Some basic rewardmap specific sanitization:
    if task is not None:
        task = task.replace(
            "-", ""
        )  # two-step and risk-sensitive have non bids task names

    elements = {
        "sub": subid,
        "ses": session,
        "task": task,
        "acq": acquisition,
        "run": run,
    }

    name_elements = "_".join(
        ["-".join([k, v]) for k, v in elements.items() if v is not None] + [extension]
    )

    return name_elements


def overwrite_warning(filename):
    if os.path.isfile(filename):
        warning_dialog = Dlg(title=f"File Already Exists: {filename}")
        warning_dialog.addField("Overwrite", choices=["Yes", "No"])
        warning_data = warning_dialog.show()
        # Step 4: Handle the user's response
        if warning_data is None:
            quit()
        elif warning_data[0] == "Yes":
            pass
        else:
            quit()


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

    logger_name = make_bids_name(
        subid=exp_dict["participant_id"],
        session=exp_dict["session"],
        task=exp_dict["task"],
        run=exp_dict["run"],
        extension=extension,
    )

    logger_name = os.path.join(outdir, logger_name)

    config_save = make_bids_name(
        subid=exp_dict["participant_id"],
        session=exp_dict["session"],
        task=exp_dict["task"],
        run=exp_dict["run"],
        extension="config.json",
    )

    config_save = os.path.join(outdir, config_save)

    overwrite_warning(logger_name)

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
