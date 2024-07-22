import json
from Ifunctions import *
from save import Save


class ModeSave:
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
