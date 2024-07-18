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


class RegexDict:
    def __init__(self, regex_dict: dict):
        self.regex_dict = regex_dict

    def __getitem__(self, target_string: str):
        for pattern, value in self.regex_dict.items():
            if re.match("^" + pattern + "$", target_string):
                return value
        return None

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
    ) -> None:
        self.screen = screen
        self.font = font
        self.colour = colour
        self.x = x
        self.y = y
        self.options = options

        self.outline_width = outline_width
        self.outline_colour = outline_colour

        self.reset()

    def reset(self):
        self.branch = ""
        self.num = 0

    def run(self):
        option = self.options[self.branch]

        if option is None:
            return

        if K_RETURN in keyboard["pushed"] or K_SPACE in keyboard["pushed"]:
            self.branch += suuji[self.num]
            self.num = 0
            return
        elif (
            K_ESCAPE in keyboard["pushed"] or K_BACKSPACE in keyboard["pushed"]
        ) and self.branch != "":
            self.cancel()
            return

        if len(option) > 0:
            if K_UP in keyboard["long_pressed"]:
                self.num += len(option) - 1
                self.num %= len(option)
            elif K_DOWN in keyboard["long_pressed"]:
                self.num += 1
                self.num %= len(option)

        for i, text in enumerate(option):
            width = self.font.render(text, False, (255, 255, 255)).get_rect().w
            selected = Ibutton(
                self.screen,
                self.font,
                self.colour,
                self.colour,
                self.x + self.font.get_height(),
                self.y + self.font.get_height() * i,
                width,
                self.font.get_height(),
                text,
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
            self.y + self.font.get_height() * self.num,
            "→",
            outline_width=self.outline_width,
            outline_colour=self.outline_colour,
        )

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
