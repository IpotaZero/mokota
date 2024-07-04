import time
import pygame
from pygame.locals import *

from Ifunctions import *

serifs = [
    RegexDict(
        {
            "": [
                "4月...",
                "next_chapter",
                "俺の名前はもこた",
                "今年、大阪公立大に入学するしがない猫(?)だ",
                "そんな俺は今、とてつもなく悩んでいる;そう、どのサークルに入るか、だ",
                "入学してから2週間、俺はいまだにどのサークルにも入っていないのだ",
                "どのサークルに入るかが大学生活の行き先を決めるといっても過言ではない",
                "しかし、俺にはこれといって得意なこともないし;どうすっかなー...",
                "そんなことを考えながら俺は部活紹介の冊子をめくる",
                "もこた:;マイコン研究会...?",
                "俺はコンピュータには全く詳しくないが、ここなら俺みたいなオタクもいるかもしれないな",
                "そう考えて俺はそのマイコン研究会とやらを覗いてみることにした",
                "そういえば、幼馴染のもこ子;あいつもこの大学に入ったらしいけど、いったいどこの部活に入るんだろう...?",
                #
                "放課後...",
                "俺は今マイコン部の入り口にいる;ちょうど今日は体験入部の日だったのだ",
                "ここから俺の輝かしいコンピュータ人生が始まる...かどうかはわからないが、まあ楽しめたらいいかな",
                "そう思いながら俺はドアノブをひねる",
                "もこた:;失礼しま...",
                "???:;ご来場ありがとうございまーす!!",
                "もこた:;うわぁっ!?",
                "いきなりのクラッカーの音で俺は思わず後ろに転んでしまう",
                "???:;あはは、ごめんね! 大丈夫?",
                "明るい声とともに差し出された手;その先を見ると...",
                "もこた:;お前...もしかしてもこ子か!?",
                "もこ子:;およ? ...もしかしてもこたくん? わー、おひさー! 中学ぶりだよね!",
                "そこにいたのは、なんともこ子だった!;久々に会ったからか、ずいぶん垢抜けたように見える",
                "???:;あら、もこ子のお友達?",
                "もこ子の後ろから顔がのぞく",
                "もこ子:;あっもこ美ちゃん! この人が私の幼馴染のもこたくんだよ!",
                "もこ美:;へぇ、あんたが もこた ね あたしは部長のもこ美、よろしくね!;まあ立ち話もなんだし、入りなさいよ",
                "もこ美と呼ばれた女の子に促され、俺は部室の中に入った",
                #
                "部屋は6畳ほどの広さで、壁際にデスクトップパソコンが4台置いてある",
                "天井近くまである本棚にはCDやプログラミング関連の本、そして...なぜか占いの本が",
                "ふと一番奥のパソコンを見ると、誰かが座っているのに気づいた",
                "もこ美:;ほらもこ音! あんたも挨拶しなさいよ!",
                "もこ音と呼ばれた女の子は椅子に座ったままこちらを向き、俺の顔を見つめる",
                "もこ音:;...ども",
                "もこ子:;もこ音ちゃんはねー、音楽とか作ってるんだよー! すごいよねー!",
                "もこた:;へえ、そうなのか すごいな! 俺も高校の時ちょっとやってたけど難しくて辞めちゃったんだよな",
                "もこ音:;そう...",
                "もこ音はあまり興味なさそうにディスプレイに向き直った;人見知りなのかもしれないな",
                "もこた:;そういえば、もこ子、お前はなんでこのサークルに入ったんだ?",
                "もこ子:;んー、えーっとね、実は私、高校の頃ゲーム作ってたの!",
                "もこた:;えっ!? お前がゲームを?",
                "あまりの驚きに俺は思わず目を丸くする;なぜなら、俺たちが中学の頃もこ子は不器用の代名詞だったからだ",
                "もこ子:;えへへー あんまりすごくはないけどね",
                "もこ美:;もこ子のコードはある意味すごいのよね... なんで動いてるのかしら...",
                "もこた:;は、はぁ ところであんたはこのサークルでどんなことをしてるんだ?",
                "もこ美:;あたしはプログラミングより、絵を描くことが多いわね;そういえば、あんたはこの部に入って何がしたいの?",
                "もこた:;俺は...",
                "question",
                ["音楽", "プログラミング", "美術"],
            ],
            "0": [
                "credit",
                0,
                "もこた:;音楽、もう一回やってみようかな",
                "もこ音:;!!",
                "もこ音がこちらをちらっと見る",
            ],
            "1": [
                "credit",
                1,
                "もこた:;プログラミングとか面白そうだな",
                "もこ子:;やったー! 一緒にやろうよ!",
            ],
            "2": [
                "credit",
                2,
                "もこた:;絵とか、描いてみたいな",
                "もこ美:;へえ、なかなかセンスがあるじゃない;悪くないわね",
            ],
            ".#": [
                "もこ美:;それにしても、よかったわ、今年は新入生が3人も入ってくれて;去年は1人も来なかったのよね",
                "もこた:;え、いや まだ入部すると決めてはいないんだけど 一応体験入部に来ただけっていうか...",
                "そう、俺は体験入部に来たのだ 他の部活も見てみたいし...",
            ],
            "0##": [
                "もこ音:;もこた君、入って...くれないの...?",
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
                "俺がそういった瞬間、みんなの表情がパッと明るくなる",
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
                "もこた:;確か...この辺で集合だったよな...",
                "駅から出てきょろきょろとあたりを見回すと、浴衣の集団が目についた",
                "go",
            ],
            "0": [
                "もこ助:;お、来たな",
                "もこ子:;こんばんはー!",
                "もこ美:;やっと来たのね",
                "もこた:;お待たせ、もこ音さんは?",
                "もこ子:;まだ来てないけど...あっ! あれじゃない?",
                "もこ子が指さした方を見ると、紫色の浴衣に身を包んだもこ音さんがこちらに向かっていた",
                "もこ音:;す、すいません ちょっと着付けに時間がかかって...",
                "sleep",
                1,
                "俺は思わずその姿に見とれてしまい、声が出せなくなる",
            ],
            "1": [
                "もこ美:;あら、やっと来たのね まあもこ子はまだ来てないんだけど",
                "もこた:;え、あいつまだ来てないのか?",
                "まったく、あいつらしいな;そう思った直後、駅の方から声が聞こえてくる",
                "もこ子:;皆ー! ごめーん! おまたせー!",
                "もこ子は息を切らせながら俺たちの方へ走ってきた",
            ],
            "2": [""],
        }
    ),
]


