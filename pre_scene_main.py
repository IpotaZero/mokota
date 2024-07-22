from Ifunctions import *
from save import Save


class PreSceneMain:
    def __init__(self, saves: list[Save], config: dict) -> None:
        self.scene_name = "main"

        # このまま出てきたらえらー
        self.name = "ERROR"

        self.screen = self.screen = pygame.display.get_surface()
        self.buffer_screen = pygame.Surface(screen_option["default_size"])
        self.layer_background = pygame.Surface(screen_option["default_size"])
        self.layer_buttons = pygame.Surface(
            screen_option["default_size"], pygame.SRCALPHA
        )

        self.saves = saves
        self.config = config

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.save_data_num = None

        self.is_end = False

        self.chapter = 0
        self.branch = "first"
        self.text_num = 0
        self.frame = 0
        self.credits = [0, 0, 0]
        self.footprints = {}

        self.start()

    def start(self):
        self.popups = []

        self.skip = False
        self.auto = False

        self.log = []
        self.log_slicer = 0

        self.mode = "text"

        self.frame = 0

        self.story_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            540,
            RegexDict({}),
            title=RegexDict({"": "選択肢"}),
        )

        self.set_save_command()

        self.title_command = Icommand(
            self.layer_buttons,
            self.font,
            (255, 255, 255),
            50,
            200,
            RegexDict(
                {
                    "": ["タイトルに戻る", "設定", "再開する"],
                    "0": ["はい", "いいえ"],
                    "1": [
                        "画面サイズ",
                        ["BGM:", self.config["volume_bgm"], 0, 9],
                        ["SE :", self.config["volume_se"], 0, 9],
                        ["TEXT_SPEED:", self.config["text_speed"], 1, 5],
                        "やめる",
                    ],
                    "10": [
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
                }
            ),
            title=RegexDict({"0": "ほんとに?"}),
        )

        self.images: dict = {}
        self.letter_colour = (255, 255, 255)

        pygame.mixer.init()  # 初期化

        self.load_save_data(self.save_data_num)
