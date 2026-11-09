class SimBaseStim:
    def __init__(self, win=None, name=None, **kwargs):
        self.autoDraw = False
        self.win = win
        self.name = name

    def setAutoDraw(self, auto_draw: bool):
        self.autoDraw = auto_draw

    def setPos(self, new_pos):
        self.pos = new_pos

    def draw(self):
        pass


class SimImageStim(SimBaseStim):
    def __init__(
        self,
        win,
        name: str | None = None,
        image: str | None = None,
        pos: tuple | None = None,
        size: tuple | None = None,
        autoDraw=None,
    ) -> None:
        super().__init__(win=win, name=name, autoDraw=autoDraw)

        self.image = image

        self.pos = pos

        if self.pos is None:
            self.pos = (0, 0)

        if size is None:
            self.size = (100, 100)
        else:
            self.size = size

        self.opacity = 1.0

    def setOpacity(self, newOpacity):
        self.opacity = newOpacity


class SimTextStim(SimBaseStim):
    def __init__(
        self,
        win,
        name=None,
        text=None,
        color=None,
        height=None,
        pos=None,
        font=None,
        alignText=None,
        anchorHoriz=None,
        units=None,
        autoDraw=None,
    ):
        super().__init__(win=win, name=name, autoDraw=autoDraw)

        self.text = text
        self.color = color
        self.height = height
        self.pos = pos
        self.font = font
        self.alignText = alignText
        self.anchorHoriz = anchorHoriz
        self.units = units

    def setText(self, new_text: str | None):
        self.text = new_text


class SimRect(SimBaseStim):
    def __init__(
        self,
        win,
        name=None,
        width=None,
        height=None,
        lineColor=None,
        fillColor=None,
        lineWidth=None,
        pos=None,
        units=None,
        autoDraw=None,
    ):
        super().__init__(win=win, name=name, autoDraw=autoDraw)

        self.width = width
        self.height = height
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.lineWidth = lineWidth
        self.pos = pos
        self.units = units