class MainScene:
    def __init__(self, screen: pygame.Surface, pushed: list[int]) -> None:
        self.screen = screen
        self.pushed = pushed

        self.font = pygame.font.Font("DotGothic16-Regular.ttf", 32)

        self.chapter = 0
        self.text_num = 0
        self.branch = ""
        self.frame = 0

        self.credits = [0, 0, 0]

        self.select = 0

        self.is_end = False

        self.next_scene_name = "main_scene"

        pygame.mixer.init()  # 初期化

    def mainloop(self) -> None:
        self.screen.fill((0, 0, 0))  # 背景を黒

        element = serifs[self.chapter][self.branch][self.text_num]

        if element == "question":
            options = serifs[self.chapter][self.branch][self.text_num + 1]
            if K_DOWN in self.pushed:
                self.select += 1
                self.select %= len(options)
            elif K_UP in self.pushed:
                self.select += len(options) - 1
                self.select %= len(options)
            elif K_RETURN in self.pushed:
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
                700,
                self.frame / 2,
            )

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50 + 32,
                400,
                ";".join(options),
                700,
                self.frame / 2,
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

        elif element == "bgm":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(
                "sounds/" + serifs[self.chapter][self.branch][self.text_num + 1]
            )
            pygame.mixer.music.play(-1)
            self.text_num += 2

        elif element == "stop_bgm":
            pygame.mixer.music.fadeout(1000)
            self.text_num += 1

        elif element == "sleep":
            time.sleep(serifs[self.chapter][self.branch][self.text_num + 1])
            self.text_num += 2
            self.pushed.clear()

        else:
            if K_RETURN in self.pushed:
                text_length = len(serifs[self.chapter][self.branch][self.text_num]) * 2

                if text_length > self.frame:
                    self.frame = text_length
                else:
                    self.text_num += 1
                    self.frame = 0

                if self.text_num == len(serifs[self.chapter][self.branch]):
                    self.text_num = 0
                    self.branch += "#"

            t = serifs[self.chapter][self.branch][self.text_num]

            if self.frame % 60 < 30:
                t += "▼"

            Itext(
                self.screen,
                self.font,
                (255, 255, 255),
                50,
                400,
                t,
                700,
                self.frame / 2,
            )

        pygame.display.update()  # 画面更新

        self.frame += 1
