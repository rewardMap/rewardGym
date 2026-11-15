"""
Stubs, so that environments can be used together with PsychoPy, not requiring
any installation of other packages into the PsychoPy env.
"""

from .render.backends.be_simulation.stimuli_simulation import SimBaseStim
from .render.backends.be_simulation.stimuli_simulation import SimImageStim as ImageStim
from .render.backends.be_simulation.stimuli_simulation import SimRect as Rect
from .render.backends.be_simulation.stimuli_simulation import SimTextStim as TextStim
from .render.backends.be_simulation.backend_simulation import Clock, Window

__all__ = ["ImageStim", "Rect", "TextStim", "Clock", "Window"]


class Env:
    def __init__(self):
        pass


class Discrete:
    def __init__(self, n_states):
        self.n_states = n_states


class Surface:
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
