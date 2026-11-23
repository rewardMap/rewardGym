from dataclasses import dataclass
from typing import Any

from ..protocols import ClockProtocol, DisplayProtocol, InputProtocol, LoggerProtocol
from ..validation import ClockMismatchError, check_availability


@dataclass
class EnvironmentContext:
    window: Any | None = None
    input_handler: InputProtocol | None = None
    logger: LoggerProtocol | None = None
    mode: str = "simulation"
    render: DisplayProtocol | None = None
    stimuli: None = None
    random_state: None = None
    clock: None | ClockProtocol = None

    def __post_init__(self):
        from .backends import BACKENDS

        check_availability(self.mode, "backend")

        BACKENDS[self.mode]().setup(self)

        self.validate_clocks()

    @property
    def win(self):
        return self.window

    def get_time(self):
        return self.clock.getTime()

    def reset_time(self):
        self.clock.reset()

    def validate_clocks(self):
        if hasattr(self.logger, "clock") and self.logger.clock is not self.clock:
            raise ClockMismatchError(
                "Make sure the logger and environment use the same clock!"
            )

        if hasattr(self.render, "clock") and self.render.clock is not self.clock:
            raise ClockMismatchError(
                "Make sure the DisplayClass and the environment use the same clock!"
            )

        if (
            hasattr(self.input_handler, "clock")
            and self.input_handler.clock is not self.clock
        ):
            raise ClockMismatchError(
                "Make sure the input_handler and the environment use the same clock!"
            )


@dataclass
class StepContext:
    env_context: EnvironmentContext
    condition: Any
    total_reward: Any
    reward: Any
    location: Any
    previous_action: Any
    info: dict
    reaction_time: float | None = None
    tracker: Any | None = None

    @property
    def win(self):
        return self.env_context.window

    @property
    def logger(self):
        return self.env_context.logger

    @property
    def input_handler(self):
        return self.env_context.input_handler

    @property
    def rt(self):
        return self.reaction_time

    @property
    def key(self):
        return self.previous_action

    @property
    def render(self):
        return self.env_context.render

    @property
    def stimuli(self):
        return self.env_context.stimuli

    def get_time(self):
        return self.env_context.get_time()

    @property
    def clock(self):
        return self.env_context.clock
