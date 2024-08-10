import json
import sys
import pygame
from pygame.locals import *

from Ifunctions import *
from save import Save


class SceneTitle:
    def __init__(self, saves: list[Save], config: dict[str]) -> None:
        self.scene_name = "title"
        self.screen = pygame.display.get_surface()
        self.buffer_screen = pygame.Surface(screen_option["default_size"])
        self.saves = saves
        self.config = config

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 64)
        self.font2 = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.command = Icommand(
            self.buffer_screen,
            self.font2,
            (255, 255, 255),
            20,
            150,
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
                    "3": [
                        "やめる",
                        "画面サイズ",
                        "音量",
                        ["テキストの速さ:", self.config["text_speed"], 1, 5],
                        "編集(デバッグ)",
                    ],
                    "31": [
                        "やめる",
                        "フルスクリーン",
                        "600x400",
                        "800x533",
                        "900x600",
                        "1200x800",
                        "1500x1000",
                        "1800x1200",
                        "2400x1600",
                    ],
                    "32": [
                        "やめる",
                        ["BGM:", self.config["volume_bgm"], 0, 9],
                        ["SE :", self.config["volume_se"], 0, 9],
                        # ["オーディオ:", 0, ["ステレオ", "モノラル"]],
                    ],
                    "4": ["はい", "いいえ"],
                },
            ),
            title=RegexDict(
                {
                    "1": "セーブデータを選択",
                    "1.": "どうする?",
                    "1.1": "ほんとに?",
                    "2": "どのイラストを見る?",
                    "3": "設定",
                    "31": "画面サイズの変更",
                    "32": "音量設定",
                    "4": "ほんとに?",
                }
            ),
            # outline_width=2,
            # outline_colour=[(255, 255, 255)],
        )

        self.is_end = False

        pygame.mixer.init()  # 初期化

        pygame.mixer.music.stop()
        pygame.mixer.music.load("sounds/bgm/試作19 2.mp3")
        pygame.mixer.music.set_volume(self.config["volume_bgm"] / 9)
        pygame.mixer.music.play()

        self.is_first_looped = False

    def mainloop(self):
        self.check_music_end(2.292, 77.847)
        # self.check_music_end(2.292, 12)

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
            for i, save in enumerate(self.saves):
                Itext(
                    self.buffer_screen,
                    self.font2,
                    (255, 255, 255),
                    500,
                    150 + self.font2.get_height() * (i + 1),
                    '"' + save.current_text(18) + '"',
                    # outline_width=2,
                    # outline_colour=[(255, 255, 255)],
                )

        elif self.command.is_match("1."):
            # load->cancel
            if self.command[1] == len(self.saves):
                self.command.cancel(2)
                return

        elif self.command.is_match("1.0"):
            # load->load
            pygame.mixer.music.fadeout(1000)
            self.is_end = True
            return self.command[1]

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

        elif self.command.is_match("2."):
            if self.command[1] == 0:
                self.command.cancel(2)
                return

            elif self.command.get_selected_option() == "???":
                self.command.cancel()
                return
        elif self.command.is_match("3"):
            s = self.command.get_range_value()[0]

            if s != self.config["text_speed"]:
                self.config["text_speed"] = s
                with open("config.dat", "w") as f:
                    f.write(json.dumps(self.config))

        elif self.command.is_match("30"):
            self.command.cancel(2)

        elif self.command.is_match("31."):
            if self.command[2] == 0:
                self.command.cancel(2)
                return

            size = [
                (0, 0),
                (600, 400),
                (800, 533),
                (900, 600),
                (1200, 800),
                (1500, 1000),
                (1800, 1200),
                (2400, 1600),
            ][self.command[2] - 1]

            set_window_size(size)

            self.config["window_size"] = size

            with open("config.dat", "w") as f:
                f.write(json.dumps(self.config))

            self.command.cancel(1)

        elif self.command.is_match("32"):
            g, h = self.command.get_range_value()

            if (g, h) != (self.config["volume_bgm"], self.config["volume_se"]):
                self.config["volume_bgm"], self.config["volume_se"] = g, h
                pygame.mixer.music.set_volume(g / 9)
                with open("config.dat", "w") as f:
                    f.write(json.dumps(self.config))

        elif self.command.is_match("320"):
            self.command.cancel(2)

        elif self.command.is_match("34"):
            self.is_end = True
            return "edit"

        elif self.command.is_match("40"):
            pygame.quit()  # 全てのpygameモジュールの初期化を解除
            sys.exit()  # 終了（ないとエラーで終了することになる）

        elif self.command.is_match("41"):
            self.command.cancel(2)

        scr = pygame.transform.smoothscale(
            self.buffer_screen,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )
        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()  # 画面更新

    def check_music_end(self, loop_start, loop_end):
        if pygame.mixer.music.get_busy():

            # 現在の再生時間を取得
            current_time = pygame.mixer.music.get_pos() / 1000
            if self.is_first_looped:
                current_time += loop_start

            print(current_time)
            if current_time >= loop_end:
                self.is_first_looped = True
                # 音楽を停止してループ開始位置から再生
                pygame.mixer.music.stop()
                pygame.mixer.music.play(start=loop_start)
