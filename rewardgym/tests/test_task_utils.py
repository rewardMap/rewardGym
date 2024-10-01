from rewardgym.tasks.utils import (
    check_condition_present_or,
    check_conditions_not_following,
    check_conditions_not_following_substring,
    check_conditions_present,
)


def test_no_following():
    assert check_conditions_not_following([1, 3, 5, 7], [2, 4, 6], 1) == True


def test_following_within_window():
    assert check_conditions_not_following([1, 3, 5, 7], [3, 5], 1) == False


def test_following_outside_window():
    assert check_conditions_not_following([1, 3, 5, 7, 2, 4], [3, 5], 1) == False


def test_empty_condition_list():
    assert check_conditions_not_following([], [1, 2, 3], 1) == True


def test_empty_not_following():
    assert check_conditions_not_following([1, 2, 3], [], 1) == True


def test_window_length_two():
    assert check_conditions_not_following([1, 2, 3, 4, 5], [3, 5], 2) == False


def test_window_length_two_no_following():
    assert check_conditions_not_following([1, 2, 3, 4, 5], [6, 7], 2) == True


def test_condition_list_equals_not_following():
    assert check_conditions_not_following([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 1) == False


def test_window_length_zero():
    assert check_conditions_not_following([1, 2, 3, 4, 5], [3, 4], 0) == True


def test_non_integer_elements():
    assert check_conditions_not_following(["a", "b", "c", "d"], ["b", "d"], 2) == False


def test_all_conditions_present():
    assert check_conditions_present([1, 2, 3, 4, 5], [2, 4]) == True


def test_not_all_conditions_present():
    assert check_conditions_present([1, 2, 3, 4, 5], [2, 6]) == False


def test_empty_conditions_required():
    assert check_conditions_present([1, 2, 3, 4, 5], []) == True


def test_both_lists_empty():
    assert check_conditions_present([], []) == True


def test_condition_list_equals_conditions_required():
    assert check_conditions_present([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == True


def test_mixed_element_types():
    assert check_conditions_present([1, "a", 3.0, (1, 2)], ["a", 3.0]) == True


def test_condition_present_in_list():
    """Test when one of the required conditions is present."""
    condition_list = ["none_risky-40", "save-20_none"]
    condition_required = (["risky-40_none"], ["none_risky-40"])
    assert check_condition_present_or(condition_list, condition_required) == True


def test_condition_not_present_in_list():
    """Test when none of the required conditions are present."""
    condition_list = ["save-20_none", "save-40_none"]
    condition_required = (["risky-40_none"], ["none_risky-40"])
    assert check_condition_present_or(condition_list, condition_required) == False


def test_multiple_conditions_present():
    """Test when multiple conditions are present in the list."""
    condition_list = ["none_risky-40", "risky-40_none", "save-20_none"]
    condition_required = (["risky-40_none"], ["none_risky-40"])
    assert check_condition_present_or(condition_list, condition_required) == True


def test_empty_condition_list_or():
    """Test when the condition list is empty."""
    condition_list = []
    condition_required = (["risky-40_none"], ["none_risky-40"])
    assert check_condition_present_or(condition_list, condition_required) == False


def test_empty_condition_required():
    """Test when no conditions are required."""
    condition_list = ["none_risky-40", "save-20_none"]
    condition_required = ()
    assert check_condition_present_or(condition_list, condition_required) == False


def test_no_violation_with_window_1():
    # Test where no violation happens with window_length=1
    condition_list = ["abc-qqq", "qqq-qqq", "abc-qqq"]
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_violation_with_window_1():
    # Test where a violation happens with window_length=1
    condition_list = ["abc-qqq", "abc-qqq", "qqq-qqq"]
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == False
    )


def test_no_violation_with_longer_window():
    # Test where no violation happens with a longer window_length
    condition_list = ["abc-qqq", "qqq-qqq", "qqq-qqq", "abc-qqq"]
    not_following = ["abc"]
    window_length = 2
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_violation_with_longer_window():
    # Test where a violation happens with a longer window_length
    condition_list = ["abc-qqq", "qqq-qqq", "abc-qqq", "abc-qqq"]
    not_following = ["abc"]
    window_length = 2
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == False
    )


def test_no_match_in_not_following():
    # Test where nothing from not_following is in condition_list
    condition_list = ["qqq-qqq", "xyz-123", "123-xyz"]
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_empty_condition_list_not_following():
    # Test with an empty condition_list
    condition_list = []
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_empty_not_following_list():
    # Test with an empty not_following list (nothing to violate)
    condition_list = ["abc-qqq", "abc-qqq", "qqq-qqq"]
    not_following = []
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_single_element_in_condition_list():
    # Test with only one element in the condition_list
    condition_list = ["abc-qqq"]
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_window_length_exceeds_list_length():
    # Test where the window length exceeds the condition_list length
    condition_list = ["abc-qqq", "qqq-qqq"]
    not_following = ["abc"]
    window_length = 10
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


def test_no_substring_violation_due_to_non_following():
    # Test where substrings match but don't follow within the window
    condition_list = ["abc-qqq", "qqq-qqq", "abc-123"]
    not_following = ["abc"]
    window_length = 1
    assert (
        check_conditions_not_following_substring(
            condition_list, not_following, window_length
        )
        == True
    )


# To run the tests, save this in a test file and run `pytest`.
