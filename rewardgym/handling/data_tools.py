import warnings
from typing import Dict, Union

import numpy as np
import pandas as pd

try:
    pd.set_option("future.no_silent_downcasting", True)
except pd._config.config.OptionError:
    # Option removed in pandas >= 2.2
    pass


def prepare_data(
    data: Union[Dict, pd.DataFrame],
    remap_dictionary={"left": 0, "right": 1},
    drop_trials=True,
    seperator="\t",
):
    if isinstance(data, dict):
        data = pd.DataFrame.from_dict(data)
    elif isinstance(data, str):
        data = pd.read_csv(data, sep=seperator)

    data = data.replace({"n/a": np.nan, "None": None}).infer_objects(copy=False)
    if remap_dictionary is not None:
        data["response_button"] = data["response_button"].map(remap_dictionary)

    for data_typ, col in zip(
        [
            float,
            float,
            pd.Int64Dtype(),
            float,
            float,
            pd.Int64Dtype(),
            pd.Int64Dtype(),
            str,
        ],
        [
            "onset",
            "duration",
            "start_position",
            "response_time",
            "reward",
            "trial",
            "action",
            "rl_label",
        ],
    ):
        try:
            data[col] = data[col].astype(data_typ)
        except KeyError:
            warnings.warn(
                f"Column '{col}' missing in DataFrame. Could not cast to {data_typ}.",
                UserWarning,
            )

    if drop_trials:
        trials_to_drop = data.query("event_type == 'reminder'").trial.values
        print(f"Dropping {len(trials_to_drop)} trials.")
        data = data[~data["trial"].isin(trials_to_drop)]
        dropped_trials = len(trials_to_drop)
    else:
        dropped_trials = None

    return data, dropped_trials
