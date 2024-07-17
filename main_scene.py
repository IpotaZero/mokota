import json
import pygame
from pygame.locals import *

from Ifunctions import *
from story import Save, serifs


class MainScene:
    def __init__(self, screen: pygame.Surface, saves: list[Save]) -> None:
        self.scene_name = "main"

        # このまま出てきたらえらー
        self.name = "ERROR"

        self.screen = screen

        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.save_data_num = None

        self.start()

    def start(self):
        self.popups = []

        self.skip = False
        self.auto = False

        self.log = []
        self.log_slicer = 0

        self.mode = "text"

        self.frame = 0

        self.load_save_data(self.save_data_num)

        self.story_command = Icommand(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            540,
            RegexDict({}),
        )

        self.set_save_command()

        self.title_command = Icommand(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            540 + self.font.get_height(),
            RegexDict({"": ["タイトルに戻る", "再開する"], "0": ["はい", "いいえ"]}),
        )

        self.is_end = False

        self.images: dict = {}
        self.letter_colour = (255, 255, 255)

        pygame.mixer.init()  # 初期化

    def set_save_command(self):
        save_data_list = [
            save["name"] + ": chapter " + str(save["chapter"]) for save in self.saves
        ] + ["空のデータ"]

        self.save_command = Icommand(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            80,
            RegexDict(
                {
                    "": save_data_list,
                    ".": ["ロード", "セーブ", "やめる"],
                    ".[0-1]": ["はい", "いいえ"],
                    # ".2": ["ERROR"],
                }
            ),
        )

    def mainloop(self):
        self.screen.fill((0, 0, 0))  # 背景を黒
        for image in self.images.values():
            if image["on"] != None or image["on"] == True:
                self.screen.blit(image["size"], image["pos"])

        scr = pygame.Surface((1140, 250), flags=pygame.SRCALPHA)
        scr.fill((0, 0, 0, 255 / 2))
        self.screen.blit(scr, (30, 530))

        if self.mode == "text" or self.mode == "log":
            is_pushed_log = (
                Ibutton(
                    self.screen,
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

        if self.mode == "text" or self.mode == "save":
            is_pushed_save = (
                Ibutton(
                    self.screen,
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

        if self.mode == "text" or self.mode == "pause":
            is_pushed_escape = (
                Ibutton(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    1070,
                    30,
                    100,
                    40,
                    "TITLE",
                )
                or K_ESCAPE in keyboard["pushed"]
            )

        if self.mode == "text":
            if self.skip:
                is_pushed_skip = (
                    Ibutton(
                        self.screen,
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
                        self.screen,
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
                        self.screen,
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
                        self.screen,
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
                Itext(self.screen, self.font, (255, 255, 255), 30, 30, popup["text"])
                popup["life"] -= 1
                if popup["life"] == 0:
                    self.popups.remove(popup)

            self.mode_text()
            self.frame += 1

        elif self.mode == "log":
            if is_pushed_log:
                self.mode = "text"

            self.mode_log()

        elif self.mode == "save":
            if is_pushed_save:
                self.mode = "text"

            self.mode_save()

        elif self.mode == "pause":
            if is_pushed_escape:
                self.mode = "text"
            self.mode_pause()

        pygame.display.update()  # 画面更新

    def mode_text(self):
        # branchの長さが20を超えるストーリーは止めた方がいいんじゃないかな
        if len(self.branch) > 20:
            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                540,
                "branchが存在しません;もしくは単にbranchの長さが20を超えてる;chapterを分けた方がいいんじゃないかな",
                max_width=1100,
                frame=self.frame / 2,
            )
            return

        element = serifs[self.chapter][self.branch][self.text_num]

        if type(element) == str:
            self.solve_text(element)
        elif type(element) == list:
            self.solve_command(element)

    def solve_text(self, text: str):
        formated_text = text.format(name=self.name)

        if self.frame == 1:
            self.log.append(formated_text + ";")
            self.log_slicer = None

        clicked = Ibutton(
            self.screen,
            self.font,
            (255, 255, 255),
            (255, 255, 255),
            50,
            540,
            1100,
            190,
            "",
            line_width=0,
        )

        text_length = len(formated_text) * 2

        if (
            K_RETURN in keyboard["pushed"]
            or K_SPACE in keyboard["pushed"]
            or clicked
            or self.skip
            or (
                text_length + 30 <= self.frame
                and (
                    self.auto
                    or K_RETURN in keyboard["long_pressed"]
                    or K_SPACE in keyboard["long_pressed"]
                )
            )
        ):
            if text_length > self.frame:
                self.frame = text_length
            else:
                self.text_num += 1
                self.frame = 0

            # if self.text_num == len(element_list):
            #     self.text_num = 0

        if self.frame % 60 < 30:
            formated_text += "▼"

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            540,
            formated_text,
            max_width=1100,
            frame=self.frame / 2,
        )

    def solve_command(self, command):
        element = command[0]

        if element == "goto":
            self.text_num = 0
            self.frame = 0

            if type(command[1]) == str:
                self.branch = command[1]

            else:
                self.branch = command[1](
                    {
                        "footprints": self.footprints,
                        "max_credit": self.credits.index(max(self.credits)),
                    }
                )
            return

        elif element == "question":
            if self.frame == 1:
                self.story_command.options.regex_dict[""] = command[1]

            self.story_command.run()

            if self.story_command.is_match("."):
                self.log.append(self.story_command.get_selected_option() + ";")
                self.footprints[self.branch] = self.story_command[0]
                self.branch = command[2][self.story_command[0]]
                self.text_num = 0
                self.frame = 0
                self.story_command.reset()

        elif element == "go":
            self.branch += str(self.credits.index(max(self.credits)))
            self.text_num = 0
            self.frame = 0

        elif element == "credit":
            num = command[1]
            self.credits[num] += 5
            self.text_num += 2
            self.frame = 0

            self.popups.append({"text": "LEVEL UP!", "life": 120})

        elif element == "next_chapter":
            self.chapter += 1
            self.branch = ""
            self.text_num = 0
            self.frame = 0

        elif element == "sound":
            pygame.mixer.Sound("sounds/" + command[1]).play()
            self.text_num += 1
            self.frame = 0

        elif element == "bgm":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/" + command[1])
            pygame.mixer.music.play(-1)
            self.text_num += 2
            self.frame = 0

        elif element == "stop_bgm":
            pygame.mixer.music.fadeout(1000)
            self.text_num += 1
            self.frame = 0

        elif element == "sleep":
            if command[1] * 60 <= self.frame:
                self.text_num += 1
                # self.pushed.clear()
                self.frame = 0

        elif element == "darken":
            scr = pygame.Surface((1200, 800), flags=pygame.SRCALPHA)
            scr.fill((0, 0, 0, 255 * self.frame / 60))
            self.screen.blit(scr, (0, 0))

            if self.frame == 60:
                self.text_num += 1
                self.frame = 0

        elif element == "rdarken":
            scr = pygame.Surface((1200, 800), flags=pygame.SRCALPHA)
            scr.fill((0, 0, 0, 255 * (1 - self.frame / 60)))
            self.screen.blit(scr, (0, 0))

            if self.frame == 60:
                self.text_num += 1
                self.frame = 0

        elif element == "image_back":
            path = "images/background/" + command[1]
            img = pygame.image.load(path).convert()
            if len(command) >= 3:
                self.images["background"] = command[2]
            else:
                self.images["background"] = {
                    "size": pygame.transform.scale(img, (1200, 800)),
                    "pos": (0, 0),
                    "on": True,
                }
            self.text_num += 2

        elif element == "image_one":
            path = "images/" + command[1]
            img = pygame.image.load(path)
            self.images[command[1]] = command[2]
            self.text_num += 1

        elif element == "image_onoff":
            self.images[command[1]]["on"] = command[2]
        # elif element == "image":
        #     img = pygame.image.load(
        #         "images/" + element_list[self.text_num + 1]
        #     )
        #     scale = serifs[self.chapter][self.branch][self.text_num + 2]
        #     pos = serifs[self.chapter][self.branch][self.text_num + 3]

        #     self.images.append((pygame.transform.scale(img, scale), pos))
        #     self.text_num += 3

        elif element == "delete_image":
            r = command[1]
            del self.images[r]
            self.text_num += 1

        else:
            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                540,
                f"知らないコマンド: {element}",
                max_width=1100,
            )

    def mode_log(self):
        text = Iadjust(self.font, ";".join(self.log), 1100)

        row = text.split(";")

        max_row_num = 14

        if self.log_slicer is None:
            self.log_slicer = max([len(row) - max_row_num, 0])

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            65,
            ";".join(row[self.log_slicer :]),
            max_width=1100,
            max_height=650,
        )

        line = len(row)

        if line > max_row_num:
            scroll = Iscroll(50, 70, 1100, 660)

            if line - self.log_slicer > max_row_num:
                is_pushed_down = Ibutton(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    150,
                    738,
                    900,
                    32,
                    "▼",
                    line_width=2,
                )
                # Itext(self.screen, self.font, (255, 255, 255), 380, 500, "▼")

                if (
                    K_DOWN in keyboard["long_pressed"]
                    or is_pushed_down
                    or (scroll[0] and scroll[1] == "down")
                ):
                    self.log_slicer += 1
                    self.log_slicer %= line

            if self.log_slicer > 0:
                is_pushed_up = Ibutton(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    150,
                    30,
                    900,
                    32,
                    "▲",
                    line_width=2,
                )

                if (
                    K_UP in keyboard["long_pressed"]
                    or is_pushed_up
                    or (scroll[0] and scroll[1] == "up")
                ):
                    self.log_slicer += line - 1
                    self.log_slicer %= line

    def mode_save(self):
        self.save_command.run()

        if self.save_command.is_match(""):
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "セーブデータを選択")

            for i, save in enumerate(self.saves):
                current_text = '"' + save.current_text(18) + '"'

                Itext(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    520,
                    80 + self.font.get_height() * i,
                    current_text,
                )

        elif self.save_command.is_match("."):
            selected_save_data_num = self.save_command[0]

            current_text = ""

            if selected_save_data_num < len(self.saves):
                save = self.saves[selected_save_data_num]
                current_text = '"' + save.current_text(20) + '"'

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                40,
                self.save_command.get_selected_option() + current_text,
            )

        elif self.save_command.is_match(".[0-1]"):
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "ほんとに?")

        # print(self.save_command.branch, self.save_command.num)

        if self.save_command.is_match(".00"):
            # load->yes
            save_data_number = self.save_command[0]

            if len(self.saves) == save_data_number:
                self.save_command.cancel()
                return

            self.load_save_data(save_data_number)

            self.save_command.cancel(3)

            self.log = []
            self.mode = "text"

        elif self.save_command.is_match(".10"):
            # save->yes
            save_data_number = self.save_command[0]

            if len(self.saves) == save_data_number:
                self.saves.append(Save({}))

            # print(self.saves, save_data_number)

            self.saves[save_data_number]["name"] = self.name
            self.saves[save_data_number]["chapter"] = self.chapter
            self.saves[save_data_number]["branch"] = self.branch
            self.saves[save_data_number]["text_num"] = self.text_num
            self.saves[save_data_number]["credits"] = self.credits
            self.saves[save_data_number]["footprints"] = self.footprints

            with open("save.dat", "w") as f:
                f.write(json.dumps([save.save_data for save in self.saves]))

            self.save_command.cancel(3)

            self.set_save_command()

        elif self.save_command.is_match(".[0-1]1"):
            # yes/no
            self.save_command.cancel(2)

        elif self.save_command.is_match(".2"):
            # cancel
            # print(0)
            self.save_command.cancel(2)

    def load_save_data(self, save_data_number):
        self.chapter = 0
        self.text_num = 0
        self.branch = ""
        self.credits = [0, 0, 0]
        self.footprints = {}

        self.frame = 0
        self.images = []
        self.background_image = None
        pygame.mixer.music.fadeout(1000)

        if save_data_number is not None:
            self.name = self.saves[save_data_number]["name"]
            self.chapter = self.saves[save_data_number]["chapter"]
            self.branch = self.saves[save_data_number]["branch"]
            self.text_num = self.saves[save_data_number]["text_num"]
            self.credits = self.saves[save_data_number]["credits"]
            self.footprints = self.saves[save_data_number]["footprints"]

    def mode_pause(self):

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            30,
            ";".join(
                [
                    ["もこ音", "もこ子", "もこ美"][i] + ": " + str(self.credits[i])
                    for i in range(3)
                ]
            ),
        )

        self.title_command.run()

        if self.title_command.is_match("0"):
            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                540,
                "ほんとに?",
            )
        elif self.title_command.is_match("00"):
            self.is_end = True

        elif self.title_command.is_match("01"):
            self.title_command.cancel(2)

        elif self.title_command.is_match("1"):
            self.mode = "text"
