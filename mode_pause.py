import json
from Ifunctions import *

from pre_scene_main import PreSceneMain


class ModePause(PreSceneMain):
    def mainloop_pause(self):
        pass

    def mode_pause(self):
        Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 30, 1140, 750)

        # Itext(
        #     self.layer_buttons,
        #     self.font,
        #     (255, 255, 255),
        #     50,
        #     30,
        #     ";".join(
        #         [
        #             ["もこ音", "もこ子", "もこ美"][i] + ": " + str(self.credits[i])
        #             for i in range(3)
        #         ]
        #     ),
        # )

        self.title_command.run()

        if self.title_command.is_match("0"):
            self.mode = "text"

        elif self.title_command.is_match("1"):
            g, h, i = self.title_command.get_range_value()
            if (
                self.config["volume_bgm"],
                self.config["volume_se"],
                self.config["text_speed"],
            ) != (g, h, i):
                (
                    self.config["volume_bgm"],
                    self.config["volume_se"],
                    self.config["text_speed"],
                ) = (g, h, i)
                pygame.mixer.music.set_volume(g / 9)

                with open("config.dat", "w") as f:
                    f.write(json.dumps(self.config))

        elif self.title_command.is_match("11."):
            if self.title_command[2] == 8:
                self.title_command.cancel(2)
                return

            size = [
                (0, 0),
                (600, 400),
                (800, 533),
                (900, 600),
                (1200, 800),
                (1500, 1000),
                (1800, 1200),
                (2400, 1600),
            ][self.title_command[2]]

            set_window_size(size)

            self.config["window_size"] = size

            with open("config.dat", "w") as f:
                f.write(json.dumps(self.config))

            self.title_command.cancel(1)

        elif self.title_command.is_match("10"):
            self.title_command.cancel(2)

        elif self.title_command.is_match("20"):
            self.is_end = True
            pygame.mixer.music.fadeout(1000)

        elif self.title_command.is_match("21"):
            self.title_command.cancel(2)
