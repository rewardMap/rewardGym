from collections.abc import Callable

from ..protocols import ClockProtocol
from ..render.stimulus_stubs import SimBaseStim
from ..render.stimulus_stubs import SimImageStim as ImageStim
from ..render.stimulus_stubs import SimRect as Rect
from ..render.stimulus_stubs import SimTextStim as TextStim

__all__ = [
    "ImageStim",
    "Rect",
    "TextStim",
]


class Clock(ClockProtocol):
    def __init__(self):
        self.time = 0

    def getTime(self):
        return self.time

    def reset(self):
        pass


class Window:
    def __init__(self, **kwargs):
        pass

    def flip(self):
        pass

    def close(self):
        pass

    def callOnFlip(self, function: Callable, *args, **kwargs):
        pass


class TextBox2(SimBaseStim):
    pass


class Line(SimBaseStim):
    pass


def getKeys(**kwargs):
    pass


def waitKeys(**kwargs):
    pass


def quit():
    pass


class Dlg:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def addField(self, *args, **kwargs):
        pass

    def show(self):
        # Just for working with the gui dialog
        return ["Yes"]


class DlgFromDict:
    def __init__(self, *args, **kwargs) -> None:
        self.OK = True
