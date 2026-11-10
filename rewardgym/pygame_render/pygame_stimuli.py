import numpy as np

from ..optional_dependencies import pygame


def psychopy_color_to_pygame(color):
    if color is None:
        return None

    if isinstance(color, str):
        return pygame.Color(color)

    if len(color) != 3:
        raise ValueError(f"Unsupported color: {color}")

    # PsychoPy rgb
    if all(isinstance(x, (int, float)) and -1 <= x <= 1 for x in color):
        return tuple(int((c + 1) * 127.5) for c in color)

    # already pygame-like
    return tuple(int(c) for c in color)


class PygameBaseStim:
    def __init__(
        self,
        win,
        name=None,
        pos=(0, 0),
        autoDraw: bool = False,
        opacity: float = 1.0,
        **kwargs,
    ):
        self.win = win
        self.name = name

        self.pos = pos
        self._autoDraw = False
        self.setAutoDraw(autoDraw)
        self.opacity = opacity

    @property
    def autoDraw(self):
        return self._autoDraw

    @autoDraw.setter
    def autoDraw(self, value):
        value = bool(value)

        if value == self._autoDraw:
            return

        self._autoDraw = value

        if value:
            self.win.register_auto_draw(self)
        else:
            self.win.unregister_auto_draw(self)

    def setPos(self, pos):
        self.pos = pos

    def setAutoDraw(self, value):
        self.autoDraw = value

        if value:
            self.win.register_auto_draw(self)
        else:
            self.win.unregister_auto_draw(self)

    def draw(self):
        self.win.register_draw(self)

    def _render(self):
        raise NotImplementedError

    def setOpacity(self, value):
        self.opacity = value


class PygameImageStim(PygameBaseStim):
    def __init__(
        self,
        win,
        image,
        pos=(0, 0),
        size=None,
        name=None,
        autoDraw: bool = False,
        opacity: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            win=win, name=name, pos=pos, autoDraw=autoDraw, opacity=opacity
        )

        if isinstance(image, str):
            surface = pygame.image.load(image).convert_alpha()

        elif isinstance(image, np.ndarray):
            image = image[::-1]
            surface = self._numpy_to_surface(image)

        else:
            raise TypeError(f"Unsupported image type: {type(image)}")

        if size is not None:
            surface = pygame.transform.smoothscale(
                surface,
                (
                    int(size[0]),
                    int(size[1]),
                ),
            )

        self.surface = surface
        self.size = self.surface.get_size()

    def setOpacity(self, value):
        self.opacity = float(value)

    def _render(self):
        surface = self.surface.copy()

        surface.set_alpha(
            max(
                0,
                min(
                    255,
                    int(self.opacity * 255),
                ),
            )
        )

        x, y = self.win.psychopy_to_pygame(self.pos)

        rect = surface.get_rect(center=(int(x), int(y)))

        self.win.screen.blit(
            surface,
            rect,
        )

    @staticmethod
    def _numpy_to_surface(image):
        image = np.asarray(image)

        if image.dtype != np.uint8:
            if np.issubdtype(
                image.dtype,
                np.floating,
            ):
                image = (
                    (image * 255)
                    .clip(
                        0,
                        255,
                    )
                    .astype(np.uint8)
                )
            else:
                image = image.astype(np.uint8)

        if image.ndim == 2:
            image = np.stack(
                [image] * 3,
                axis=-1,
            )

        if image.shape[-1] == 4:
            surface = pygame.image.frombuffer(
                image.tobytes(),
                (
                    image.shape[1],
                    image.shape[0],
                ),
                "RGBA",
            ).convert_alpha()

        elif image.shape[-1] == 3:
            surface = pygame.image.frombuffer(
                image.tobytes(),
                (
                    image.shape[1],
                    image.shape[0],
                ),
                "RGB",
            ).convert()

        else:
            raise ValueError(f"Unsupported image shape {image.shape}")

        return surface


class PygameRect(PygameBaseStim):
    def __init__(
        self,
        win,
        width,
        height,
        pos=(0, 0),
        lineColor="white",
        fillColor=None,
        lineWidth=1,
        name=None,
        autoDraw: bool = False,
        opacity: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            win=win, name=name, pos=pos, autoDraw=autoDraw, opacity=opacity
        )

        self.width = width
        self.height = height

        self.lineColor = psychopy_color_to_pygame(lineColor)

        self.fillColor = (
            psychopy_color_to_pygame(fillColor) if fillColor is not None else None
        )

        self.lineWidth = lineWidth

        self.size = (width, height)

    def _render(self):
        x, y = self.win.psychopy_to_pygame(self.pos)

        rect_surface = pygame.Surface(
            (int(self.width), int(self.height)),
            pygame.SRCALPHA,
        )
        alpha = int(self.opacity * 255)

        rect = pygame.Rect(
            0,
            0,
            int(self.width),
            int(self.height),
        )
        rect.center = (int(x), int(y))

        if self.fillColor is not None:
            fill_color = (
                *self.fillColor[:3],
                alpha,
            )

            pygame.draw.rect(
                rect_surface,
                fill_color,
                rect_surface.get_rect(),
            )

        if self.lineColor is not None and self.lineWidth > 0:
            line_color = (
                *self.lineColor[:3],
                alpha,
            )

            pygame.draw.rect(
                rect_surface,
                line_color,
                rect_surface.get_rect(),
                width=int(self.lineWidth),
            )

        rect = rect_surface.get_rect(center=(int(x), int(y)))

        self.win.screen.blit(
            rect_surface,
            rect,
        )


class PygameTextStim(PygameBaseStim):
    def __init__(
        self,
        win,
        text="",
        pos=(0, 0),
        color="white",
        height=40,
        font=None,
        name=None,
        alignText=None,
        anchorHoriz=None,
        units=None,
        autoDraw: bool = False,
        opacity: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            win=win, name=name, pos=pos, autoDraw=autoDraw, opacity=opacity
        )

        self.text = text

        self.color = psychopy_color_to_pygame(color)

        self.height = int(height)

        self.font_name = font

        self.font = pygame.font.SysFont(
            font,
            self.height,
        )

        self.alignText = alignText
        self.anchorHoriz = anchorHoriz
        self.units = units

    def setText(self, text):
        self.text = text

    def _render(self):
        surface = self.font.render(
            str(self.text),
            True,
            self.color,
        )

        alpha = int(self.opacity * 255)
        surface.set_alpha(alpha)

        x, y = self.win.psychopy_to_pygame(self.pos)

        rect = surface.get_rect(center=(int(x), int(y)))

        self.win.screen.blit(
            surface,
            rect,
        )
