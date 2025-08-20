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


def process_trial_for_rl(trial_id: int, trial_df: pd.DataFrame) -> list:
    """
    Process a single trial into (obs0, action, reward, obs1, reaction_time, trial).
    Returns a list of tuples.
    """
    tuples = []
    trial_df = trial_df.reset_index(drop=True)

    def make_empty_dict(
        trial_id,
        dictionary_keys=["obs0", "action", "reward", "obs1", "reaction_time", "trial"],
    ):
        template_dict = {key: None for key in dictionary_keys}
        template_dict["trial"] = trial_id

        return template_dict

    tmp_dict = make_empty_dict(trial_id)

    tmp_obs0 = None

    for i in range(len(trial_df)):
        row = trial_df.loc[i]

        if row["rl_label"] == "obs":
            if tmp_dict["obs0"] is None:
                tmp_dict["obs0"] = row["current_location"]
            else:
                if tmp_dict["obs1"] is None:
                    tmp_dict["obs1"] = row["current_location"]
                    tmp_obs0 = row["current_location"]
                else:
                    warnings.warn(
                        "More than two obs encountered in trial %s" % trial_id
                    )

        elif row["rl_label"] == "action":
            if tmp_dict["action"] is None:
                tmp_dict["action"] = row["action"]
                tmp_dict["reaction_time"] = row["response_time"]

        elif row["rl_label"] == "reward":
            if tmp_dict["reward"] is None:
                tmp_dict["reward"] = row["reward"]

        # Check if a complete tuple is ready
        if all(value is not None for value in tmp_dict.values()):
            tuples.append(tuple(tmp_dict.values()))
            tmp_dict = make_empty_dict(trial_id)
            tmp_dict["trial"] = trial_id

            if tmp_obs0 is not None:
                tmp_dict["obs0"] = tmp_obs0
                tmp_obs0 = None

    # Handle dangling partial tuple with obs0, action, reward
    if all(tmp_dict[key] is not None for key in ["obs0", "action", "reward"]):
        tuples.append(tuple(tmp_dict.values()))

    return tuples


def prepare_data_for_rl(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw event dataframe into structured obs→action→reward→obs1 sequences.
    """
    # Step 1: Sort and reset
    df = df.sort_values(["trial", "onset"]).reset_index(drop=True).copy()

    # Step 2: Process trials
    all_tuples = []
    for trial_id, trial_df in df.groupby("trial"):
        all_tuples.extend(process_trial_for_rl(trial_id, trial_df))

    # Step 3: Build dataframe
    rl_dataframe = pd.DataFrame(
        all_tuples,
        columns=["obs0", "action", "reward", "obs1", "reaction_time", "trial"],
    )
    return rl_dataframe
