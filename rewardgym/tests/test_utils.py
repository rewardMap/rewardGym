from ..utils import check_elements_in_list


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
