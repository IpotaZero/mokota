import pygame
import re
from pygame.locals import *


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

        # 貼り付ける文字列、貼り付ける場所
        screen.blit(jtext, (x + blitx, y + blity))

        blitx += jtext.get_rect().w


def Ibutton(
    mouse: dict,
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
    text_alighn="center",
):
    button = pygame.Rect(x, y, width, height)  # creates a rect object
    if line_width > 0:
        pygame.draw.rect(screen, colour, button, width=line_width)

    jtext = font.render(text, False, text_colour)
    text_width = jtext.get_rect().w / 2
    text_height = jtext.get_rect().h / 2

    if text_alighn == "center":
        screen.blit(
            jtext, (x + width / 2 - text_width, y + height / 2 - text_height - 1)
        )
    elif text_alighn == "left":
        screen.blit(jtext, (x, y + height / 2 - text_height - 1))

    if (
        mouse["clicked"]
        and x <= mouse["position"][0] <= x + width
        and y <= mouse["position"][1] <= y + height
    ):
        return True

    return False


class RegexDict:
    def __init__(self, regex_dict: dict):
        self.regex_dict = regex_dict

    def __getitem__(self, target_string):
        for pattern, value in self.regex_dict.items():
            if re.match("^" + pattern + "$", target_string):
                return value
        return None


class Icommand:
    def __init__(
        self,
        mouse: dict,
        pushed: list[int],
        screen: pygame.Surface,
        font: pygame.font.Font,
        colour: tuple[int, int, int],
        x: int,
        y: int,
        options: RegexDict,
    ) -> None:
        self.mouse = mouse
        self.pushed = pushed
        self.screen = screen
        self.font = font
        self.colour = colour
        self.x = x
        self.y = y
        self.options = options

        self.reset()

    def reset(self):
        self.branch = ""
        self.num = 0

    def run(self):
        option = self.options[self.branch]

        if K_RETURN in self.pushed or K_SPACE in self.pushed:
            if option is None:
                return
            self.branch += str(self.num)
            self.num = 0
            return
        elif (
            K_ESCAPE in self.pushed or K_BACKSPACE in self.pushed
        ) and self.branch != "":
            self.cancel()
            return

        if option is None:
            return

        if len(option) > 0:
            if K_UP in self.pushed:
                self.num += len(option) - 1
                self.num %= len(option)
            elif K_DOWN in self.pushed:
                self.num += 1
                self.num %= len(option)

        for i, text in enumerate(option):
            width = self.font.render(text, False, (255, 255, 255)).get_rect().w
            selected = Ibutton(
                self.mouse,
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
                text_alighn="left",
            )

            if selected:
                self.branch += str(i)
                self.num = 0
                return

        Itext(
            self.screen,
            self.font,
            self.colour,
            self.x,
            self.y + self.font.get_height() * self.num,
            "→",
        )

    def cancel(self, n=1):
        for _ in range(n):
            if self.branch != "":
                self.num = int(self.branch[-1])
                self.branch = self.branch[:-1]
