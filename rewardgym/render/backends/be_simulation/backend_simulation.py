from collections.abc import Callable
from typing import Any

from ....logging import ExperimentLogger
from ....protocols import ClockProtocol, DisplayProtocol
from ...contexts import EnvironmentContext
from ...input_handling import BaseInputHandler
from ...timing import simulation_wait
from ..backend_base import FlipValue, RewardGymBackend
from .factory_simulation import SimulationFactory


class SimulationBackend(RewardGymBackend):
    mode = "simulation"

    def setup(self, context: EnvironmentContext):
        if context.window is None:
            context.window = Window()

        if context.input_handler is None:
            context.input_handler = SimulationInput()

        if context.logger is None:
            context.logger = ExperimentLogger(file_name=None, clock=Clock())

        if context.render is None:
            context.render = SimulationDisplay()

        context.stimuli = SimulationFactory()


class SimulationDisplay(DisplayProtocol):
    def __init__(self, **kwargs):
        pass

    def flip(self) -> FlipValue:
        return FlipValue()

    def schedule_on_flip(self, callback, *args, **kwargs) -> Any:
        return None

    def wait(self, **kwargs) -> Any:
        return simulation_wait(**kwargs)


class SimulationInput(BaseInputHandler):
    def get_keys(self) -> list[tuple[str, float]]:
        return []


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

    def flip(self) -> FlipValue:
        return FlipValue()

    def close(self):
        pass

    def callOnFlip(self, function: Callable, *args, **kwargs):
        pass
