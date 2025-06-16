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
        ["-".join([k, str(v)]) for k, v in elements.items() if v is not None]
        + [extension]
    )

    return name_elements
