from .stimulus_stubs import SimImageStim, SimRect, SimTextStim


class SimulationFactory:
    def image(self, **kwargs):
        return SimImageStim(**kwargs)

    def rectangle(self, **kwargs):
        return SimRect(**kwargs)

    def text(self, **kwargs):
        return SimTextStim(**kwargs)


class PsychoPyFactory:
    def image(self, **kwargs):
        from psychopy.visual import ImageStim

        return ImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from psychopy.visual.rect import Rect

        return Rect(**kwargs)

    def text(self, **kwargs):
        from psychopy.visual import TextStim

        return TextStim(**kwargs)
