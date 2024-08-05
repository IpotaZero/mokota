from Ifunctions import *
from save import Save


class PreSceneMain:
    def __init__(self, saves: list[Save], config: dict) -> None:
        self.scene_name = "main"
        self.is_end = False

        self.screen = self.screen = pygame.display.get_surface()
        self.buffer_screen = pygame.Surface(screen_option["default_size"])
        self.layer_background = pygame.Surface(screen_option["default_size"])
        self.layer_buttons = pygame.Surface(
            screen_option["default_size"], pygame.SRCALPHA
        )

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        # このまま出てきたらえらー
        self.name = "ERROR"

        self.saves = saves
        self.config = config

        self.save_data_num = None

        # 初期値
        self.chapter = 0
        self.branch = "first"
        self.text_num = 0
        self.credits = [0, 0, 0]
        self.footprints = {}

        self.log = []
        self.log_slicer = 0
        self.frame = 0
        self.images: dict = {}

        self.story_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            540 - self.font.get_height(),
            RegexDict({}),
            # title=RegexDict({"": "選択肢"}),
        )

        self.save_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            80 - self.font.get_height(),
            RegexDict(
                {
                    "": ["ERROR"],
                    ".": ["ロード", "セーブ", "削除", "やめる"],
                    ".[0-2]": ["はい", "いいえ"],
                    # ".2": ["ERROR"],
                }
            ),
            title=RegexDict({"": "セーブデータを選択", ".[0-2]": "ほんとに?"}),
        )

        self.start()

    def start(self):
        self.popups = []

        self.skip = False
        self.auto = False

        self.mode = "text"

        self.story_command.reset()

        self.set_save_command()

        self.title_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            200,
            RegexDict(
                {
                    "": ["再開する", "設定", "タイトルに戻る"],
                    "1": [
                        "やめる",
                        "画面サイズ",
                        ["BGM:", self.config["volume_bgm"], 0, 9],
                        ["SE :", self.config["volume_se"], 0, 9],
                        ["TEXT_SPEED:", self.config["text_speed"], 1, 5],
                    ],
                    "11": [
                        "フルスクリーン",
                        "600x400",
                        "800x533",
                        "900x600",
                        "1200x800",
                        "1500x1000",
                        "1800x1200",
                        "2400x1600",
                        "やめる",
                    ],
                    "2": ["はい", "いいえ"],
                }
            ),
            title=RegexDict({"0": "ほんとに?"}),
        )

        self.letter_colour = (255, 255, 255)

        pygame.mixer.init()  # 初期化

        self.load_save_data(self.save_data_num)

    def set_save_command(self):
        save_data_list = [
            save["name"] + ": chapter " + str(save["chapter"]) for save in self.saves
        ] + ["空のデータ"]

        self.save_command.options.regex_dict[""] = save_data_list

        self.save_command.reset()
