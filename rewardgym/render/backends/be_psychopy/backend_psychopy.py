from typing import Any

from psychopy import core
from psychopy.visual import Window

from ....logging import ExperimentLogger
from ....protocols import DisplayProtocol, KeyboardProtocol
from ...contexts import EnvironmentContext
from ...input_handling import BaseInputHandler
from ...events import wait
from ..backend_base import FlipValue, RewardGymBackend
from .factory_psychopy import PsychoPyFactory


class PsychoPyBackend(RewardGymBackend):
    mode = "psychopy"

    def setup(self, context: EnvironmentContext):
        if context.window is None:
            context.window = Window(
                size=[1680, 1050],
                fullscr=False,
                color=[-0.5, -0.5, -0.5],
                colorSpace="rgb",
                units="pix",
            )

        if context.logger is None:
            from psychopy.core import Clock

            context.logger = ExperimentLogger(file_name=None, clock=Clock())

        if context.input_handler is None:
            context.input_handler = PsychoPyInput(
                context.logger.clock, win=context.window
            )

        if context.render is None:
            context.render = PsychoPyDisplay(window=context.window)

        context.stimuli = PsychoPyFactory()


class PsychoPyDisplay(DisplayProtocol):
    def __init__(self, *, window, **kwargs):
        self.win = window

    def flip(self) -> FlipValue:
        return FlipValue(timestamp=self.win.flip())

    def schedule_on_flip(self, callback, *args, **kwargs) -> Any:
        return self.win.callOnFlip(callable, *args, **kwargs)

    def wait(self, **kwargs):
        return wait(**kwargs)


class PsychoPyInput(BaseInputHandler):
    def __init__(
        self,
        clock,
        keyboard: KeyboardProtocol | None = None,
        kill_switch: str = "q",
        mr_trigger: str = "5",
        repetition_time: float = 2,
        win=None,
    ) -> None:
        if keyboard is None:
            from psychopy.hardware.keyboard import Keyboard

            keyboard = Keyboard(clock=clock)

        super().__init__(
            kill_switch=kill_switch,
            mr_trigger=mr_trigger,
            repetition_time=repetition_time,
        )

        self.interface = keyboard
        self.win = win

    def get_keys(self) -> list[tuple[str, float]]:
        keys = [(i.name, i.rt) for i in self.interface.getKeys()]
        return keys

    def _close(self):
        if self.win is not None:
            self.win.close()
        if core is not None:
            core.quit()
