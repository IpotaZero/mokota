import copy
import pygame
from pygame.locals import *

from Ifunctions import *
from story import serifs
from save import Save
from mode_text import ModeText
from mode_save import ModeSave
from mode_log import ModeLog
from mode_pause import ModePause


class SceneMain(ModeText, ModeSave, ModeLog, ModePause):
    def __init__(self, saves: list[Save], config: dict) -> None:
        self.scene_name = "main"

        # このまま出てきたらえらー
        self.name = "ERROR"

        self.screen = self.screen = pygame.display.get_surface()
        self.buffer_screen = pygame.Surface(screen_option["default_size"])
        self.layer_background = pygame.Surface(screen_option["default_size"])
        self.layer_buttons = pygame.Surface(
            screen_option["default_size"], pygame.SRCALPHA
        )

        self.saves = saves
        self.config = config

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.save_data_num = None

        self.is_end = False

        self.start()

    def start(self):
        self.popups = []

        self.skip = False
        self.auto = False

        self.log = []
        self.log_slicer = 0

        self.mode = "text"

        self.frame = 0

        self.story_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            540,
            RegexDict({}),
            title=RegexDict({"": "選択肢"}),
        )

        self.set_save_command()

        self.title_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            200,
            RegexDict(
                {
                    "": ["タイトルに戻る", "設定", "再開する"],
                    "0": ["はい", "いいえ"],
                    "1": [
                        "画面サイズ",
                        ["BGM:", self.config["volume_bgm"], 0, 9],
                        ["SE :", self.config["volume_se"], 0, 9],
                        ["TEXT_SPEED:", self.config["text_speed"], 1, 5],
                        "やめる",
                    ],
                    "10": [
                        "フルスクリーン",
                        "600x400",
                        "800x533",
                        "900x600",
                        "1200x800",
                        "1500x1000",
                        "1800x1200",
                        "2400x1600",
                        "やめる",
                    ],
                }
            ),
            title=RegexDict({"0": "ほんとに?"}),
        )

        self.images: dict = {}
        self.letter_colour = (255, 255, 255)

        pygame.mixer.init()  # 初期化

        self.load_save_data(self.save_data_num)

    def set_save_command(self):
        save_data_list = [
            save["name"] + ": chapter " + str(save["chapter"]) for save in self.saves
        ] + ["空のデータ"]

        self.save_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            80 - self.font.get_height(),
            RegexDict(
                {
                    "": save_data_list,
                    ".": ["ロード", "セーブ", "削除", "やめる"],
                    ".[0-2]": ["はい", "いいえ"],
                    # ".2": ["ERROR"],
                }
            ),
            title=RegexDict({"": "セーブデータを選択", ".[0-2]": "ほんとに?"}),
        )

    def mainloop(self):
        self.layer_background.fill((0, 0, 0))  # 背景を黒
        for image in self.images.values():
            if image["is_shown"]:
                self.layer_background.blit(
                    pygame.transform.scale(image["img"], image["size"]), image["pos"]
                )

        self.layer_buttons.fill((0, 0, 0, 0))  # 透明

        # print(self.frame, self.text_num, self.branch)

        if self.mode in ["text", "log"]:
            is_pushed_log = (
                Ibutton(
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    30,
                    740,
                    100,
                    40,
                    "LOG",
                )
                or K_l in keyboard["pushed"]
            )

        if self.mode in ["text", "save"]:
            is_pushed_save = (
                Ibutton(
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    1070,
                    740,
                    100,
                    40,
                    "SAVE",
                )
                or K_s in keyboard["pushed"]
            )

        if self.mode in ["text", "pause"]:
            is_pushed_escape = (
                Ibutton(
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    1070,
                    30,
                    100,
                    40,
                    "PAUSE",
                    outline_colour=[(0, 0, 0)],
                    outline_width=2,
                )
                or K_ESCAPE in keyboard["pushed"]
            )

        if self.mode == "text":
            if self.skip:
                is_pushed_skip = (
                    Ibutton(
                        self.layer_buttons,
                        self.font,
                        (255, 255, 255),
                        (255, 255, 255),
                        160,
                        740,
                        100,
                        40,
                        "SKIP",
                        line_width=100,
                        outline_colour=[(0, 0, 0)],
                        outline_width=2,
                    )
                    or K_k in keyboard["pushed"]
                )
            else:
                is_pushed_skip = (
                    Ibutton(
                        self.layer_buttons,
                        self.font,
                        (255, 255, 255),
                        (255, 255, 255),
                        160,
                        740,
                        100,
                        40,
                        "SKIP",
                    )
                    or K_k in keyboard["pushed"]
                )

            if self.auto:
                is_pushed_auto = (
                    Ibutton(
                        self.layer_buttons,
                        self.font,
                        (255, 255, 255),
                        (255, 255, 255),
                        290,
                        740,
                        100,
                        40,
                        "AUTO",
                        line_width=100,
                        outline_colour=[(0, 0, 0)],
                        outline_width=2,
                    )
                    or K_a in keyboard["pushed"]
                )
            else:
                is_pushed_auto = (
                    Ibutton(
                        self.layer_buttons,
                        self.font,
                        (255, 255, 255),
                        (255, 255, 255),
                        290,
                        740,
                        100,
                        40,
                        "AUTO",
                    )
                    or K_a in keyboard["pushed"]
                )

            if is_pushed_skip:
                self.skip = not self.skip

            elif is_pushed_auto:
                self.auto = not self.auto

            elif is_pushed_escape:
                self.mode = "pause"
                self.title_command.reset()

            elif is_pushed_log:
                self.mode = "log"

            elif is_pushed_save:
                self.mode = "save"
                self.save_command.reset()

            for popup in self.popups:
                Itext(
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    30,
                    30,
                    popup["text"],
                )
                popup["life"] -= 1
                if popup["life"] == 0:
                    self.popups.remove(popup)

            Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 530, 1140, 250)

            self.frame += 1
            self.mode_text()

        elif self.mode == "log":
            if is_pushed_log:
                self.mode = "text"

            Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 30, 1140, 750)

            self.mode_log()

        elif self.mode == "save":
            if is_pushed_save:
                self.mode = "text"

            Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 30, 1140, 750)

            self.mode_save()

        elif self.mode == "pause":
            if is_pushed_escape:
                self.mode = "text"

            Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 30, 1140, 750)

            self.mode_pause()

        if self.frame == 0:
            return

        self.buffer_screen.blit(self.layer_background, (0, 0))
        self.buffer_screen.blit(self.layer_buttons, (0, 0))

        scr = pygame.transform.smoothscale(
            self.buffer_screen,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )
        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()  # 画面更新

    def load_save_data(self, save_data_number):
        Itext(
            self.buffer_screen,
            self.font,
            (255, 255, 255),
            950,
            700,
            "NOW LOADING...",
        )

        scr = pygame.transform.scale(
            self.buffer_screen,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )

        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()

        self.chapter = 0
        self.text_num = 0
        self.branch = "first"
        self.credits = [0, 0, 0]
        self.footprints = {}

        self.log = []
        self.frame = 0
        self.images = {}

        pygame.mixer.music.fadeout(1000)

        if save_data_number is not None:
            save: Save = self.saves[save_data_number]
            self.name = save["name"]
            self.chapter = save["chapter"]
            self.branch = save["branch"]
            self.text_num = save["text_num"]
            self.credits = copy.deepcopy(save["credits"])
            self.footprints = copy.deepcopy(save["footprints"])

            # print(save["credits"])

            chapter = save["chapter"]
            branch = "first"
            text_num = 0

            while branch != save["branch"] or text_num != save["text_num"]:
                self.frame = 1

                element = serifs[chapter][branch][text_num]
                text_num += 1

                if type(element) == str:
                    self.solve_text(element)
                    continue

                if element[0] == "goto":
                    branch = self.get_next_branch(element)
                    text_num = 0

                elif element[0] == "question":
                    # print(self.footprints)
                    branch = element[2][save["footprints"][branch]]
                    text_num = 0

                elif element[0] not in ["sound", "credit"]:
                    self.solve_1frame_command(element)

            # self.frame = 0

            # print(save["credits"])

            self.name = save["name"]
            self.chapter = save["chapter"]
            self.branch = save["branch"]
            self.text_num = save["text_num"]
            self.credits = copy.deepcopy(save["credits"])
            self.footprints = copy.deepcopy(save["footprints"])

            self.frame = 0

            # print(self.frame)
