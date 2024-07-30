import pygame
from pygame.locals import *

from Ifunctions import *
from mode_text import ModeText
from mode_save import ModeSave
from mode_log import ModeLog
from mode_pause import ModePause


class SceneMain(ModeText, ModeSave, ModeLog, ModePause):
    def mainloop(self):
        self.layer_background.fill((0, 0, 0))  # 背景を黒
        for image in self.images.values():
            if image["is_shown"]:
                self.layer_background.blit(
                    pygame.transform.scale(image["img"], image["size"]), image["pos"]
                )

        self.layer_buttons.fill((0, 0, 0, 0))  # 透明

        self.mainloop_log()
        self.mainloop_save()
        self.mainloop_pause()
        self.mainloop_text()

        if self.frame == 0:
            return

        self.buffer_screen.blit(self.layer_background, (0, 0))
        self.buffer_screen.blit(self.layer_buttons, (0, 0))

        scr = pygame.transform.smoothscale(
            self.buffer_screen,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )
        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()  # 画面更新
