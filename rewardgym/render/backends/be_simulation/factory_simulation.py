from ....protocols import FactoryProtocol
from .stimuli_simulation import SimImageStim, SimRect, SimTextStim


class SimulationFactory(FactoryProtocol):
    def image(self, **kwargs):
        return SimImageStim(**kwargs)

    def rectangle(self, **kwargs):
        return SimRect(**kwargs)

    def text(self, **kwargs):
        return SimTextStim(**kwargs)
