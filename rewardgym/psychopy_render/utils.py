def get_psychopy_info(task: str = "hcp"):

    if task == "hcp":
        from .hcp import info_dict
    elif task == "mid":
        from .mid import info_dict
    elif task == "risk-sensitive":
        from .risk_sensitive import info_dict
    elif task == "two-step":
        from .two_step import info_dict
    elif task == "gonogo":
        from .gonogo import info_dict
    elif task == "posner":
        from .posner import info_dict

    return info_dict
