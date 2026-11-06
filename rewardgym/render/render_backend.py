from typing import Any

from ..protocols import DisplayProtocol
from ..timing import simulation_wait, wait


class SimulationDisplay(DisplayProtocol):
    def __init__(self, **kwargs):
        pass

    def flip(self) -> Any:
        return None

    def schedule_on_flip(self, callback, *args, **kwargs) -> Any:
        return None

    def wait(self, **kwargs) -> Any:
        return simulation_wait(**kwargs)


class PsychoPyDisplay(DisplayProtocol):
    def __init__(self, *, window, **kwargs):
        self.win = window

    def flip(self) -> Any:
        return self.win.flip()

    def schedule_on_flip(self, callback, *args, **kwargs) -> Any:
        return self.win.callOnFlip(callable, *args, **kwargs)

    def wait(self, **kwargs):
        return wait(**kwargs)


class PygameDisplay(DisplayProtocol):
    def __init__(self, window, **kwargs):
        self.win = window

    def flip(self):
        self.win.flip()

    def schedule_on_flip(
        self,
        callback,
        *args,
        **kwargs,
    ):
        self.win.callOnFlip(
            callback,
            *args,
            **kwargs,
        )

    def wait(self, *args, **kwargs):
        return wait(
            *args,
            **kwargs,
        )
