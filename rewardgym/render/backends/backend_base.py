from dataclasses import dataclass

from ...protocols import FactoryProtocol, WindowProtocol
from ...validation import UnknownStimulusError
from ..contexts import EnvironmentContext
from ..stimulus_definitions import StimulusDefinition


@dataclass
class FlipValue:
    timestamp: float | None = None
    frame: float | None = None


class RewardGymBackend:
    mode: str

    def setup(self, context: EnvironmentContext):
        raise NotImplementedError


class BaseFactory(FactoryProtocol):
    def __init__(self):
        self._registry = {}

    def register(self, name: str, stimulus_or_function):
        if name in self._registry:
            raise ValueError(f"{name} has already been registered in factory.")

        self._registry[name] = stimulus_or_function

    def __getitem__(self, name):
        return self._registry[name]

    def check_available(self, name):
        if name not in self._registry:
            raise UnknownStimulusError(
                f"{name} not registered in registry. Use factory.get_available for a list of stimuli."
            )

    def get_available(self):
        return list(self._registry.keys())


def setup_stimulus(
    window: WindowProtocol, factory: FactoryProtocol, definition: StimulusDefinition
):
    factory.check_available(definition.stimulus_type)

    stim = factory[definition.stimulus_type](win=window, **definition.get_kwargs())

    if definition.autoDraw:
        stim.setAutoDraw(True)

    return stim
