import math
import pygame
from pygame.locals import *

from Ifunctions import *

moji = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ! ? - OK"


class NameScene:
    def __init__(self, screen: pygame.Surface, pushed: list[int]) -> None:
        self.scene_name = "name"
        self.screen = screen
        self.pushed = pushed

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 48)

        self.start()

    def start(self):

        self.is_end = False

        self.num = 0
        self.name = "MOKOTA"

    def mainloop(self) -> None:
        self.screen.fill((0, 0, 0))  # 背景を黒

        if K_RIGHT in self.pushed:
            self.num += 1
            self.num %= 30
        elif K_LEFT in self.pushed:
            self.num += len(moji) - 1
            self.num %= 30
        elif K_DOWN in self.pushed:
            self.num += 15
            self.num %= 30
        elif K_UP in self.pushed:
            self.num += len(moji) - 15
            self.num %= 30
        elif K_RETURN in self.pushed or K_SPACE in self.pushed:
            if self.num == 29:
                if len(self.name) > 0:
                    self.is_end = True
                    return self.name

            elif len(self.name) < 12:
                self.name += moji[self.num * 2]

        elif K_BACKSPACE in self.pushed or K_ESCAPE in self.pushed:
            if len(self.name) > 0:
                self.name = self.name[:-1]

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            30,
            30,
            "Enter Your Name",
        )

        Itext(
            self.screen,
            self.font2,
            (255, 255, 255),
            400,
            30,
            self.name,
        )

        Itext(
            self.screen,
            self.font2,
            (255, 255, 255),
            40,
            100,
            moji,
            max_width=740,
        )

        m = (
            ";" * math.floor(self.num / 15)
            + "  " * (self.num % 15)
            + moji[self.num * 2]
        )

        if self.num == 29:
            m = ";" * math.floor(self.num / 15) + "  " * (self.num % 15) + "OK"

        Itext(
            self.screen,
            self.font2,
            (255, 255, 0),
            40,
            100,
            m,
        )

        pygame.display.update()  # 画面更新
