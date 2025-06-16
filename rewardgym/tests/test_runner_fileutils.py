from rewardgym.runner import make_bids_name
from rewardgym.runner.psychopy_utils import overwrite_warning


def test_minimal_required():
    result = make_bids_name("001")
    assert result == "sub-001_beh.tsv"


def test_full_arguments():
    result = make_bids_name(
        subid="002",
        session="01",
        task="risk-sensitive",
        run="2",
        acquisition="highres",
        extension="events.tsv",
    )
    assert result == "sub-002_ses-01_task-risksensitive_acq-highres_run-2_events.tsv"


def test_task_hyphen_removal():
    result = make_bids_name(subid="003", task="two-step")
    assert result == "sub-003_task-twostep_beh.tsv"


def test_custom_extension():
    result = make_bids_name("004", extension="bold.nii.gz")
    assert result == "sub-004_bold.nii.gz"


def test_some_fields_none():
    result = make_bids_name("005", session="01", run=None, acquisition=None)
    assert result == "sub-005_ses-01_beh.tsv"


def test_all_optional_fields_none():
    result = make_bids_name("006", session=None, task=None, run=None, acquisition=None)
    assert result == "sub-006_beh.tsv"


def test_numeric_values_as_strings():
    result = make_bids_name("007", session="1", task="cog", run="1", acquisition="fast")
    assert result == "sub-007_ses-1_task-cog_acq-fast_run-1_beh.tsv"


def test_overwrite_warning_yes(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")

    overwrite_warning(str(test_file))
