from ..protocols import FactoryProtocol, WindowProtocol
from .stimulus_definitions import Stimuli, StimulusDefinition
from .simulation_backend import SimImageStim, SimRect, SimTextStim


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


class SimulationFactory(FactoryProtocol):
    def image(self, **kwargs):
        return SimImageStim(**kwargs)

    def rectangle(self, **kwargs):
        return SimRect(**kwargs)

    def text(self, **kwargs):
        return SimTextStim(**kwargs)


class PsychoPyFactory(FactoryProtocol):
    def image(self, **kwargs):
        from psychopy.visual import ImageStim

        if not isinstance(kwargs["image"], str):
            img = kwargs["image"]
            if "size" not in kwargs:
                kwargs["size"] = (img.shape[1], img.shape[0])

        return ImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from psychopy.visual.rect import Rect

        return Rect(**kwargs)

    def text(self, **kwargs):
        from psychopy.visual import TextStim

        return TextStim(**kwargs)


class PygameFactory(FactoryProtocol):
    def image(self, **kwargs):
        from .pygame_backend import PygameImageStim

        return PygameImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from .pygame_backend import PygameRect

        return PygameRect(**kwargs)

    def text(self, **kwargs):
        from .pygame_backend import PygameTextStim

        return PygameTextStim(**kwargs)
