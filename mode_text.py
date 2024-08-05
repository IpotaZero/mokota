import json
from story import serifs
from Ifunctions import *

from pre_scene_main import PreSceneMain


class ModeText(PreSceneMain):
    def mainloop_text(self):
        pass

    def draw_backscreen(self):
        IImage(self.layer_background, "images/UI/テキスト背景.png", 13, 575, 1726 /1.5, 315/1.5)
            
        #Irect(self.layer_background, (0, 0, 0, 255 // 2), 30, 530, 1140, 250)

    def mode_text(self):
        self.draw_backscreen()

        chapter = serifs[self.chapter]
        if self.branch not in chapter:
            Itext(
                self.layer_buttons,
                self.font,
                (255, 255, 255),
                50,
                540,
                "知らないbranch: " + self.branch,
                max_width=1100,
                frame=self.frame / 2,
            )
            return

        branch = chapter[self.branch]
        if len(branch) <= self.text_num:
            Itext(
                self.layer_buttons,
                self.font,
                (255, 255, 255),
                50,
                540,
                "elementが存在しないtext_num",
                max_width=1100,
                frame=self.frame / 2,
            )
            return

        element = branch[self.text_num]

        if type(element) == str:
            self.solve_text(element)
        elif type(element) == list:
            self.solve_command(element)

    def solve_text(self, text: str):
        formated_text = text.format(name=self.name)

        if self.frame == 1:
            self.log.append(formated_text + ";")
            self.log_slicer = None

        clicked = Ibutton(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            (255, 255, 255),
            50,
            540,
            1100,
            190,
            "",
            line_width=0,
        )

        text_speed = [3, 2.5, 2, 1.5, 1][self.config["text_speed"] - 1]

        text_length = len(formated_text) * text_speed

        if (
            len({K_RETURN, K_SPACE} & keyboard["pushed"]) > 0
            or clicked
            or self.get_skip_flag()
            or (
                text_length + 30 <= self.frame
                and (
                    self.auto or len({K_RETURN, K_SPACE} & keyboard["long_pressed"]) > 0
                )
            )
        ):
            if text_length > self.frame:
                self.frame = text_length
            else:
                self.text_num += 1
                self.frame = 0
                self.update_passed_branches()
                return

            # if self.text_num == len(element_list):
            #     self.text_num = 0

        if self.frame % 60 < 30:
            formated_text += "▼"

        Itext(
            self.layer_buttons,
            self.font,
            (0, 0, 0),
            90,
            647,
            formated_text,
            max_width=1100,
            frame=self.frame / text_speed,
            line_size=60,
        )

    def update_passed_branches(self):
        passed_branches: list = self.config["passed_branches"]
        chapter = str(self.chapter)

        if chapter not in passed_branches:
            passed_branches[chapter] = {}

        if self.branch not in passed_branches[chapter]:
            passed_branches[chapter][self.branch] = 0

        passed_branches[chapter][self.branch] = max(
            self.text_num, passed_branches[chapter][self.branch]
        )

        with open("config.dat", "w") as f:
            f.write(json.dumps(self.config))

    def get_next_branch(self, command) -> str:
        element = command[1]
        if type(element) == str:
            return element
        elif type(element) == list:
            index = command[2](
                {
                    "footprints": self.footprints,
                    "max_credit": self.credits.index(max(self.credits)),
                }
            )
            self.footprints[self.branch] = index

            return element[index]

    def get_skip_flag(self):
        passed_branches: dict = self.config["passed_branches"]
        chapter = str(self.chapter)

        return self.skip and (
            self.config["debug_skip"]
            or (
                chapter in passed_branches
                and self.branch in passed_branches[chapter]
                and self.text_num < passed_branches[chapter][self.branch]
            )
        )

    def solve_command(self, command):
        if self.solve_1frame_command(command):
            self.solve_long_frame_command(command)

    def solve_1frame_command(self, command):
        command_type = command[0]

        # 次のブランチに進む
        if command_type == "goto":
            self.branch = self.get_next_branch(command)
            # print(self.branch)
            self.text_num = -1

        # 好感度を上げる
        elif command_type == "credit":
            num = command[1]
            self.credits[num] += 5

            # self.popups.append({"text": "LEVEL UP!", "life": 120})
            # print(self.saves[1].save_data)

        # 次のチャプターに進む
        elif command_type == "next_chapter":
            self.chapter += 1
            self.branch = "first"
            self.text_num = -1

            self.images.clear()
            pygame.mixer.music.fadeout(1000)

        # 効果音を流す
        elif command_type == "sound":
            se = pygame.mixer.Sound("sounds/se/" + command[1])
            se.set_volume(self.config["volume_se"] / 9)
            se.play()

        # BGMを流す
        elif command_type == "bgm":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/bgm/" + command[1])
            pygame.mixer.music.play(-1)

        # BGMを止める
        elif command_type == "stop_bgm":
            pygame.mixer.music.fadeout(1000)

        # 背景を変更する
        elif command_type == "image_back":
            path = "images/background/" + command[1]
            img = pygame.image.load(path).convert()

            # デフォルト値
            img_data = {
                "img": img,
                "size": screen_option["default_size"],
                "pos": (0, 0),
                "is_shown": True,
            }

            # オーダーメイド
            if len(command) >= 3:
                commands: dict = command[2]
                for key in commands:
                    img_data[key] = commands[key]

            self.images["back"] = img_data

        # 画像を変える[path, name, dict]
        elif command_type == "image":
            path = "images/" + command[1]
            img = pygame.image.load(path).convert()

            # デフォルト値
            img_data = {
                "img": img,
                "size": screen_option["default_size"],
                "pos": (0, 0),
                "is_shown": True,
            }

            # オーダーメイド
            if len(command) >= 4:
                commands: dict = command[3]
                for key in commands:
                    img_data[key] = commands[key]

            self.images[command[2]] = img_data

        # 画像を非表示、表示
        elif command_type == "image_onoff":
            image_name = command[1]

            self.images[image_name]["is_shown"] = command[2]

        # 画像を削除
        elif command_type == "image_delete":
            self.images.pop(command[1])

        elif command_type == "delete_image":
            r = command[1]
            del self.images[r]

        elif command_type == "character":
            name: str = command[1]
            place: int = command[2]  # 左、真ん中、右
            is_shown: bool = command[3] if len(command) > 3 else True

            size = (1536 / 2.5, 2048 / 2.5)

            pos = (
                (place - 1) * 400 + screen_option["default_size"][0] / 2 - size[0] / 2,
                185,
            )

            self.images[name] = {
                "img": pygame.image.load(
                    "images/character/" + name + ".png"
                ).convert_alpha(),
                "size": size,
                "pos": pos,
                "is_shown": is_shown,
            }

            self.images[name + "eye"] = {
                "img": pygame.image.load(
                    "images/character/" + "face" + ".png"
                ).convert_alpha(),
                "size": size,
                "pos": pos,
                "is_shown": is_shown,
            }

        else:
            return True

        self.text_num += 1
        self.frame = 0

        return False

    def solve_long_frame_command(self, command):
        command_type = command[0]

        if command_type == "question":
            if self.frame == 1:
                self.story_command.options.regex_dict[""] = command[1]

            self.story_command.run()

            if self.story_command.is_match("."):
                # ログに追加
                self.log.append(self.story_command.get_selected_option() + ";")
                # 分岐履歴
                self.footprints[self.branch] = self.story_command[0]
                # 次のbranch
                self.branch = command[2][self.story_command[0]]

                # リセット
                self.text_num = 0
                self.frame = 0
                self.story_command.reset()

        elif command_type == "darken":
            Irect(
                self.layer_background,
                (0, 0, 0, 255 * self.frame // 60),
                0,
                0,
                screen_option["default_size"][0],
                screen_option["default_size"][1],
            )

            if self.frame == 60:
                self.text_num += 1
                self.frame = 0

        elif command_type == "rdarken":
            scr = pygame.Surface(screen_option["default_size"], flags=pygame.SRCALPHA)
            scr.fill((0, 0, 0, 255 * (1 - self.frame / 60)))
            self.layer_background.blit(scr, (0, 0))

            if self.frame == 60:
                self.text_num += 1
                self.frame = 0

        elif command_type == "sleep":
            if command[1] * 60 <= self.frame:
                self.text_num += 1
                # self.pushed.clear()
                self.frame = 0
        else:
            Itext(
                self.layer_buttons,
                self.font,
                (255, 255, 255),
                50,
                540,
                f"知らないコマンド: {command_type}",
                max_width=1100,
            )

            if K_RETURN in keyboard["pushed"]:
                self.text_num += 1
                self.frame = 0
