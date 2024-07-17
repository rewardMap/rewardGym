def get_psychopy_info(task: str = "hcp", **kwargs):

    if task == "hcp":
        from .hcp import get_info_dict
    elif task == "mid":
        from .mid import get_info_dict
    elif task == "risk-sensitive":
        from .risk_sensitive import get_info_dict
    elif task == "two-step":
        from .two_step import get_info_dict
    elif task == "gonogo":
        from .gonogo import get_info_dict
    elif task == "posner":
        from .posner import get_info_dict

    return get_info_dict(**kwargs)
