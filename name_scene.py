import math
import pygame
from pygame.locals import *

from Ifunctions import *

moji = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろやゆよわをがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょっんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモラリルレロヤユヨワヲガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポァィゥェォャュョッンー消終"


class NameScene:
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "name"
        self.screen = screen

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 48)

        self.start()

    def start(self):

        self.is_end = False

        self.num = 0
        self.name = "もこた"

    def mainloop(self):
        row_letter_num = 20
        self.screen.fill((255, 201, 224))

        if K_RIGHT in keyboard["long_pressed"]:
            self.num += 1
            self.num %= len(moji)
        elif K_LEFT in keyboard["long_pressed"]:
            self.num += len(moji) - 1
            self.num %= len(moji)
        elif K_DOWN in keyboard["long_pressed"]:
            self.num += row_letter_num
            self.num %= len(moji)
        elif K_UP in keyboard["long_pressed"]:
            self.num += len(moji) - row_letter_num
            self.num %= len(moji)
        elif K_RETURN in keyboard["pushed"] or K_SPACE in keyboard["pushed"]:
            if self.num == len(moji) - 1:
                if len(self.name) > 0:
                    self.is_end = True
                    return self.name
            elif self.num == len(moji) - 2:
                if len(self.name) > 0:
                    self.name = self.name[:-1]

            elif len(self.name) < 7:
                self.name += moji[self.num]

        elif K_BACKSPACE in keyboard["pushed"] or K_ESCAPE in keyboard["pushed"]:
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
            size = 56

            x = 40 + (i % row_letter_num) * size
            y = 112 + math.floor(i / row_letter_num) * self.font.get_height()

            selected = Ibutton(
                self.screen,
                self.font,
                (255, 255, 255),
                (255, 255, 255),
                x,
                y,
                size,
                size,
                char,
                line_width=0,
            )

            if i == self.num:
                Itext(
                    self.screen,
                    self.font,
                    (255, 240, 0),
                    x + 4,
                    y - 8,
                    char,
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

        # m = (
        #     ";" * math.floor(self.num / row_letter_num)
        #     + "  " * (self.num % row_letter_num)
        #     + moji[self.num]
        # )

        # Itext(
        #     self.screen,
        #     self.font,
        #     (255, 240, 0),
        #     40,
        #     100,
        #     m,
        # )

        pygame.display.update()  # 画面更新
