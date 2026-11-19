from ....protocols import FactoryProtocol


class PygameFactory(FactoryProtocol):
    def __init__(self):
        super().__init__()
        from .stimuli_pygame import PygameImageStim, PygameTextStim, PygameRect

        self.register("image", PygameImageStim)
        self.register("text", PygameTextStim)
        self.register("rectangle", PygameRect)
