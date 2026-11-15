from ....protocols import FactoryProtocol


class PygameFactory(FactoryProtocol):
    def image(self, **kwargs):
        from .stimuli_pygame import PygameImageStim

        return PygameImageStim(**kwargs)

    def rectangle(self, **kwargs):
        from .stimuli_pygame import PygameRect

        return PygameRect(**kwargs)

    def text(self, **kwargs):
        from .stimuli_pygame import PygameTextStim

        return PygameTextStim(**kwargs)
