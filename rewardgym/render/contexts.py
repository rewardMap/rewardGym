from dataclasses import dataclass
from typing import Any

from ..input_handling import PsychoPyInput, SimulationInput
from ..logging import ExperimentLogger
from ..protocols import DisplayProtocol, InputProtocol, LoggerProtocol
from .backend_factories import PsychoPyFactory, PygameFactory, SimulationFactory
from .render_backend import PsychoPyDisplay, PygameDisplay, SimulationDisplay


@dataclass
class EnvironmentContext:
    window: Any | None = None
    input_handler: InputProtocol | None = None
    logger: LoggerProtocol | None = None
    mode: str = "simulation"
    render: DisplayProtocol | None = None
    stimuli: None = None
    random_state: None = None

    def __post_init__(self):
        if self.mode not in ["psychopy", "simulation", "pygame"]:
            raise ValueError(f"{self.mode} has to be 'psychopy' or 'simulation'!")

        if self.mode == "psychopy":
            self._setup_psychopy()

        elif self.mode == "simulation":
            self._setup_simulation()

        elif self.mode == "pygame":
            self._setup_pygame()

    def _setup_psychopy(self):
        if self.window is None:
            from psychopy.visual import Window

            self.window = Window(
                size=[1680, 1050],
                fullscr=False,
                color=[-0.5, -0.5, -0.5],
                colorSpace="rgb",
                units="pix",
            )

        if self.logger is None:
            from psychopy.core import Clock

            self.logger = ExperimentLogger(file_name=None, clock=Clock())

        if self.input_handler is None:
            self.input_handler = PsychoPyInput(self.logger.clock, win=self.window)

        if self.render is None:
            self.render = PsychoPyDisplay(window=self.window)

        self.stimuli = PsychoPyFactory()

    def _setup_simulation(self):
        if self.window is None:
            from ..stubs import Window

            self.window = Window()

        if self.input_handler is None:
            self.input_handler = SimulationInput()

        if self.logger is None:
            from ..stubs import Clock

            self.logger = ExperimentLogger(file_name=None, clock=Clock())

        if self.render is None:
            self.render = SimulationDisplay()

        self.stimuli = SimulationFactory()

    def _setup_pygame(self):
        if self.window is None:
            from .pygame_backend import PygameWindow

            self.window = PygameWindow()

        if self.input_handler is None:
            from ..input_handling import PygameInput

            self.input_handler = PygameInput(win=self.window)

        if self.logger is None:
            from psylog.interfaces import SystemClock

            self.logger = ExperimentLogger(file_name=None, clock=SystemClock())

        if self.render is None:
            self.render = PygameDisplay(self.window)

        self.stimuli = PygameFactory()

    @property
    def win(self):
        return self.window


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

    @property
    def render(self):
        return self.env_context.render

    @property
    def stimuli(self):
        return self.env_context.stimuli
