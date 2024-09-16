class Clock:
    def __init__(self):
        self.time = 0

    def getTime(self):
        return self.time


class Window:
    def __init__(self, **kwargs):
        pass

    def flip(self):
        pass

    def close(self):
        pass


class ImageStim:
    def __init__(self, *args, **kwargs) -> None:
        pass


class TextStim(ImageStim):
    pass


class Rect(ImageStim):
    pass


def getKeys(**kwargs):
    pass


def quit():
    pass


class Dlg:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def addField(self, *args, **kwargs):
        pass

    def show(self):
        # Just for working with the gui dialog
        return ["Yes"]


class DlgFromDict:
    def __init__(self, *args, **kwargs) -> None:
        self.OK = True
