import pygame
from pygame.locals import *

from Ifunctions import *
from scene import Scene


class DarkeningScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "darkening"

        self.screen = screen
        super().__init__(screen)

        self.start()

    def start(self):
        self.is_end = False
        self.frame = 0

    def mainloop(self) -> None:
        scr = pygame.Surface((1200, 800), flags=pygame.SRCALPHA)
        scr.fill((0, 0, 0, 255 * self.frame / 120))

        self.screen.blit(scr, (0, 0))

        self.frame += 1

        if self.frame == 60:
            self.is_end = True
