import math
import pygame
import re
from pygame.locals import *

keyboard = {
    "pressed": [],
    "pushed": [],
    "long_pressed": [],
}

mouse = {
    "clicked": False,
    "long_clicked": False,
    "double_clicked": False,
    "right_clicked": False,
    "up": False,
    "down": False,
    "position": (0, 0),
    "last_click_time": 0,
}

screen_option = {
    "ratio": 1,
    "offset": (0, 0),
    "real_size": (0, 0),
}


def set_window_size(size):
    if size == (0, 0):
        # 画面サイズの取得
        real_width, real_height = screen_option["real_size"]

        # それぞれの比率を計算
        width_ratio = real_width / 1200
        height_ratio = real_height / 800

        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        if width_ratio <= height_ratio:
            ratio = width_ratio
            screen_option["offset"] = (0, (real_height - ratio * 800) / 2)
        else:
            ratio = height_ratio
            screen_option["offset"] = ((real_width - ratio * 1200) / 2, 0)

        # 収まる最大の比率を決定
        # ratio = min(width_ratio, height_ratio)
        screen_option["ratio"] = ratio
        return

    screen_option["ratio"] = size[0] / 1200
    screen_option["offset"] = (0, 0)

    pygame.display.set_mode(size)


def Iadjust(font: pygame.font.Font, text: str, max_width: int):
    blitx = 0

    adjusted = ""

    for char in text:
        # テキスト表示用Surfaceを作る
        # render(text, antialias, color)
        jtext = font.render(char, False, (255, 255, 255))

        if char == ";":
            blitx = 0

        # blit の前にはみ出さないかチェック
        if blitx + jtext.get_rect().w >= max_width:
            adjusted += ";"
            blitx = 0

        adjusted += char

        blitx += jtext.get_rect().w

    return adjusted


def Irect(
    screen: pygame.Surface,
    colour: tuple[int, int, int] | tuple[int, int, int, int],
    x: int,
    y: int,
    width: int,
    height: int,
):
    scr = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    scr.fill(colour)
    screen.blit(scr, (x, y))


def Itext(
    screen: pygame.Surface,
    font: pygame.font.Font,
    colour: tuple[int, int, int],
    x: int,
    y: int,
    text: str,
    frame: int = 10000,
    max_width: int = 10000,
    max_height: int = 10000,
    outline_width: int = 0,
    outline_colour: list[tuple[int, int, int]] = [(0, 0, 0)],
):
    blitx = 0
    blity = 0

    for i, char in enumerate(text):
        if i > frame:
            break

        # テキスト表示用Surfaceを作る
        # render(text, antialias, color)
        jtext = font.render(char, False, colour)

        if char == ";":
            blitx = 0
            blity += jtext.get_rect().h
            continue

        # blit の前にはみ出さないかチェック
        if blitx + jtext.get_rect().w >= max_width:
            blitx = 0
            blity += jtext.get_rect().h

        if blity >= max_height:
            break

        if outline_width > 0:
            for j, ocolour in enumerate(reversed(outline_colour)):
                jtext2 = font.render(char, False, ocolour)

                for i in range(8):
                    screen.blit(
                        jtext2,
                        (
                            x
                            + blitx
                            + math.cos(2 * math.pi * i / 8)
                            * outline_width
                            * (len(outline_colour) - j),
                            y
                            + blity
                            + math.sin(2 * math.pi * i / 8)
                            * outline_width
                            * (len(outline_colour) - j),
                        ),
                    )

        # 貼り付ける文字列、貼り付ける場所
        screen.blit(jtext, (x + blitx, y + blity))

        blitx += jtext.get_rect().w


def Ibutton(
    screen: pygame.Surface,
    font: pygame.font.Font,
    colour: tuple[int, int, int],
    text_colour: tuple[int, int, int],
    x: int,
    y: int,
    width: int,
    height: int,
    text: str,
    line_width=2,
    text_align="center",
    outline_width: int = 0,
    outline_colour: tuple[int, int, int] = (0, 0, 0),
):
    button = pygame.Rect(x, y, width, height)  # creates a rect object
    if line_width > 0:
        pygame.draw.rect(screen, colour, button, width=line_width)

    jtext = font.render(text, False, text_colour)
    text_width = jtext.get_rect().w / 2
    text_height = jtext.get_rect().h / 2

    if text_align == "center":
        Itext(
            screen,
            font,
            text_colour,
            x + width / 2 - text_width,
            y + height / 2 - text_height - 1,
            text,
            outline_width=outline_width,
            outline_colour=outline_colour,
        )

    elif text_align == "left":
        Itext(
            screen,
            font,
            text_colour,
            x,
            y,
            text,
            outline_width=outline_width,
            outline_colour=outline_colour,
        )

    if (
        mouse["clicked"]
        and x * screen_option["ratio"] + screen_option["offset"][0]
        <= mouse["position"][0]
        <= (x + width) * screen_option["ratio"] + screen_option["offset"][0]
        and y * screen_option["ratio"] + screen_option["offset"][1]
        <= mouse["position"][1]
        <= (y + height) * screen_option["ratio"] + screen_option["offset"][1]
    ):
        return True

    return False


def Iscroll(x: int, y: int, width: int, height: int) -> tuple[bool, str]:
    if not (mouse["up"] or mouse["down"]):
        return (False, "none")

    if (
        x * screen_option["ratio"] + screen_option["offset"][0]
        <= mouse["position"][0]
        <= (x + width) * screen_option["ratio"] + screen_option["offset"][0]
        and y * screen_option["ratio"] + screen_option["offset"][1]
        <= mouse["position"][1]
        <= (y + height) * screen_option["ratio"] + screen_option["offset"][1]
    ):
        if mouse["up"]:
            return (True, "up")
        else:
            return (True, "down")

    return (False, "none")


