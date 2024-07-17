import pygame
from pygame.locals import *

from Ifunctions import *


class DarkeningScene:
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "darkening"

        self.screen = screen

        self.start()

    def start(self):
        self.is_end = False
        self.frame = 0

    def mainloop(self) -> None:
        scr = pygame.Surface((1200, 800), flags=pygame.SRCALPHA)
        scr.fill((0, 0, 0, 255 * self.frame / 120))

        self.screen.blit(scr, (0, 0))

        pygame.display.update()  # 画面更新

        self.frame += 1

        if self.frame == 60:
            self.is_end = True
