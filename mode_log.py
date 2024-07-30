from Ifunctions import *

from pre_scene_main import PreSceneMain


class ModeLog(PreSceneMain):
    def mainloop_log(self):
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

        if self.mode == "log":
            if is_pushed_log:
                self.mode = "text"

            self.mode_log()

        elif self.mode == "text":
            if is_pushed_log:
                self.mode = "log"

    def mode_log(self):
        Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 30, 1140, 750)

        text = Iadjust(self.font, ";".join(self.log), 1100)

        row = text.split(";")

        max_row_num = 14

        if self.log_slicer is None:
            self.log_slicer = max([len(row) - max_row_num, 0])

        Itext(
            self.layer_buttons,
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
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    150,
                    750,
                    900,
                    30,
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
                    self.layer_buttons,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    150,
                    30,
                    900,
                    30,
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
