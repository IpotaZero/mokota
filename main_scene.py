import json
import pygame
from pygame.locals import *

from Ifunctions import *

serifs = [
    RegexDict(
        {
            "": [
                "4月...",
                # "next_chapter",
                "俺の名前は{name}",
                "今年、大阪公立大に入学するしがない猫(?)だ",
                "そんな俺は今、とてつもなく悩んでいる;そう、どのサークルに入るか、だ",
                "入学してから2週間、俺はいまだにどのサークルにも入っていないのだ",
                "どのサークルに入るかが大学生活の行き先を決めるといっても過言ではない",
                "しかし、俺にはこれといって得意なこともないし;どうすっかなー...",
                "そんなことを考えながら俺は部活紹介の冊子をめくる",
                "{name}:;マイコン研究会...?",
                "俺はコンピュータには全く詳しくないが、ここなら俺みたいなオタクもいるかもしれないな",
                "そう考えて俺はそのマイコン研究会とやらを覗いてみることにした",
                "そういえば、幼馴染のもこ子;あいつもこの大学に入ったらしいけど、いったいどこの部活に入るんだろう...?",
                #
                "放課後...",
                "俺は今マイコン部の入り口にいる;ちょうど今日は体験入部の日だったのだ",
                "ここから俺の輝かしいコンピュータ人生が始まる...かどうかはわからないが、まあ楽しめたらいいかな",
                "そう思いながら俺はドアノブをひねる",
                "{name}:;失礼しま...",
                "???:;ご来場ありがとうございまーす!!",
                "{name}:;うわぁっ!?",
                "いきなりのクラッカーの音で俺は思わず後ろに転んでしまう",
                "???:;あはは、ごめんね! 大丈夫?",
                "明るい声とともに差し出された手;その先を見ると...",
                "{name}:;お前...もしかしてもこ子か!?",
                "もこ子:;およ? ...もしかして{name}くん? わー、おひさー! 中学ぶりだよね!",
                "そこにいたのは、なんともこ子だった!;久々に会ったからか、ずいぶん垢抜けたように見える",
                "???:;あら、もこ子のお友達?",
                "もこ子の後ろから顔がのぞく",
                "もこ子:;あっもこ美ちゃん! この人が私の幼馴染の{name}くんだよ!",
                "もこ美:;へぇ、あんたが {name} ね あたしは部長のもこ美、よろしくね!;まあ立ち話もなんだし、入りなさいよ",
                "もこ美と呼ばれた女の子に促され、俺は部室の中に入った",
                #
                "部屋は6畳ほどの広さで、壁際にデスクトップパソコンが4台置いてある",
                "天井近くまである本棚にはCDやプログラミング関連の本、そして...なぜか占いの本が",
                "ふと一番奥のパソコンを見ると、誰かが座っているのに気づいた",
                "もこ美:;ほらもこ音! あんたも挨拶しなさいよ!",
                "もこ音と呼ばれた女の子は椅子に座ったままこちらを向き、俺の顔を見つめる",
                "もこ音:;...ども",
                "もこ子:;もこ音ちゃんはねー、音楽とか作ってるんだよー! すごいよねー!",
                "{name}:;へえ、そうなのか すごいな! 俺も高校の時ちょっとやってたけど難しくて辞めちゃったんだよな",
                "もこ音:;そう...",
                "もこ音はあまり興味なさそうにディスプレイに向き直った;人見知りなのかもしれないな",
                "{name}:;そういえば、もこ子、お前はなんでこのサークルに入ったんだ?",
                "もこ子:;んー、えーっとね、実は私、高校の頃ゲーム作ってたの!",
                "{name}:;えっ!? お前がゲームを?",
                "あまりの驚きに俺は思わず目を丸くする;なぜなら、俺たちが中学の頃もこ子は不器用の代名詞だったからだ",
                "もこ子:;えへへー あんまりすごくはないけどね",
                "もこ美:;もこ子のコードはある意味すごいのよね... なんで動いてるのかしら...",
                "{name}:;は、はぁ ところであんたはこのサークルでどんなことをしてるんだ?",
                "もこ美:;あたしはプログラミングより、絵を描くことが多いわね;そういえば、あんたはこの部に入って何がしたいの?",
                "{name}:;俺は...",
                "question",
                ["音楽", "プログラミング", "美術"],
            ],
            "0": [
                "credit",
                0,
                "{name}:;音楽、もう一回やってみようかな",
                "もこ音:;!!",
                "もこ音がこちらをちらっと見る",
            ],
            "1": [
                "credit",
                1,
                "{name}:;プログラミングとか面白そうだな",
                "もこ子:;やったー! 一緒にやろうよ!",
            ],
            "2": [
                "credit",
                2,
                "{name}:;絵とか、描いてみたいな",
                "もこ美:;へえ、なかなかセンスがあるじゃない;悪くないわね",
            ],
            ".#": [
                "もこ美:;それにしても、よかったわ、今年は新入生が3人も入ってくれて;去年は1人も来なかったのよね",
                "{name}:;え、いや まだ入部すると決めてはいないんだけど 一応体験入部に来ただけっていうか...",
                "そう、俺は体験入部に来たのだ 他の部活も見てみたいし...",
            ],
            "0##": [
                "もこ音:;{name}君、入って...くれないの...?",
                "もこ美が無表情で、しかし訴えかけるような眼でこちらを見つめてくる",
            ],
            "1##": [
                "もこ子:;えー! 入ってよー! 一緒にプログラミングしようよー!",
                "もこ子が子どもみたいに少し怒った顔でこちらを見つめてくる",
            ],
            "2##": [
                "もこ美:;...ふん まあ、別にいいけど? 入る入らないはあんたの決めることだし",
                "もこ美は口を固く結んでそっぽを向いてしまった",
            ],
            ".###": [
                "そんな顔をされたら俺は...",
                "もこ:;～～～分かった分かった! 俺は、マイコン研究会に入部します!",
                "俺がそういった瞬間、みんなの表情がぱあっと明るくなる",
                "ああ、ここが俺の居場所なのかもな;俺はなぜだか漠然と、そう思った",
                "next_chapter",
            ],
        }
    ),
    # RegexDict(
    #     {
    #         "": [
    #             "7月...",
    #             "入部してから3か月、俺はすっかりマイコン部に入り浸っていた",
    #             #
    #             "そして今、夏休みが始まろうとしている!",
    #         ],
    #         "0": ["もこ音さんと"],
    #     }
    # ),
    RegexDict(
        {
            "": [
                "9月...",
                "bgm",
                "電車走行中2.mp3",
                "ガタンゴトン...ガタンゴトン...",
                "俺は今、電車に乗ってとある田舎町に向かっている",
                "もこ美の故郷であるその町では、今日、花火大会が行われるらしい",
                "俺は夕日に照らされた山をぼうっと眺めながら目的の駅に着くのを待っていた...",
                "stop_bgm",
                "sound",
                "電車のブレーキ.mp3",
                "sleep",
                3,
                "sound",
                "電車の圧搾空気排出.mp3",
                "sleep",
                1,
                #
                "{name}:;確か...この辺で集合だったよな...",
                "駅から出てきょろきょろとあたりを見回すと、浴衣の集団が目についた",
                "go",
            ],
            "0": [
                "もこ助:;お、来たな",
                "もこ子:;こんばんはー!",
                "もこ美:;やっと来たのね",
                "{name}:;お待たせ、もこ音さんは?",
                "もこ子:;まだ来てないけど...あっ! あれじゃない?",
                "もこ子が指さした方を見ると、紫色の浴衣に身を包んだもこ音さんがこちらに向かっていた",
                "もこ音:;す、すいません ちょっと着付けに時間がかかって...",
                "sleep",
                1,
                "俺は思わずその姿に見とれてしまい、声が出せなくなる",
            ],
            "1": [
                "もこ美:;あら、やっと来たのね まあもこ子はまだ来てないんだけど",
                "{name}:;え、あいつまだ来てないのか?",
                "まったく、あいつらしいな;そう思った直後、駅の方から声が聞こえてくる",
                "もこ子:;皆ー! ごめーん! おまたせー!",
                "もこ子は息を切らせながら俺たちの方へ走ってきた",
                "{name}:;",
            ],
            "2": [
                "{name}:;お待たせお待たせ あれ? もこ美は?",
                "もこ音:;まだ来てないですね",
            ],
        }
    ),
]


