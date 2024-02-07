import types

import pytest

from ..utils import check_elements_in_list, get_condition_state, unpack_conditions


def test_check_element_list_all_elements_present():
    check_list = [1, 2, 3]
    check_set = [1, 2, 3]
    assert check_elements_in_list(check_list, check_set) is True


def test_check_element_list_some_elements_missing():
    check_list = [1, 2, 3]
    check_set = [1, 2]
    assert check_elements_in_list(check_list, check_set) is False


def test_check_element_list_empty_list():
    check_list = []
    check_set = [1, 2, 3]
    assert check_elements_in_list(check_list, check_set) is True


def test_check_element_list_empty_set():
    check_list = [1, 2, 3]
    check_set = []
    assert check_elements_in_list(check_list, check_set) is False


def test_check_element_list_both_empty():
    check_list = []
    check_set = []
    assert check_elements_in_list(check_list, check_set) is True


def test_check_element_list_duplicate_elements():
    check_list = [1, 2, 2, 3]
    check_set = [1, 2, 3]
    assert check_elements_in_list(check_list, check_set) is True


@pytest.mark.parametrize(
    "conditions, episode, expected_output",
    [
        (None, None, None),
        ([1, 2, 3], 1, 2),
        (([1, 2, 3], [1, 0, 0]), 2, 1),
        (([1],), None, 1),
    ],
)
def test_get_condition_state(conditions, episode, expected_output):
    result = get_condition_state(conditions, episode)
    assert result == expected_output


@pytest.mark.parametrize(
    "conditions, episode, expected_output",
    [
        ([1, 2, 3], 4, pytest.raises(IndexError, match="list index.*")),
        (([1, 2, 3], [0.1, 0.2]), None, pytest.raises(ValueError)),
        ([1, 2, 3], None, pytest.raises(Exception)),
    ],
)
def test_get_condition_exceptions(conditions, episode, expected_output):
    with expected_output:
        get_condition_state(conditions, episode)


def test_unpack_conditions_lists():

    l1 = [1, 2, 3]
    l2 = None

    assert unpack_conditions((l1, l2), 1) == (2, None)
    assert unpack_conditions((l2, l1), 1) == (None, 2)
    assert unpack_conditions((l1, l1), 1) == (2, 2)


def test_unpack_conditions_tuple():

    l1 = ([1, 2, 3], [1, 0, 0])
    l2 = None
    l3 = ([0],)

    assert unpack_conditions((l1, l2), 1) == (1, None)
    assert unpack_conditions((l2, l1), 1) == (None, 1)
    assert unpack_conditions((l1, l1), 1) == (1, 1)
    assert unpack_conditions((l3, l1), 1) == (0, 1)
