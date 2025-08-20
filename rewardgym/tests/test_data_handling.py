import warnings

import pandas as pd
import pytest

from rewardgym.handling.data_tools import (  # replace with actual module path
    prepare_data,
    prepare_data_for_rl,
    process_trial_for_rl,
)


@pytest.fixture
def sample_dict():
    return {
        "onset": [0.1, 0.2, 0.3],
        "duration": [1.0, 1.5, 2.0],
        "start_position": [1, 2, 3],
        "response_time": [0.5, 0.6, 0.7],
        "reward": [10, 20, 30],
        "trial": [1, 2, 3],
        "action": [0, 1, 2],
        "rl_label": ["a", "b", "c"],
        "response_button": ["left", "right", "left"],
        "event_type": ["trial", "reminder", "trial"],
    }


@pytest.mark.parametrize("input_type", ["dict", "dataframe"])
def test_input_dict_and_dataframe(sample_dict, input_type):
    if input_type == "dict":
        data = sample_dict
    else:
        data = pd.DataFrame(sample_dict)

    df_out, dropped = prepare_data(data)
    assert isinstance(df_out, pd.DataFrame)
    # reminder row should be dropped
    assert dropped == 1
    assert set(df_out["response_button"].unique()) <= {0, 1}


def test_input_as_csv(sample_dict, tmp_path):
    file_path = tmp_path / "test.csv"
    pd.DataFrame(sample_dict).to_csv(file_path, sep="\t", index=False)

    df_out, dropped = prepare_data(str(file_path))
    assert isinstance(df_out, pd.DataFrame)
    assert dropped == 1


@pytest.mark.parametrize(
    "drop_flag,expected_rows,expected_dropped",
    [
        (True, 2, 1),  # reminder trial dropped
        (False, 3, None),  # keep all trials
    ],
)
def test_drop_trials_behavior(sample_dict, drop_flag, expected_rows, expected_dropped):
    df = pd.DataFrame(sample_dict)
    df_out, dropped = prepare_data(df, drop_trials=drop_flag)
    assert len(df_out) == expected_rows
    assert dropped == expected_dropped


@pytest.mark.parametrize(
    "remap_dict,expected_values",
    [
        ({"left": 10, "right": 20}, {10, 20}),
        ({"left": "L", "right": "R"}, {"L", "R"}),
    ],
)
def test_custom_remap(sample_dict, remap_dict, expected_values):
    df = pd.DataFrame(sample_dict)
    df_out, _ = prepare_data(df, remap_dictionary=remap_dict)
    assert set(df_out["response_button"].unique()) <= expected_values


def test_string_replacement_and_types():
    data = {
        "onset": ["n/a"],
        "duration": ["None"],
        "start_position": [1],
        "response_time": [0.1],
        "reward": [5],
        "trial": [1],
        "action": [1],
        "rl_label": ["x"],
        "response_button": ["left"],
        "event_type": ["trial"],
    }
    df = pd.DataFrame(data)
    df_out, _ = prepare_data(df)

    assert pd.isna(df_out.loc[0, "onset"])
    assert pd.isna(df_out.loc[0, "duration"])


def test_missing_columns_warns():
    df = pd.DataFrame(
        {
            "onset": [0.1],
            "response_button": ["left"],
            "event_type": ["trial"],
            "trial": [0],
        }
    )
    with warnings.catch_warnings(record=True) as w:
        df_out, _ = prepare_data(df)
        assert any("missing" in str(warn.message).lower() for warn in w)


def test_empty_dataframe():
    df = pd.DataFrame(
        columns=[
            "onset",
            "duration",
            "start_position",
            "response_time",
            "reward",
            "trial",
            "action",
            "rl_label",
            "response_button",
            "event_type",
        ]
    )
    df_out, dropped = prepare_data(df)
    assert df_out.empty
    assert dropped == 0


