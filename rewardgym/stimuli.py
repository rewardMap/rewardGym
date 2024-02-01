import sys

import pygame


class BaseDisplay:
    def __init__(self, image, time, name=None, background=(127, 127, 127)):
        self.image_path = image
        self.time = time
        self.image = None
        self.name = name
        self.display_type = "image"
        self.background = background

    def __call__(self, window, clock=None, condition=None, **kwargs):

        window.fill(self.background)

        if self.image_path is not None:
            if self.image is None:
                self.image = pygame.image.load(self.image_path).convert()

            window.blit(
                self.image, self.image.get_rect(center=window.get_rect().center)
            )

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.time)

        return None


class BaseAction:
    def __init__(self, action_map={pygame.K_LEFT: 0, pygame.K_RIGHT: 1}, name=None):
        self.action_map = action_map
        self.allowed_keys = action_map.keys()
        self.display_type = "action"
        self.name = name

    def __call__(self, window=None, clock=None, condition=None, **kwargs):

        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()

                    elif event.key in self.allowed_keys:
                        return self.action_map[event.key]


class BaseText:
    def __init__(
        self,
        text,
        time,
        name=None,
        background=(127, 127, 127),
        fontcolor=(0, 0, 0),
        fontsize=36,
        textposition=(0, 0),
    ):
        self.font = None
        self.text = text
        self.time = time
        self.name = name
        self.display_type = "text"
        self.textposition = textposition
        self.background = background
        self.fontsize = fontsize
        self.text_surface = None
        self.fontcolor = fontcolor

    def __call__(self, window, clock=None, condition=None, **kwargs):

        window.fill(self.background)

        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
            self.text_surface = self.font.render(self.text, True, self.fontcolor)
            self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.time)

        return None
