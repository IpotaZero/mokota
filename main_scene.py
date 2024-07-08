import json
import pygame
from pygame.locals import *

from Ifunctions import *
from story import serifs


class MainScene:
    def __init__(
        self, screen: pygame.Surface, pushed: list[int], mouse: dict, saves: list[dict]
    ) -> None:
        self.scene_name = "main"

        self.name = "ERROR"

        self.screen = screen
        self.pushed = pushed
        self.mouse = mouse

        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.save_data_num = None

        self.start()

    def start(self):
        self.skip = False
        self.auto = False

        self.log = []
        self.log_slicer = 0

        self.mode = "text"

        self.frame = 0

        self.load_save_data(self.save_data_num)

        self.story_command = Icommand(
            self.mouse,
            self.pushed,
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            540,
            RegexDict({}),
        )

        self.set_save_command()

        self.title_command = Icommand(
            self.mouse,
            self.pushed,
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            540 + self.font.get_height(),
            RegexDict({"": ["タイトルに戻る", "再開する"], "0": ["はい", "いいえ"]}),
        )

        self.is_end = False

        self.images: list[tuple] = []
        self.letter_colour = (255, 255, 255)

        pygame.mixer.init()  # 初期化

    def set_save_command(self):
        save_data_list = [
            save["name"] + ": chapter " + str(save["chapter"]) for save in self.saves
        ] + ["空のデータ"]

        self.save_command = Icommand(
            self.mouse,
            self.pushed,
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
                    ".2": ["ERROR"],
                }
            ),
        )

    def mainloop(self):
        self.screen.fill((0, 0, 0))  # 背景を黒
        for image, pos in self.images:
            self.screen.blit(image, pos)

        if self.mode == "text" or self.mode == "log":
            is_pushed_log = (
                Ibutton(
                    self.mouse,
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
                or K_l in self.pushed
            )

        if self.mode == "text" or self.mode == "save":
            is_pushed_save = (
                Ibutton(
                    self.mouse,
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
                or K_s in self.pushed
            )

        if self.mode == "text" or self.mode == "pause":
            is_pushed_escape = (
                Ibutton(
                    self.mouse,
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
                or K_ESCAPE in self.pushed
            )

        if self.mode == "text":
            if self.skip:
                is_pushed_skip = (
                    Ibutton(
                        self.mouse,
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
                    or K_k in self.pushed
                )
            else:
                is_pushed_skip = (
                    Ibutton(
                        self.mouse,
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
                    or K_k in self.pushed
                )

            if self.auto:
                is_pushed_auto = (
                    Ibutton(
                        self.mouse,
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
                    or K_a in self.pushed
                )
            else:
                is_pushed_auto = (
                    Ibutton(
                        self.mouse,
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
                    or K_a in self.pushed
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

            self.title_command.run()

            if self.title_command.branch == "0":
                Itext(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    50,
                    540,
                    "ほんとに?",
                )
            elif self.title_command.branch == "00":
                self.is_end = True

            elif self.title_command.branch == "01":
                self.title_command.cancel(2)

            elif self.title_command.branch == "1":
                self.mode = "text"

        pygame.display.update()  # 画面更新

    def mode_text(self):
        element = serifs[self.chapter][self.branch][self.text_num]

        if element == "question":
            if self.frame == 1:
                self.story_command.options.regex_dict[""] = serifs[self.chapter][
                    self.branch
                ][self.text_num + 1]

            self.story_command.run()

            if re.match("^.$", self.story_command.branch):
                self.log.append(self.story_command.get_selected_option() + ";")
                self.branch += self.story_command.branch
                self.text_num = 0
                self.frame = 0

        elif element == "credit":
            num = serifs[self.chapter][self.branch][self.text_num + 1]
            self.credits[num] += 1
            self.text_num += 2
            self.frame = 0

        elif element == "next_chapter":
            self.chapter += 1
            self.branch = ""
            self.text_num = 0
            self.frame = 0

        elif element == "go":
            self.branch += str(self.credits.index(max(self.credits)))
            self.text_num = 0
            self.frame = 0

        elif element == "sound":
            pygame.mixer.Sound(
                "sounds/" + serifs[self.chapter][self.branch][self.text_num + 1]
            ).play()
            self.text_num += 2
            self.frame = 0

        elif element == "bgm":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(
                "sounds/" + serifs[self.chapter][self.branch][self.text_num + 1]
            )
            pygame.mixer.music.play(-1)
            self.text_num += 2
            self.frame = 0

        elif element == "stop_bgm":
            pygame.mixer.music.fadeout(1000)
            self.text_num += 1
            self.frame = 0

        elif element == "sleep":
            if serifs[self.chapter][self.branch][self.text_num + 1] * 60 <= self.frame:
                self.text_num += 2
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

        elif element == "image":
            img = pygame.image.load(
                "images/" + serifs[self.chapter][self.branch][self.text_num + 1]
            )
            scale = serifs[self.chapter][self.branch][self.text_num + 2]
            pos = serifs[self.chapter][self.branch][self.text_num + 3]

            self.images.append((pygame.transform.scale(img, scale), pos))
            self.text_num += 3

        elif element == "delete_image":
            r = serifs[self.chapter][self.branch][self.text_num + 1]
            del self.images[r]
            self.text_num += 2

        else:
            text = serifs[self.chapter][self.branch][self.text_num]

            if type(text) != str:
                text = "ERROR"

            text = text.format(name=self.name)

            if self.frame == 1:
                self.log.append(text + ";")
                self.log_slicer = None

            clicked = Ibutton(
                self.mouse,
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

            text_length = len(text) * 2

            if (
                K_RETURN in self.pushed
                or K_SPACE in self.pushed
                or clicked
                or self.skip
                or (self.auto and text_length + 30 <= self.frame)
            ):
                if text_length > self.frame:
                    self.frame = text_length
                else:
                    self.text_num += 1
                    self.frame = 0

                if self.text_num == len(serifs[self.chapter][self.branch]):
                    self.text_num = 0
                    self.branch += "#"

            if self.frame % 60 < 30:
                text += "▼"

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                540,
                text,
                max_width=1100,
                frame=self.frame / 2,
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
            scroll = Iscroll(self.mouse, 50, 70, 1100, 660)

            if line - self.log_slicer > max_row_num:
                is_pushed_down = Ibutton(
                    self.mouse,
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
                    K_DOWN in self.pushed
                    or is_pushed_down
                    or (scroll[0] and scroll[1] == "down")
                ):
                    self.log_slicer += 1
                    self.log_slicer %= line

            if self.log_slicer > 0:
                is_pushed_up = Ibutton(
                    self.mouse,
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
                    K_UP in self.pushed
                    or is_pushed_up
                    or (scroll[0] and scroll[1] == "up")
                ):
                    self.log_slicer += line - 1
                    self.log_slicer %= line

    def mode_save(self):
        self.save_command.run()

        if self.save_command.branch == "":
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "セーブデータを選択")

            for i, save in enumerate(self.saves):
                current_text = serifs[save["chapter"]][save["branch"]][save["text_num"]]
                if type(current_text) != str:
                    current_text = "ERROR"

                max_letter_num = 18

                if len(current_text) > max_letter_num:
                    current_text = (
                        current_text[:max_letter_num].replace(";", "") + "..."
                    )

                Itext(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    520,
                    80 + self.font.get_height() * i,
                    '"' + current_text + '"',
                )

        elif re.match("^.$", self.save_command.branch):
            save = self.saves[self.save_command.get_selected_num()]
            current_text = serifs[save["chapter"]][save["branch"]][save["text_num"]]
            if type(current_text) != str:
                current_text = "ERROR"

            max_letter_num = 20

            if len(current_text) > max_letter_num:
                current_text = current_text[:max_letter_num].replace(";", "") + "..."

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                40,
                self.save_command.get_selected_option() + ' "' + current_text + '"',
            )

        elif re.match("^.[0-1]$", self.save_command.branch):
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "ほんとに?")

        # print(self.save_command.branch, self.save_command.num)

        if re.match("^.00$", self.save_command.branch):
            # load->yes
            save_data_number = self.save_command.get_selected_num(3)

            if len(self.saves) == save_data_number:
                self.save_command.cancel()
                return

            self.load_save_data(save_data_number)

            self.save_command.cancel(3)

            self.log = []
            self.mode = "text"

        elif re.match("^.10$", self.save_command.branch):
            # save->yes
            save_data_number = self.save_command.get_selected_num(3)

            if len(self.saves) == save_data_number:
                self.saves.append({})

            # print(self.saves, save_data_number)

            self.saves[save_data_number]["name"] = self.name
            self.saves[save_data_number]["chapter"] = self.chapter
            self.saves[save_data_number]["branch"] = self.branch
            self.saves[save_data_number]["text_num"] = self.text_num
            self.saves[save_data_number]["credits"] = self.credits

            with open("save.dat", "w") as f:
                f.write(json.dumps(self.saves))

            self.save_command.cancel(3)

            self.set_save_command()

        elif re.match("^.[0-1]1$", self.save_command.branch):
            # yes/no
            self.save_command.cancel(2)

        elif re.match("^.2$", self.save_command.branch):
            # cancel
            # print(0)
            self.save_command.cancel(2)

    def load_save_data(self, save_data_number):
        self.chapter = 0
        self.text_num = 0
        self.branch = ""
        self.credits = [0, 0, 0]

        self.frame = 0
        self.images = []

        if save_data_number is not None:
            self.name = self.saves[save_data_number]["name"]
            self.chapter = self.saves[save_data_number]["chapter"]
            self.branch = self.saves[save_data_number]["branch"]
            self.text_num = self.saves[save_data_number]["text_num"]
            self.credits = self.saves[save_data_number]["credits"]
