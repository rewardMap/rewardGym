class Empty:
    def __init__(self, *args, **kwargs):
        pass


def empty_func(*args, **kwargs):
    return None, None


BaseAction = Empty
BaseDisplay = Empty
BaseText = Empty
TimedAction = Empty
