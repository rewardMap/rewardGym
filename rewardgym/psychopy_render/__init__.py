import os

from .logger import ExperimentLogger
from .stimuli import WaitTime
from .utils import get_psychopy_info

STIMPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../template_stimuli/")
)
