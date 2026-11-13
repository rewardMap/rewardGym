try:
    from psychopy.core import quit
    from psychopy.gui import Dlg, DlgFromDict
except ModuleNotFoundError:
    from ..stubs import (
        Dlg,
        DlgFromDict,
        quit,
    )

import os

from .file_utils import make_bids_name


def check_plugin_entry(plugins: dict, entry_point: str):
    if plugins is None:
        return []

    if entry_point in plugins.keys():
        return plugins[entry_point]
    else:
        return []


def apply_plugins(
    *,
    plugins: dict,
    entry_point: str,
    env,
    settings,
    episode,
    actions,
    **kwargs,
):
    plugin_list = check_plugin_entry(plugins=plugins, entry_point=entry_point)

    for pl in plugin_list:
        pl.modify(
            env=env,
            logger=env.context.logger,
            win=env.context.win,
            settings=settings,
            episode=episode,
            actions=actions,
            input_handler=env.context.input_handler,
        )


def overwrite_warning(filename):
    if os.path.isfile(filename):
        warning_dialog = Dlg(title=f"File Already Exists: {filename}")
        warning_dialog.addField("Overwrite", choices=["Yes", "No"])
        warning_data = warning_dialog.show()

        if warning_data is None or warning_data[0] != "Yes":
            quit()
        else:
            pass


def pspy_set_up_experiment(outdir="data/"):
    from .. import ENVIRONMENTS

    exp_dict = {
        "participant_id": "001",
        "run": 1,
        "task": ENVIRONMENTS,
        "session": "01",
        "stimulus_set": 22,
        "mode": ["behavior", "fmri"],
        "fullscreen": False,
        "instructions": False,
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
        extension=extension + ".tsv",
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


def update_psychopy_trials(settings, env, episode):
    # Update timings
    if settings["update"] is not None and len(settings["update"]) > 0:
        for k in settings["update"]:
            for jj in env.info_dict:
                if "psychopy" in env.info_dict[jj]:
                    for ii in env.info_dict[jj]["psychopy"]:
                        if ii.name == k:
                            ii.duration = settings[k][episode]
