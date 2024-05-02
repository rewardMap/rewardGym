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
