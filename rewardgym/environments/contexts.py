from dataclasses import dataclass
from typing import Any

from ..input_handling import BaseInputHandler, PsychoPyInput
from ..logging import ExperimentLogger
from ..protocols import InputProtocol, LoggerProtocol

try:
    from psychopy.visual import Window
except ModuleNotFoundError:
    from ..psychopy_render.psychopy_stubs import Window

from ..psychopy_render import psychopy_stubs


@dataclass
class EnvironmentContext:
    window: Any | None = None
    input_handler: InputProtocol | None = None
    logger: LoggerProtocol | None = None
    mode: str = "psychopy-simulate"

    def __post_init__(self):
        if self.mode not in ["psychopy", "psychopy-simulate"]:
            raise ValueError(
                f"{self.mode} has to be 'psychopy' or 'psychopy-simulate'!"
            )
        if self.logger is None:
            self.logger = ExperimentLogger(file_name=None, clock=psychopy_stubs.Clock())

        if self.window is None:
            if self.mode == "psychopy":
                self.window = Window(
                    size=[1680, 1050],
                    fullscr=False,
                    color=[-0.5, -0.5, -0.5],
                    colorSpace="rgb",
                    units="pix",
                )
            elif self.mode == "psychopy-simulate":
                self.window = psychopy_stubs.Window()

        if self.input_handler is None:
            if self.mode == "psychopy-simulate":
                self.input_handler = BaseInputHandler()
            elif self.mode == "psychopy":
                self.input_handler = PsychoPyInput(self.logger.clock, win=self.window)

        self.win = self.window


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
