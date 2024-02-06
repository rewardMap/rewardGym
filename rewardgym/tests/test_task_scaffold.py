import pytest

from ..tasks import get_env


def test_smoke_screen_hcp_base():
    get_env("hcp", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_hcp_render():
    get_env(
        "hcp",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )


def test_smoke_screen_mid_base():
    get_env("mid", conditions=None, render_mode=None, render_backend=None)


def test_smoke_screen_mid_render():
    get_env(
        "mid",
        conditions=None,
        render_mode="human",
        render_backend="pygame",
        window_size=10,
    )
