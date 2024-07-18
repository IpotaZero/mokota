import json
import sys
import pygame
from pygame.locals import *

import Ifunctions
from Ifunctions import *
from story import Save


class TitleScene:
    def __init__(self, screen: pygame.Surface, saves: list[Save]) -> None:
        self.scene_name = "title"
        self.screen = screen
        self.buffer_screen = pygame.Surface((1200, 800))
        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 64)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.command = Icommand(
            self.buffer_screen,
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
                    "3": ["やめる", "画面サイズ", "編集(デバッグ)"],
                    "31": [
                        "600x400",
                        "800x533",
                        "900x600",
                        "1200x800",
                        "1500x1000",
                        "1800x1200",
                        "2400x1600",
                        "やめる",
                    ],
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
        self.buffer_screen.fill((255, 201, 224))

        Itext(
            self.buffer_screen,
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
                self.buffer_screen,
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
                    self.buffer_screen,
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
                self.buffer_screen,
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
                self.buffer_screen,
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
                self.buffer_screen,
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
                self.buffer_screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "設定",
                # outline_width=2,
                # outline_colour=[(255, 255, 255)],
            )

        elif self.command.is_match("30"):
            self.command.cancel(2)

        elif self.command.is_match("31"):
            Itext(
                self.buffer_screen,
                self.font2,
                (255, 255, 255),
                20,
                130,
                "画面サイズの変更",
            )

        elif self.command.is_match("31."):
            if self.command[2] == 7:
                self.command.cancel(2)
                return

            size = [
                (600, 400, 0.5),
                (800, 533, 0.67),
                (900, 600, 0.75),
                (1200, 800, 1),
                (1500, 1000, 1.25),
                (1800, 1200, 1.5),
                (2400, 1600, 2),
            ][self.command[2]]

            pygame.display.set_mode(size[:2])

            screen_option["ratio"] = size[2]

            self.command.cancel(2)

        elif self.command.is_match("32"):
            self.is_end = True
            return "edit"

        elif self.command.is_match("4"):
            Itext(
                self.buffer_screen,
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

        scr = pygame.transform.scale(
            self.buffer_screen,
            (1200 * screen_option["ratio"], 800 * screen_option["ratio"]),
        )
        self.screen.blit(scr, (0, 0))
        pygame.display.update()  # 画面更新
