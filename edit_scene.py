import pygame
from pygame.locals import *

from Ifunctions import *
from story import serifs


class EditScene:
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "edit"

        self.screen = screen
        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.chapter = 0
        self.camera = [0, 0]
        self.is_end = False
        self.frame = 0

    def mainloop(self) -> None:
        # print("test")

        self.screen.fill((255, 201, 224))

        # print(serifs[self.chapter])

        speed = 20

        if K_RIGHT in keyboard["pressed"]:
            self.camera[0] -= speed
        elif K_LEFT in keyboard["pressed"]:
            self.camera[0] += speed

        if K_UP in keyboard["pressed"]:
            self.camera[1] += speed
        elif K_DOWN in keyboard["pressed"]:
            self.camera[1] -= speed

        i = 0
        layer = 0
        for branch in serifs[self.chapter].regex_dict:
            if layer != len(branch):
                i = 0
                layer = len(branch)

            clicked = Ibutton(
                self.screen,
                self.font,
                (255, 255, 255),
                (255, 255, 255),
                100 * i + self.camera[0],
                50 * layer + self.camera[1],
                100,
                50,
                branch,
                text_align="left",
            )
            i += 1

        pygame.display.update()  # 画面更新
