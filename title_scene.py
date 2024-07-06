import math
import sys
import pygame
from pygame.locals import *
import re

from Ifunctions import *


class TitleScene:
    def __init__(
        self, screen: pygame.Surface, pushed: list[int], mouse: dict, saves
    ) -> None:
        self.scene_name = "title"
        self.screen = screen
        self.mouse = mouse
        self.pushed = pushed
        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 64)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.command = Icommand(
            self.mouse,
            self.pushed,
            self.screen,
            self.font2,
            (255, 201, 214),
            20,
            180,
            RegexDict(
                {
                    "": [
                        "はじめから",
                        "とちゅうから",
                        "イラスト",
                        "せってい",
                        "やめる",
                    ],
                    "1": [
                        save["name"] + ": chapter " + str(save["chapter"])
                        for save in self.saves
                    ]
                    + ["やめる"],
                }
            ),
            outline_width=2,
            outline_colour=[(255, 255, 255)],
        )

        self.is_end = False

        pygame.mixer.init()  # 初期化

        pygame.mixer.music.stop()
        # pygame.mixer.music.load("sounds/試作19 2.mp3")
        # pygame.mixer.music.play(-1)

    def mainloop(self) -> None:
        self.screen.fill((255, 201, 224))

        Itext(
            self.screen,
            self.font,
            (255, 201, 214),
            20,
            20,
            "もこもこマイコン部!",
            outline_width=5,
            outline_colour=[(255, 255, 255)],
        )

        self.command.run()

        if self.command.branch == "0":
            pygame.mixer.music.fadeout(1000)
            self.is_end = True

        elif self.command.branch == "1":
            if len(self.command.options["1"]) == 0:
                self.command.cancel()

            Itext(
                self.screen,
                self.font2,
                (255, 201, 214),
                20,
                130,
                "セーブデータを選択",
                outline_width=2,
                outline_colour=[(255, 255, 255)],
            )
        elif self.command.branch == "3":
            pass

        elif self.command.branch == "4":
            pygame.quit()  # 全てのpygameモジュールの初期化を解除
            sys.exit()  # 終了（ないとエラーで終了することになる）

        elif re.match("^1.$", self.command.branch):
            if len(self.command.options["1"]) - 1 == int(self.command.branch[1]):
                self.command.cancel(2)
                return

            pygame.mixer.music.fadeout(1000)
            self.is_end = True
            return int(self.command.branch[1])

        pygame.display.update()  # 画面更新
