import math
import pygame
from pygame.locals import *

from Ifunctions import *

moji = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろやゆよわをがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょっーん消終"


class NameScene:
    def __init__(self, screen: pygame.Surface, pushed: list[int], mouse: dict) -> None:
        self.scene_name = "name"
        self.screen = screen
        self.mouse = mouse
        self.pushed = pushed

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 48)

        self.start()

    def start(self):

        self.is_end = False

        self.num = 0
        self.name = "もこた"

    def mainloop(self) -> None:
        self.screen.fill((255, 201, 214))

        if K_RIGHT in self.pushed:
            self.num += 1
            self.num %= len(moji)
        elif K_LEFT in self.pushed:
            self.num += len(moji) - 1
            self.num %= len(moji)
        elif K_DOWN in self.pushed:
            self.num += 15
            self.num %= len(moji)
        elif K_UP in self.pushed:
            self.num += len(moji) - 15
            self.num %= len(moji)
        elif K_RETURN in self.pushed or K_SPACE in self.pushed:
            if self.num == len(moji) - 1:
                if len(self.name) > 0:
                    self.is_end = True
                    return self.name
            elif self.num == len(moji) - 2:
                if len(self.name) > 0:
                    self.name = self.name[:-1]

            elif len(self.name) < 7:
                self.name += moji[self.num]

        elif K_BACKSPACE in self.pushed or K_ESCAPE in self.pushed:
            if len(self.name) > 0:
                self.name = self.name[:-1]

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            40,
            30,
            "名前を入力:",
        )

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            440,
            30,
            self.name,
        )

        # Itext(
        #     self.screen,
        #     self.font,
        #     (255, 255, 255),
        #     40,
        #     100,
        #     moji,
        #     max_width=740,
        # )

        for i, char in enumerate(moji):
            size = 48
            selected = Ibutton(
                self.mouse,
                self.screen,
                self.font,
                (255, 255, 255),
                (255, 255, 255),
                40 + (i % 15) * size,
                112 + math.floor(i / 15) * self.font.get_height(),
                size,
                size,
                char,
                line_width=0,
            )

            if selected:
                self.num = i
                if self.num == len(moji) - 1:
                    if len(self.name) > 0:
                        self.is_end = True
                        return self.name
                elif self.num == len(moji) - 2:
                    if len(self.name) > 0:
                        self.name = self.name[:-1]

                elif len(self.name) < 7:
                    self.name += moji[self.num]

        m = ";" * math.floor(self.num / 15) + "  " * (self.num % 15) + moji[self.num]

        Itext(
            self.screen,
            self.font,
            (255, 240, 0),
            40,
            100,
            m,
        )

        pygame.display.update()  # 画面更新
