import warnings

from .gonogo_instructions import gonogo_instructions
from .hcp_instructions import hcp_instructions
from .mid_instructions import mid_instructions
from .posner_instructions import posner_instructions
from .risksensitive_instructions import risksensitive_instructions
from .twostep_instructions import twostep_instructions


def get_instructions(task: str):
    if task == "two-step":
        return twostep_instructions
    elif task == "hcp":
        return hcp_instructions
    elif task == "gonogo":
        return gonogo_instructions
    elif task == "mid":
        return mid_instructions
    elif task == "posner":
        return posner_instructions
    elif task == "risk-sensitive":
        return risksensitive_instructions
    else:
        warnings.warn("Instructions are not yet implemented.")
        return False
