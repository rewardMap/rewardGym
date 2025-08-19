try:
    from psychopy.visual import Window
except ModuleNotFoundError:
    from .psychopy_stubs import Window


class PhotoWindow(Window):
    def flip(self):
        super().flip()
        self.getMovieFrame()
