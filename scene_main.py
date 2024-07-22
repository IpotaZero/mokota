import pygame
from pygame.locals import *

from Ifunctions import *
from mode_text import ModeText
from mode_save import ModeSave
from mode_log import ModeLog
from mode_pause import ModePause


class SceneMain(ModeText, ModeSave, ModeLog, ModePause):
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
