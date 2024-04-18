import types

import numpy as np
import pytest

from .. import ENVIRONMENTS, get_env
from ..utils import (
    add_to_df,
    check_elements_in_list,
    check_seed,
    get_condition_state,
    get_starting_nodes,
    run_single_episode,
    unpack_conditions,
)


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


def test_check_seed_with_int():
    seed = 5678
    rng = check_seed(seed)
    assert isinstance(rng, np.random.Generator)
    try:
        assert rng.bit_generator.seed_seq.entropy == seed
    except AttributeError:  # For compatibility with earlier python versions
        assert rng.bit_generator._seed_seq.entropy == seed


def test_check_seed_with_generator():
    generator = np.random.default_rng(9876)
    rng = check_seed(generator)
    assert rng == generator


def test_check_seed_with_default():
    rng = check_seed()
    assert isinstance(rng, np.random.Generator)
    try:
        assert rng.bit_generator.seed_seq.entropy == 1234
    except AttributeError:  # For compatibility with earlier python versions
        assert rng.bit_generator._seed_seq.entropy == 1234


def test_check_seed_with_invalid_input():
    with pytest.raises(TypeError):
        check_seed("invalid_seed")


def test_get_starting_nodes():
    # Test case 1: Basic example
    graph1 = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
    assert get_starting_nodes(graph1) == ["A"]

    # Test case 2: Graph with multiple starting nodes
    graph2 = {"A": ["B"], "B": ["C"], "C": ["D"], "E": ["F"]}
    assert sorted(get_starting_nodes(graph2)) == sorted(["A", "E"])

    # Test case 3: Graph with one node and no connections
    graph3 = {"A": []}
    assert get_starting_nodes(graph3) == ["A"]

    # Test case 4: Graph with no nodes
    graph4 = {}
    assert get_starting_nodes(graph4) == []


def test_run_episode_smokescreen():
    from .. import ENVIRONMENTS, get_env
    from ..agents import base_agent
    from ..utils import unpack_conditions

    for envname in ENVIRONMENTS:
        n_episodes = 20
        env, conditions = get_env(envname)
        agent = base_agent.QAgent(
            learning_rate=0.25,
            temperature=1.0,
            discount_factor=0.99,
            action_space=env.action_space.n,
        )

        for ne in range(n_episodes):

            condition, starting_position = unpack_conditions(conditions, ne)

            if envname == "risk-sensitive":
                avail_actions = list(env.condition_dict[condition].values())
            else:
                avail_actions = None

            a = run_single_episode(
                env,
                agent,
                starting_position,
                condition,
                step_reward=envname == "two-step",
                avail_actions=avail_actions,
            )


def test_add_to_df_new_df():
    episode_step = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    expected_df = {
        "index": [0, 1, 2],
        "episode": [None, None, None],
        "state": [0, 3, 6],
        "action": [1, 4, 7],
        "reward": [2, 5, 8],
        "condition": [None, None, None],
        "starting_position": [None, None, None],
    }
    result_df = add_to_df(episode_step)
    assert result_df == expected_df


def test_add_to_df_existing_df():
    episode_step = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    existing_df = {
        "index": [0, 1],
        "episode": [None, None],
        "state": [0, 3],
        "action": [1, 4],
        "reward": [2, 5],
        "condition": [None, None],
        "starting_position": [None, None],
    }
    expected_df = {
        "index": [0, 1, 2, 3, 4],
        "episode": [None, None, None, None, None],
        "state": [0, 3, 0, 1, 2],
        "action": [1, 4, 3, 4, 5],
        "reward": [2, 5, 6, 7, 8],
        "condition": [None, None, None, None, None],
        "starting_position": [None, None, None, None, None],
    }
    result_df = add_to_df(episode_step, df=existing_df)
    assert result_df == expected_df
