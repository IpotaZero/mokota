import pygame
from pygame.locals import *

from Ifunctions import *


class DarkeningScene:
    def __init__(self) -> None:
        self.scene_name = "darkening"

        self.screen = pygame.display.get_surface()

        self.start()

    def start(self):
        self.is_end = False
        self.frame = 0

    def mainloop(self) -> None:
        scr = pygame.Surface(
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
            flags=pygame.SRCALPHA,
        )
        scr.fill((0, 0, 0, 255 * self.frame / 120))

        self.screen.blit(scr, screen_option["offset"])

        pygame.display.update()  # 画面更新

        self.frame += 1

        if self.frame == 60:
            self.is_end = True
