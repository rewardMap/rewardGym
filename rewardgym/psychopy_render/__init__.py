import os

from .logger import ExperimentLogger, SimulationLogger
from .utils import get_psychopy_info

STIMPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../taskdata/stimuli/")
)