def Irange(screen, font: pygame.font.Font, colour, x, y, value):
    height = font.get_height()
    text = " " + str(value) + " "
    width = font.render(text, False, colour).get_rect().w

    is_clicked_left = Ibutton(
        screen,
        font,
        colour,
        colour,
        x,
        y,
        height,
        height,
        "◁",
        line_width=0,
    )

    Itext(screen, font, colour, x + height, y, text)

    is_clicked_right = Ibutton(
        screen,
        font,
        colour,
        colour,
        x + height + width,
        y,
        height,
        height,
        "▷",
        line_width=0,
    )

    s = Iscroll(x, y, x + width, height)

    if is_clicked_left or (s[0] and s[1] == "up"):
        return -1
    elif is_clicked_right or (s[0] and s[1] == "down"):
        return 1

    return 0


class RegexDict:
    def __init__(self, regex_dict: dict):
        self.regex_dict = regex_dict

    def __getitem__(self, target_string: str):
        for pattern, value in self.regex_dict.items():
            if re.match("^" + pattern + "$", target_string):
                return value
        return None

    def __setitem__(self, target_string, value):
        for pattern in self.regex_dict:
            if re.match("^" + pattern + "$", target_string):
                self.regex_dict[pattern] = value
                return

    def get_all(self, target_string: str):
        l = []
        for pattern, value in self.regex_dict.items():
            if re.match("^" + pattern + "$", target_string):
                l.append(value)
        return l


suuji = "0123456789abcdefghijklmnopqrstuvwxyz"


class Icommand:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        colour: tuple[int, int, int],
        x: int,
        y: int,
        options: RegexDict,
        outline_width: int = 0,
        outline_colour: tuple[int, int, int] = (0, 0, 0),
        title=RegexDict({}),
    ) -> None:
        self.screen = screen
        self.font = font
        self.colour = colour
        self.x = x
        self.y = y
        self.options = options
        self.title = title

        self.outline_width = outline_width
        self.outline_colour = outline_colour

        self.range_values = RegexDict({})

        for key in options.regex_dict:
            for option in options.regex_dict[key]:
                if type(option) == list:
                    if key not in self.range_values.regex_dict:
                        self.range_values.regex_dict[key] = []

                    self.range_values.regex_dict[key].append(option[1])

        self.reset()

    def reset(self):
        self.branch = ""
        self.num = 0

    def run(self):
        title = self.title[self.branch]

        if title is not None:
            Itext(
                self.screen,
                self.font,
                self.colour,
                self.x,
                self.y,
                title,
                outline_colour=self.outline_colour,
                outline_width=self.outline_width,
            )

        option = self.options[self.branch]

        if option is None or len(option) == 0:
            return

        if type(option[self.num]) == str:
            if K_RETURN in keyboard["pushed"] or K_SPACE in keyboard["pushed"]:
                self.branch += suuji[self.num]
                self.num = 0
                return
            elif (
                K_ESCAPE in keyboard["pushed"] or K_BACKSPACE in keyboard["pushed"]
            ) and self.branch != "":
                self.cancel()
                return

        if K_UP in keyboard["long_pressed"]:
            self.num += len(option) - 1
            self.num %= len(option)
        elif K_DOWN in keyboard["long_pressed"]:
            self.num += 1
            self.num %= len(option)

        j = 0
        for i, element in enumerate(option):
            if type(element) == list:
                Itext(
                    self.screen,
                    self.font,
                    self.colour,
                    self.x + self.font.get_height(),
                    self.y + self.font.get_height() * (i + 1),
                    option[i][0],
                    outline_width=self.outline_width,
                    outline_colour=self.outline_colour,
                )

                w = self.font.render(option[i][0], False, (0, 0, 0)).get_rect().w

                s = Irange(
                    self.screen,
                    self.font,
                    self.colour,
                    self.x + self.font.get_height() + w,
                    self.y + self.font.get_height() * (i + 1),
                    self.range_values[self.branch][j],
                )

                if i == self.num:
                    if K_RIGHT in keyboard["long_pressed"]:
                        s += 1
                    elif K_LEFT in keyboard["long_pressed"]:
                        s -= 1

                self.range_values[self.branch][j] = max(
                    min(self.range_values[self.branch][j] + s, element[3]), element[2]
                )
                j += 1
            else:
                width = self.font.render(element, False, (255, 255, 255)).get_rect().w
                selected = Ibutton(
                    self.screen,
                    self.font,
                    self.colour,
                    self.colour,
                    self.x + self.font.get_height(),
                    self.y + self.font.get_height() * (i + 1),
                    width,
                    self.font.get_height(),
                    element,
                    line_width=0,
                    text_align="left",
                    outline_width=self.outline_width,
                    outline_colour=self.outline_colour,
                )

                if selected:
                    self.branch += suuji[i]
                    self.num = 0
                    return

        Itext(
            self.screen,
            self.font,
            self.colour,
            self.x,
            self.y + self.font.get_height() * (self.num + 1),
            "→",
            outline_width=self.outline_width,
            outline_colour=self.outline_colour,
        )

    def get_range_value(self):
        return self.range_values[self.branch]

    def cancel(self, n=1):
        for _ in range(n):
            if self.branch == "":
                break
            self.num = self[-1]
            self.branch = self.branch[:-1]

    def get_selected_option(self):
        return self.options[self.branch[:-1]][self[-1]]

    def __getitem__(self, index):
        return suuji.index(self.branch[index])

    def is_match(self, key):
        return re.match("^" + key + "$", self.branch)
