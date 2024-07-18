import pygame
from pygame.locals import *

from Ifunctions import *
from scene import Scene
from story import serifs


class EditScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        self.scene_name = "edit"

        self.screen = screen
        super().__init__(screen)
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

        self.nodes = {}

        self.mode = "observation"
        self.edit_target = ""

        layer = 0

        for branch in serifs[self.chapter]:
            nexts = []

            element = serifs[self.chapter][branch][-1]

            if element[0] == "goto":
                if type(element[1]) == str:
                    nexts.append(element[1])
                elif type(element[1]) == list:
                    nexts += element[1]
            elif element[0] == "question":
                nexts += element[2]
            else:
                continue

            # print(nexts)

            if branch == "first":
                self.nodes["first"] = {"pos": (0, 0), "nexts": nexts}
                layer += 1
            else:
                self.nodes[branch]["nexts"] = nexts

            flag = False

            for i, next_branch in enumerate(nexts):
                if next_branch not in self.nodes:
                    self.nodes[next_branch] = {"pos": (400 * i, 100 * layer)}
                else:
                    flag = True

            if flag:
                continue

            layer += 1

        # print(self.nodes)

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

            for branch, value in self.nodes.items():
                if "nexts" in value:
                    for next_branch in value["nexts"]:
                        pygame.draw.line(
                            self.screen,
                            (255, 255, 255),
                            (
                                value["pos"][0] + self.camera[0] + 200,
                                value["pos"][1] + self.camera[1] + 25,
                            ),
                            (
                                self.nodes[next_branch]["pos"][0]
                                + self.camera[0]
                                + 200,
                                self.nodes[next_branch]["pos"][1] + self.camera[1] + 25,
                            ),
                        )

                clicked = Ibutton(
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    value["pos"][0] + self.camera[0],
                    value["pos"][1] + self.camera[1],
                    400,
                    50,
                    branch,
                    text_align="center",
                )

                if clicked:
                    self.edit_target = branch
                    print(branch)

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
