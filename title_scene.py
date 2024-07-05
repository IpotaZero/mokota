import sys
import pygame
from pygame.locals import *
import re

from Ifunctions import *


class TitleScene:
    def __init__(self, screen: pygame.Surface, pushed: list[int], saves) -> None:
        self.scene_name = "title"
        self.screen = screen
        self.pushed = pushed
        self.saves = saves

        font = pygame.font.Font("DotGothic16-Regular.ttf", 74)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        # フォントの設定
        self.title_text = font.render("もこもこマイコン部", False, (255, 255, 255))

        self.command = Icommand(
            pushed,
            screen,
            self.font2,
            (255, 255, 255),
            20,
            180,
            RegexDict(
                {
                    "": ["はじめから", "つづきから", "やめる"],
                    "1": [save["name"] for save in saves] + ["CANCEL"],
                }
            ),
        )

        self.is_end = False

    def mainloop(self) -> None:
        self.screen.fill((0, 0, 0))  # 背景を黒

        self.screen.blit(self.title_text, (20, 20))

        self.command.run()

        if self.command.branch == "0":
            self.is_end = True

        elif self.command.branch == "1":
            if len(self.command.options["1"]) == 0:
                self.command.cancel()

            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "Choose Save Data",
            )

        elif self.command.branch == "2":
            pygame.quit()  # 全てのpygameモジュールの初期化を解除
            sys.exit()  # 終了（ないとエラーで終了することになる）

        elif re.match("^1.$", self.command.branch):
            if len(self.command.options["1"]) - 1 == int(self.command.branch[1]):
                self.command.cancel(2)
                return

            self.is_end = True
            return int(self.command.branch[1])

        pygame.display.update()  # 画面更新
