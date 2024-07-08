import json
import sys
import pygame
from pygame.locals import *
import re

from Ifunctions import *
from story import serifs


class TitleScene:
    def __init__(
        self, screen: pygame.Surface, pushed: list[int], mouse: dict, saves: list
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
            (255, 255, 255),
            20,
            180,
            RegexDict(
                {
                    "": [
                        "はじめから",
                        "とちゅうから",
                        "イラスト",
                        "せってい",
                        "おわる",
                    ],
                    "1": [
                        save["name"] + ": chapter " + str(save["chapter"])
                        for save in self.saves
                    ]
                    + ["やめる"],
                    "1.": ["ロード", "削除", "やめる"],
                    "1.1": ["はい", "いいえ"],
                    "2": ["やめる", "???", "???", "???"],
                    "3": ["やめる"],
                    "4": ["はい", "いいえ"],
                }
            ),
            # outline_width=2,
            # outline_colour=[(255, 255, 255)],
        )

        self.is_end = False

        pygame.mixer.init()  # 初期化

        pygame.mixer.music.stop()
        # pygame.mixer.music.load("sounds/試作19 2.mp3")
        # pygame.mixer.music.play(-1)

    def mainloop(self):
        self.screen.fill((255, 201, 224))

        Itext(
            self.screen,
            self.font,
            (255, 201, 214),
            350,
            50,
            "初恋コードライン",
            outline_width=5,
            outline_colour=[(255, 255, 255)],
        )

        self.command.run()

        if self.command.branch == "0":
            pygame.mixer.music.fadeout(1000)
            self.is_end = True

        elif self.command.branch == "1":
            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "セーブデータを選択",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

            for i, save in enumerate(self.saves):
                current_text = serifs[save["chapter"]][save["branch"]][save["text_num"]]
                if type(current_text) != str:
                    current_text = "ERROR"
                # print(type(current_text))

                max_letter_num = 18

                if len(current_text) > max_letter_num:
                    current_text = (
                        current_text[:max_letter_num].replace(";", "") + "..."
                    )

                Itext(
                    self.screen,
                    self.font2,
                    (255, 255, 255),
                    500,
                    180 + self.font2.get_height() * i,
                    '"' + current_text + '"',
                    # outline_width=2,
                    # outline_colour=[(255, 255, 255)],
                )

        elif re.match("^1.$", self.command.branch):
            # load->cancel
            if self.command.get_selected_num() == len(self.saves):
                self.command.cancel(2)
                return

            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "どうする?",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

        elif re.match("^1.0$", self.command.branch):
            # load->load
            pygame.mixer.music.fadeout(1000)
            self.is_end = True
            return self.command.get_selected_num(2)

        elif re.match("^1.1$", self.command.branch):
            # load->delete
            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "ほんとに?",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

        elif re.match("^1.10$", self.command.branch):
            # load->delete->yes
            self.saves.pop(self.command.get_selected_num(3))

            with open("save.dat", "w") as f:
                f.write(json.dumps(self.saves))

            self.command.cancel(3)

            self.command.options.regex_dict["1"] = [
                save["name"] + ": chapter " + str(save["chapter"])
                for save in self.saves
            ] + ["やめる"]

        elif re.match("^1.11$", self.command.branch):
            # load->delete->no
            self.command.cancel(2)

        elif re.match("^1.2$", self.command.branch):
            # load->cancel
            self.command.cancel(2)

        elif self.command.branch == "2":
            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "どのイラストを見る?",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

        elif re.match("^2.$", self.command.branch):
            if self.command.get_selected_num() == 0:
                self.command.cancel(2)

            elif self.command.get_selected_option() == "???":
                self.command.cancel()
                return

        elif self.command.branch == "3":
            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "設定",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

        elif re.match("^3.$", self.command.branch):
            if self.command.get_selected_num() == 0:
                self.command.cancel(2)

        elif self.command.branch == "4":
            Itext(
                self.screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "ほんとに?",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )
        elif self.command.branch == "40":
            pygame.quit()  # 全てのpygameモジュールの初期化を解除
            sys.exit()  # 終了（ないとエラーで終了することになる）

        elif self.command.branch == "41":
            self.command.cancel(2)

        pygame.display.update()  # 画面更新
