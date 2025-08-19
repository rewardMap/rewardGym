import warnings

import pandas as pd
import pytest

from rewardgym.handling.data_tools import (
    prepare_data,  # replace with actual module path
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
