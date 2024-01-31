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

    def __call__(self, window, clock=None, condition=None):

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

    def __call__(self, window=None, clock=None, condition=None):

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
