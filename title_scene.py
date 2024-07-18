import json
from re import S
import sys
import pygame
from pygame.locals import *

from Ifunctions import *
from scene import Scene
from story import Save


class TitleScene(Scene):
    def __init__(self, screen: pygame.Surface, saves: list[Save]) -> None:
        self.scene_name = "title"
        self.screen = screen
        super().__init__(screen)
        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 64)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.command = Icommand(
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
                    "3": ["やめる", "編集(デバッグ)"],
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

        if self.command.is_match("0"):
            pygame.mixer.music.fadeout(1000)
            self.is_end = True

        elif self.command.is_match("1"):
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
                Itext(
                    self.screen,
                    self.font2,
                    (255, 255, 255),
                    500,
                    180 + self.font2.get_height() * i,
                    '"' + save.current_text(18) + '"',
                    # outline_width=2,
                    # outline_colour=[(255, 255, 255)],
                )

        elif self.command.is_match("1."):
            # load->cancel
            if self.command[1] == len(self.saves):
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

        elif self.command.is_match("1.0"):
            # load->load
            pygame.mixer.music.fadeout(1000)
            self.is_end = True
            return self.command[1]

        elif self.command.is_match("1.1"):
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

        elif self.command.is_match("1.10"):
            # load->delete->yes
            self.saves.pop(self.command[1])

            with open("save.dat", "w") as f:
                f.write(json.dumps([save.save_data for save in self.saves]))

            self.command.cancel(3)

            self.command.options.regex_dict["1"] = [
                save["name"] + ": chapter " + str(save["chapter"])
                for save in self.saves
            ] + ["やめる"]

        elif self.command.is_match("1.11"):
            # load->delete->no
            self.command.cancel(2)

        elif self.command.is_match("1.2"):
            # load->cancel
            self.command.cancel(2)

        elif self.command.is_match("2"):
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

        elif self.command.is_match("2."):
            if self.command[1] == 0:
                self.command.cancel(2)
                return

            elif self.command.get_selected_option() == "???":
                self.command.cancel()
                return

        elif self.command.is_match("3"):
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

        elif self.command.is_match("3."):
            if self.command[1] == 0:
                self.command.cancel(2)
            elif self.command[1] == 1:
                self.is_end = True
                return "edit"

        elif self.command.is_match("4"):
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
        elif self.command.is_match("40"):
            pygame.quit()  # 全てのpygameモジュールの初期化を解除
            sys.exit()  # 終了（ないとエラーで終了することになる）

        elif self.command.is_match("41"):
            self.command.cancel(2)
