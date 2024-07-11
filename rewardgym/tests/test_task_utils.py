import numpy as np

from rewardgym.tasks.utils import (
    check_conditions_not_following,
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


def test_empty_condition_list():
    assert check_conditions_present([], [1, 2, 3]) == False


def test_empty_conditions_required():
    assert check_conditions_present([1, 2, 3, 4, 5], []) == True


def test_both_lists_empty():
    assert check_conditions_present([], []) == True


def test_condition_list_equals_conditions_required():
    assert check_conditions_present([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == True


def test_non_integer_elements():
    assert check_conditions_present(["a", "b", "c", "d"], ["b", "d"]) == True


def test_mixed_element_types():
    assert check_conditions_present([1, "a", 3.0, (1, 2)], ["a", 3.0]) == True
