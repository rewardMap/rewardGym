from ....protocols import FactoryProtocol


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