class MainScene:
    def __init__(
        self, screen: pygame.Surface, pushed: list[int], mouse: dict, saves: list[dict]
    ) -> None:
        self.scene_name = "main"

        self.name = "ERROR"

        self.screen = screen
        self.pushed = pushed
        self.mouse = mouse

        self.saves = saves

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.start()

    def start(self):
        self.log = []
        self.log_slicer = 0

        self.mode = "text"

        self.chapter = 0
        self.text_num = 0
        self.branch = ""
        self.frame = 0

        self.credits = [0, 0, 0]

        self.select = 0

        self.set_save_command()

        self.title_command = Icommand(
            self.pushed,
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            400,
            RegexDict({"": ["BACK TO TITLE", "RESUME"]}),
        )

        self.is_end = False

        pygame.mixer.init()  # 初期化

    def set_save_command(self):
        s = [
            save["name"] + ": chapter " + str(save["chapter"]) for save in self.saves
        ] + ["nodata"]

        self.save_command = Icommand(
            self.pushed,
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            80,
            RegexDict(
                {"": s, ".": ["LOAD", "SAVE", "CANCEL"], ".[0-1]": ["YES", "NO"]}
            ),
        )

    def mainloop(self) -> None:
        self.screen.fill((0, 0, 0))  # 背景を黒

        if self.mode == "text" or self.mode == "log":
            is_pushed_log = (
                Ibutton(
                    self.mouse,
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    30,
                    30,
                    80,
                    40,
                    "LOG",
                )
                or K_l in self.pushed
            )

        if self.mode == "text" or self.mode == "save":
            is_pushed_save = (
                Ibutton(
                    self.mouse,
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    690,
                    30,
                    80,
                    40,
                    "SAVE",
                )
                or K_s in self.pushed
            )

        if self.mode == "text" or self.mode == "pause":
            is_pushed_escape = (
                Ibutton(
                    self.mouse,
                    self.screen,
                    self.font,
                    (255, 255, 255),
                    (255, 255, 255),
                    690,
                    90,
                    80,
                    40,
                    "TITLE",
                )
                or K_ESCAPE in self.pushed
            )

        if self.mode == "text":
            if is_pushed_escape:
                self.mode = "pause"

            if is_pushed_log:
                self.mode = "log"

            if is_pushed_save:
                self.mode = "save"

            self.mode_text()

        elif self.mode == "log":
            if is_pushed_log:
                self.mode = "text"

            self.mode_log()

        elif self.mode == "save":
            if is_pushed_save:
                self.mode = "text"

            self.mode_save()

        elif self.mode == "pause":
            if is_pushed_escape:
                self.mode = "text"

            self.title_command.run()

            if self.title_command.branch == "0":
                self.is_end = True

            elif self.title_command.branch == "1":
                self.mode = "text"
                self.title_command.branch = ""

        pygame.display.update()  # 画面更新

        self.frame += 1

    def mode_text(self):
        element = serifs[self.chapter][self.branch][self.text_num]

        if element == "question":
            options = serifs[self.chapter][self.branch][self.text_num + 1]

            if K_DOWN in self.pushed:
                self.select += 1
                self.select %= len(options)
            elif K_UP in self.pushed:
                self.select += len(options) - 1
                self.select %= len(options)
            elif K_RETURN in self.pushed or K_SPACE in self.pushed:
                self.branch += str(self.select)
                self.text_num = 0
                self.frame = 0

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                400 + self.select * 48,
                "→",
                max_width=700,
                frame=self.frame / 2,
            )

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50 + 32,
                400,
                ";".join(options),
                max_width=700,
                frame=self.frame / 2,
            )

        elif element == "credit":
            num = serifs[self.chapter][self.branch][self.text_num + 1]
            self.credits[num] += 1
            self.text_num += 2
            self.frame = 0

        elif element == "next_chapter":
            self.chapter += 1
            self.branch = ""
            self.text_num = 0
            self.frame = 0

        elif element == "go":
            self.branch += str(self.credits.index(max(self.credits)))
            self.text_num = 0
            self.frame = 0

        elif element == "sound":
            pygame.mixer.Sound(
                "sounds/" + serifs[self.chapter][self.branch][self.text_num + 1]
            ).play()
            self.text_num += 2
            self.frame = 0

        elif element == "bgm":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(
                "sounds/" + serifs[self.chapter][self.branch][self.text_num + 1]
            )
            pygame.mixer.music.play(-1)
            self.text_num += 2
            self.frame = 0

        elif element == "stop_bgm":
            pygame.mixer.music.fadeout(1000)
            self.text_num += 1
            self.frame = 0

        elif element == "sleep":
            if serifs[self.chapter][self.branch][self.text_num + 1] * 60 <= self.frame:
                self.text_num += 2
                # self.pushed.clear()
                self.frame = 0

        else:
            t = serifs[self.chapter][self.branch][self.text_num].format(name=self.name)

            if self.frame == 1:
                self.log.append(t)
                self.log_slicer = None

            if K_RETURN in self.pushed or K_SPACE in self.pushed:
                text_length = len(t) * 2

                if text_length > self.frame:
                    self.frame = text_length
                else:
                    self.text_num += 1
                    self.frame = 0

                if self.text_num == len(serifs[self.chapter][self.branch]):
                    self.text_num = 0
                    self.branch += "#"

            if self.frame % 60 < 30:
                t += "▼"

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                400,
                t,
                max_width=700,
                frame=self.frame / 2,
            )

    def mode_log(self):

        text = Iadjust(self.font, ";".join(self.log), 700)

        row = text.split(";")

        if self.log_slicer is None:
            self.log_slicer = len(row) - 9

        Itext(
            self.screen,
            self.font,
            (255, 255, 255),
            50,
            80,
            ";".join(row[self.log_slicer :]),
            max_width=700,
            max_height=400,
        )

        line = len(row)

        if line > 9:
            if line - self.log_slicer > 9:
                Itext(self.screen, self.font, (255, 255, 255), 380, 500, "▼")

                if K_DOWN in self.pushed:
                    self.log_slicer += 1
                    self.log_slicer %= line
            if self.log_slicer > 0:
                Itext(self.screen, self.font, (255, 255, 255), 380, 30, "▲")

                if K_UP in self.pushed:
                    self.log_slicer += line - 1
                    self.log_slicer %= line

    def mode_save(self):
        self.save_command.run()

        if self.save_command.branch == "":
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "Choose Save Data")

        elif re.match("^.$", self.save_command.branch):
            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                40,
                self.save_command.options[""][int(self.save_command.branch)],
            )
        elif re.match("^.[0-1]$", self.save_command.branch):
            Itext(self.screen, self.font, (255, 255, 255), 50, 40, "Really?")

        # print(self.save_command.branch, self.save_command.num)

        if re.match("^.00$", self.save_command.branch):
            # load->yes
            save_data_number = int(self.save_command.branch[0])

            if len(self.saves) <= save_data_number:
                self.save_command.cancel()
                return

            self.load_save_data(save_data_number)

            self.save_command.cancel(3)

        elif re.match("^.10$", self.save_command.branch):
            # save->yes
            save_data_number = int(self.save_command.branch[0])

            if len(self.saves) <= save_data_number:
                self.saves.append({})

            # print(self.saves, save_data_number)

            self.saves[save_data_number]["name"] = self.name
            self.saves[save_data_number]["chapter"] = self.chapter
            self.saves[save_data_number]["branch"] = self.branch
            self.saves[save_data_number]["text_num"] = self.text_num
            self.saves[save_data_number]["credits"] = self.credits

            with open("save.dat", "w") as f:
                f.write(json.dumps(self.saves))

            self.save_command.cancel(3)

            self.set_save_command()

        elif re.match("^.[0-1]1$", self.save_command.branch):
            # yes/no
            self.save_command.cancel(2)

        elif re.match("^.2$", self.save_command.branch):
            # cancel
            # print(0)
            self.save_command.cancel(2)

    def load_save_data(self, save_data_number):
        self.name = self.saves[save_data_number]["name"]
        self.chapter = self.saves[save_data_number]["chapter"]
        self.branch = self.saves[save_data_number]["branch"]
        self.text_num = self.saves[save_data_number]["text_num"]
        self.credits = self.saves[save_data_number]["credits"]

        self.frame = 0
