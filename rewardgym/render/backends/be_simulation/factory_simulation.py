from ..backend_base import BaseFactory
from .stimuli_simulation import SimImageStim, SimRect, SimTextStim


class SimulationFactory(BaseFactory):
    def __init__(self):
        super().__init__()
        self.register("image", SimImageStim)
        self.register("text", SimTextStim)
        self.register("rectangle", SimRect)
