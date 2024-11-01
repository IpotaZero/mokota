import math
import pygame
from pygame.locals import *

from Ifunctions import *

moji = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろやゆよわをがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょっんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモラリルレロヤユヨワヲガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポァィゥェォャュョッンー消終"


class SceneName:
    def __init__(self, config) -> None:
        self.scene_name = "name"

        self.config = config

        self.screen = self.screen = pygame.display.get_surface()
        self.buffer_screnn = pygame.Surface(screen_option["default_size"])

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 48)
        self.moved_se = pygame.mixer.Sound("sounds/se/select.wav")
        self.finishd_se = pygame.mixer.Sound("sounds/se/ok.wav")
        self.start()

    def start(self):
        self.is_end = False

        self.num = 0
        self.name = "もこた"

        pygame.mixer.music.stop()
        pygame.mixer.music.load("sounds/bgm/試作25.mp3")
        pygame.mixer.music.set_volume(self.config["volume_bgm"] / 9)
        pygame.mixer.music.play(-1)

    def add_num(self, num):
        self.moved_se.play()
        self.num += num
        self.num %= len(moji)

    def mainloop(self):
        row_letter_num = 20
        self.buffer_screnn.fill((255, 201, 224))

        if K_RIGHT in keyboard["long_pressed"]:
            self.add_num(1)
        elif K_LEFT in keyboard["long_pressed"]:
            self.add_num(len(moji) - 1)
        elif K_DOWN in keyboard["long_pressed"]:
            self.add_num(row_letter_num)
        elif K_UP in keyboard["long_pressed"]:
            self.add_num(len(moji) - row_letter_num)
        elif K_TAB in keyboard["pushed"]:
            if len(self.name) > 0:
                self.finishd_se.play()
                self.is_end = True
                return self.name
        elif len({K_RETURN, K_SPACE, K_z} & keyboard["pushed"]) > 0:
            if self.num == len(moji) - 1:
                if len(self.name) > 0:
                    self.finishd_se.play()
                    self.is_end = True
                    return self.name
            elif self.num == len(moji) - 2:
                if len(self.name) > 0:
                    self.name = self.name[:-1]

            elif len(self.name) < 7:
                self.name += moji[self.num]

        elif len({K_BACKSPACE, K_ESCAPE, K_x} & keyboard["pushed"]) > 0:
            if len(self.name) > 0:
                self.name = self.name[:-1]

        Itext(
            self.buffer_screnn,
            self.font,
            (255, 255, 255),
            40,
            30,
            "名前を入力:",
        )

        Itext(
            self.buffer_screnn,
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
                self.buffer_screnn,
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
                    self.buffer_screnn,
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

        scr = pygame.transform.smoothscale(
            self.buffer_screnn,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )
        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()  # 画面更新
