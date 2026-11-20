from ..backend_base import BaseFactory


class PygameFactory(BaseFactory):
    def __init__(self):
        super().__init__()
        from .stimuli_pygame import PygameImageStim, PygameRect, PygameTextStim

        self.register("image", PygameImageStim)
        self.register("text", PygameTextStim)
        self.register("rectangle", PygameRect)
