import copy
import json
from Ifunctions import *
from save import Save
from story import serifs

from pre_scene_main import PreSceneMain


class ModeSave(PreSceneMain):
    def mode_save(self):
        self.save_command.run()

        if self.save_command.is_match(""):
            for i, save in enumerate(self.saves):
                current_text = '"' + save.current_text(18) + '"'

                Itext(
                    self.layer_buttons,
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
                self.layer_buttons,
                self.font,
                (255, 255, 255),
                50,
                40,
                self.save_command.get_selected_option() + current_text,
            )

        if self.save_command.is_match(".00"):
            # load->yes
            save_data_number = self.save_command[0]

            if len(self.saves) == save_data_number:
                self.save_command.cancel()
                return

            self.load_save_data(save_data_number)

            self.save_command.cancel(3)

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

            self.set_save_command()

            self.save_command.cancel(3)

        elif self.save_command.is_match(".20"):
            save_data_number = self.save_command[0]

            if len(self.saves) == save_data_number:
                self.save_command.cancel()
                return

            self.saves.pop(save_data_number)

            with open("save.dat", "w") as f:
                f.write(json.dumps([save.save_data for save in self.saves]))

            self.set_save_command()

            self.save_command.cancel(3)

        elif self.save_command.is_match(".[0-2]1"):
            # yes/no
            self.save_command.cancel(2)

        elif self.save_command.is_match(".3"):
            # cancel
            # print(0)
            self.save_command.cancel(2)

    def load_save_data(self, save_data_number):
        Itext(
            self.buffer_screen,
            self.font,
            (255, 255, 255),
            950,
            700,
            "NOW LOADING...",
        )

        scr = pygame.transform.scale(
            self.buffer_screen,
            (
                screen_option["default_size"][0] * screen_option["ratio"],
                screen_option["default_size"][1] * screen_option["ratio"],
            ),
        )

        self.screen.blit(scr, screen_option["offset"])
        pygame.display.update()

        self.chapter = 0
        self.text_num = 0
        self.branch = "first"
        self.credits = [0, 0, 0]
        self.footprints = {}

        self.log = []
        self.log_slicer = 0
        self.frame = 0
        self.images = {}

        pygame.mixer.music.fadeout(1000)

        if save_data_number is not None:
            save: Save = self.saves[save_data_number]
            self.name = save["name"]
            self.chapter = save["chapter"]
            self.branch = save["branch"]
            self.text_num = save["text_num"]
            self.credits = copy.deepcopy(save["credits"])
            self.footprints = copy.deepcopy(save["footprints"])

            chapter = save["chapter"]
            branch = "first"
            text_num = 0

            # bgmがちょっと漏れる
            pygame.mixer.music.set_volume(0)

            while (branch, text_num) != (save["branch"], save["text_num"]):
                self.frame = 1

                element = serifs[chapter][branch][text_num]
                text_num += 1

                if type(element) == str:
                    self.solve_text(element)
                    continue

                if element[0] == "goto":
                    branch = self.get_next_branch(element)
                    text_num = 0

                elif element[0] == "question":
                    # print(self.footprints)
                    branch = element[2][save["footprints"][branch]]
                    text_num = 0

                elif element[0] not in ["sound"]:
                    self.solve_1frame_command(element)

            self.name = save["name"]
            self.chapter = save["chapter"]
            self.branch = save["branch"]
            self.text_num = save["text_num"]
            self.credits = copy.deepcopy(save["credits"])
            self.footprints = copy.deepcopy(save["footprints"])

            self.frame = 0

            pygame.mixer.music.set_volume(self.config["volume_bgm"] / 9)
