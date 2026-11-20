from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ....logging import ExperimentLogger
from ....protocols import ClockProtocol, DisplayProtocol
from ...contexts import EnvironmentContext
from ...events import wait
from ...input_handling import BaseInputHandler
from ..backend_base import FlipValue, RewardGymBackend
from .factory_simulation import SimulationFactory


class SimulationBackend(RewardGymBackend):
    mode = "simulation"

    def setup(self, context: EnvironmentContext):
        if context.clock is None:
            context.clock = Clock()

        if context.window is None:
            context.window = Window()

        if context.logger is None:
            context.logger = ExperimentLogger(file_name=None, clock=context.clock)

        if context.input_handler is None:
            context.input_handler = SimulationInput(context.clock)

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
        return wait(**kwargs)


@dataclass(order=True)
class ScheduledResponse:
    scheduled_time: float
    key: str


class SimulationInput(BaseInputHandler):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.response_log = []

    def get_keys(self) -> list[tuple[str, float]]:
        responses = []

        current_time = self.clock.getTime()
        while self.response_log and self.response_log[0].scheduled_time <= current_time:
            response = self.response_log.pop(0)

            responses.append((response.key, response.scheduled_time))

        return responses

    def add_response(self, key, response_time):
        self.response_log.append(
            ScheduledResponse(response_time + self.clock.getTime(), key)
        )
        self.response_log.sort()

    def next_response_time(self):
        if not self.response_log:
            return None

        return max([self.response_log[0].scheduled_time - self.clock.getTime(), 0])


class Clock(ClockProtocol):
    def __init__(self):
        self.time = 0

    def getTime(self):
        return self.time

    def reset(self):
        pass

    def advance_time(self, dt: float):
        self.time += dt


class Window:
    def __init__(self, **kwargs):
        pass

    def flip(self) -> FlipValue:
        return FlipValue()

    def close(self):
        pass

    def callOnFlip(self, function: Callable, *args, **kwargs):
        pass