@pytest.fixture
def sample_df():
    """A small raw dataframe with one complete trial (obs→action→reward→obs1)."""
    return pd.DataFrame(
        [
            {
                "trial": 1,
                "onset": 0.1,
                "rl_label": "obs",
                "current_location": "A",
                "action": None,
                "reward": None,
                "response_time": None,
            },
            {
                "trial": 1,
                "onset": 0.2,
                "rl_label": "action",
                "current_location": None,
                "action": "left",
                "reward": None,
                "response_time": 0.5,
            },
            {
                "trial": 1,
                "onset": 0.3,
                "rl_label": "reward",
                "current_location": None,
                "action": None,
                "reward": 1,
                "response_time": None,
            },
            {
                "trial": 1,
                "onset": 0.4,
                "rl_label": "obs",
                "current_location": "B",
                "action": None,
                "reward": None,
                "response_time": None,
            },
        ]
    )


def test_process_trial_for_rl_complete(sample_df):
    """Ensure process_trial_for_rl produces the expected tuple from one full trial."""
    tuples = process_trial_for_rl(1, sample_df)
    assert len(tuples) == 1
    obs0, action, reward, obs1, rt, trial = tuples[0]
    assert obs0 == "A"
    assert action == "left"
    assert reward == 1
    assert obs1 == "B"
    assert rt == 0.5
    assert trial == 1


def test_process_trial_for_rl_multiple_obs_warns(sample_df):
    """If more than 2 obs appear before the tuple closes, a warning should be raised."""
    df = pd.DataFrame(
        [
            {
                "trial": 1,
                "onset": 0.1,
                "rl_label": "obs",
                "current_location": "A",
                "action": None,
                "reward": None,
                "response_time": None,
            },
            {
                "trial": 1,
                "onset": 0.2,
                "rl_label": "obs",
                "current_location": "B",
                "action": None,
                "reward": None,
                "response_time": None,
            },
            {
                "trial": 1,
                "onset": 0.3,
                "rl_label": "obs",
                "current_location": "C",
                "action": None,
                "reward": None,
                "response_time": None,
            },
            {
                "trial": 1,
                "onset": 0.4,
                "rl_label": "action",
                "current_location": None,
                "action": "left",
                "reward": None,
                "response_time": 0.5,
            },
            {
                "trial": 1,
                "onset": 0.5,
                "rl_label": "reward",
                "current_location": None,
                "action": None,
                "reward": 1,
                "response_time": None,
            },
        ]
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        process_trial_for_rl(1, df)
        assert any("More than two obs" in str(warning.message) for warning in w)


def test_process_trial_for_rl_partial_tuple(sample_df):
    """A trial missing obs1 should still return tuple if obs0, action, reward exist."""
    df = sample_df.drop(sample_df.index[-1])  # drop obs1
    tuples = process_trial_for_rl(1, df)
    assert len(tuples) == 1
    obs0, action, reward, obs1, rt, trial = tuples[0]
    assert obs0 == "A"
    assert action == "left"
    assert reward == 1
    assert obs1 is None  # missing obs1


def test_prepare_data_for_rl(sample_df):
    """Integration test for prepare_data_for_rl."""
    df = sample_df.copy()
    result_df = prepare_data_for_rl(df)
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == [
        "obs0",
        "action",
        "reward",
        "obs1",
        "reaction_time",
        "trial",
    ]
    assert result_df.shape[0] == 1
    row = result_df.iloc[0]
    assert row.obs0 == "A"
    assert row.action == "left"
    assert row.reward == 1
    assert row.obs1 == "B"
    assert row.reaction_time == 0.5
    assert row.trial == 1


def test_prepare_data_for_rl_multiple_trials(sample_df):
    """Ensure multiple trials are processed independently."""
    df2 = sample_df.copy()
    df2["trial"] = 2  # duplicate with different trial id
    df = pd.concat([sample_df, df2], ignore_index=True)

    result_df = prepare_data_for_rl(df)
    assert result_df["trial"].nunique() == 2
    assert result_df.shape[0] == 2
