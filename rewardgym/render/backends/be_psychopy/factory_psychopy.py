from ..backend_base import BaseFactory


class PsychoPyFactory(BaseFactory):
    def __init__(self):
        from psychopy import visual

        super().__init__()
        self.register("image", self._create_image)
        self.register("text", visual.TextStim)
        self.register("rectangle", visual.rect.Rect)

    @staticmethod
    def _create_image(**kwargs):
        from psychopy.visual import ImageStim

        if not isinstance(kwargs["image"], str):
            img = kwargs["image"]
            if "size" not in kwargs:
                kwargs["size"] = (img.shape[1], img.shape[0])

        return ImageStim(**kwargs)
