try:
    from psychopy import core
except ImportError:
    core = None

try:
    import pygame
except ImportError:
    pygame = None


def require_pygame():
    if pygame is None:
        raise ImportError("Install pygame with:\n" "pip install pygame")
