from pathlib import Path

import pytest

from rewardgym import extend_task_registry


def test_task_registry_overwrite_warning():
    path = Path(__file__).parent / "../tasks/twostep"

    with pytest.warns(UserWarning, match="already registered"):
        extend_task_registry(extra_dirs=[path])
