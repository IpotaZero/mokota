import pygame
from pygame.locals import *

from Ifunctions import *
from story import serifs


class EditScene:
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "edit"

        self.screen = screen
        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.chapter = 0
        self.camera = [0, 0]
        self.is_end = False
        self.frame = 0

        self.command = Icommand(
            self.screen,
            self.font,
            (255, 255, 255),
            800,
            90,
            RegexDict({"": ["編集する", "子を追加する", "削除する"]}),
        )

        # self.nodes = []

        # for branch in serifs[self.chapter].regex_dict:
        #     self.nodes.append({"id": branch, "nexts": []})

        self.mode = "observation"
        self.edit_target = ""

    def mainloop(self) -> None:
        self.screen.fill((255, 201, 224))

        if self.mode == "observation":
            speed = 20

            if K_RIGHT in keyboard["pressed"]:
                self.camera[0] -= speed
            elif K_LEFT in keyboard["pressed"]:
                self.camera[0] += speed

            if K_UP in keyboard["pressed"]:
                self.camera[1] += speed
            elif K_DOWN in keyboard["pressed"]:
                self.camera[1] -= speed
            elif K_RETURN in keyboard["pushed"]:
                self.is_end = True

            i = 0
            layer = 0

            for branch in serifs[self.chapter].regex_dict:
                if layer != len(branch):
                    i = 0
                    layer = len(branch)

                clicked = Ibutton(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    100 * i + self.camera[0],
                    50 * layer + self.camera[1],
                    100,
                    50,
                    branch,
                    text_align="center",
                )

                if clicked:
                    self.edit_target = branch

                i += 1

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                800,
                50,
                "",
                max_width=1100,
            )

            self.command.run()

            if self.command.is_match("0"):
                self.mode = "edit"
            elif self.command.is_match("1"):
                pass
            elif self.command.is_match("2"):
                pass

        pygame.display.update()  # 画面更新
