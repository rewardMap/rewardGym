from dataclasses import dataclass
from typing import Any

from ..protocols import DisplayProtocol, InputProtocol, LoggerProtocol


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
        from .backends import get_backends

        backend_registry = get_backends()

        if self.mode not in backend_registry:
            raise ValueError(
                f"{self.mode} has to be in {list(backend_registry.keys())}!"
            )

        backend_registry[self.mode]().setup(self)

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
