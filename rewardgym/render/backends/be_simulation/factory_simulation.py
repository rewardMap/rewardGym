from .stimuli_simulation import SimImageStim, SimRect, SimTextStim
from ....protocols import FactoryProtocol


class SimulationFactory(FactoryProtocol):
    def image(self, **kwargs):
        return SimImageStim(**kwargs)

    def rectangle(self, **kwargs):
        return SimRect(**kwargs)

    def text(self, **kwargs):
        return SimTextStim(**kwargs)
