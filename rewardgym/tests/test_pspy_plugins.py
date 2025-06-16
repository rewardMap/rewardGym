from rewardgym.runner.psychopy_utils import check_plugin_entry


def test_plugins_none():
    assert check_plugin_entry(None, "entry") == []


def test_entry_point_exists():
    plugins = {"entry": ["plugin1", "plugin2"], "other": ["plugin3"]}
    assert check_plugin_entry(plugins, "entry") == ["plugin1", "plugin2"]


def test_entry_point_does_not_exist():
    plugins = {"entry": ["plugin1", "plugin2"]}
    assert check_plugin_entry(plugins, "missing") == []


def test_empty_plugins_dict():
    assert check_plugin_entry({}, "entry") == []


def test_entry_point_with_empty_list():
    plugins = {"entry": []}
    assert check_plugin_entry(plugins, "entry") == []


def test_entry_point_key_case_sensitive():
    plugins = {"Entry": ["plugin1"]}
    assert check_plugin_entry(plugins, "entry") == []
