from ..protocols import FactoryProtocol, WindowProtocol
from .stimulus_classes import Stimuli, StimulusDefinition
from .stimulus_stubs import SimImageStim, SimRect, SimTextStim


def setup_stimulus(
    window: WindowProtocol, factory: FactoryProtocol, definition: StimulusDefinition
):
    if definition.setup_protocol == Stimuli.IMAGE:
        return factory.image(win=window, **definition.get_kwargs())

    elif definition.setup_protocol == Stimuli.RECTANGLE:
        return factory.rectangle(win=window, **definition.get_kwargs())

    elif definition.setup_protocol == Stimuli.TEXT:
        return factory.text(win=window, **definition.get_kwargs())

    else:
        raise NotImplementedError(
            f"{definition.setup_protocol}, is not implemented in the present factory!"
        )


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

        return ImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from psychopy.visual.rect import Rect

        return Rect(**kwargs)

    def text(self, **kwargs):
        from psychopy.visual import TextStim

        return TextStim(**kwargs)


class PygameFactory(FactoryProtocol):
    def image(self, **kwargs):
        from ..pygame_render.pygame_stimuli import PygameImageStim

        return PygameImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from ..pygame_render.pygame_stimuli import PygameRect

        return PygameRect(**kwargs)

    def text(self, **kwargs):
        from ..pygame_render.pygame_stimuli import PygameTextStim

        return PygameTextStim(**kwargs)
