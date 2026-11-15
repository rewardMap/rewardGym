from ...protocols import FactoryProtocol, WindowProtocol
from ..contexts import EnvironmentContext
from ..stimulus_definitions import Stimuli, StimulusDefinition


class RewardGymBackend:
    mode: str

    def setup(self, context: EnvironmentContext):
        raise NotImplementedError


def setup_stimulus(
    window: WindowProtocol, factory: FactoryProtocol, definition: StimulusDefinition
):
    if definition.setup_protocol == Stimuli.IMAGE:
        stim = factory.image(win=window, **definition.get_kwargs())

    elif definition.setup_protocol == Stimuli.RECTANGLE:
        stim = factory.rectangle(win=window, **definition.get_kwargs())

    elif definition.setup_protocol == Stimuli.TEXT:
        stim = factory.text(win=window, **definition.get_kwargs())

    else:
        raise NotImplementedError(
            f"{definition.setup_protocol}, is not implemented in the present factory!"
        )

    if definition.autoDraw:
        stim.setAutoDraw(True)

    return stim
