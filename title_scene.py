import sys
import pygame
from pygame.locals import *


class TitleScene:
    def __init__(self, screen: pygame.Surface, pushed: list[int]) -> None:
        self.screen = screen
        self.pushed = pushed

        font = pygame.font.Font("DotGothic16-Regular.ttf", 74)

        # フォントの設定
        self.title_text = font.render("もこもこマイコン部", False, (255, 255, 255))

        self.arrow = font.render("→", False, (255, 255, 255))

        self.options = list(
            map(lambda x: font.render(x, False, (255, 255, 255)), ["あそぶ", "やめる"])
        )

        self.is_end = False

        self.next_scene_name = "main_scene"

        self.command = 0

    def mainloop(self) -> None:
        self.screen.fill((0, 0, 0))  # 背景を黒

        self.screen.blit(self.title_text, (20, 20))

        if K_UP in self.pushed:
            self.command -= 1
            self.command %= len(self.options)
        elif K_DOWN in self.pushed:
            self.command += 1
            self.command %= len(self.options)

        if K_RETURN in self.pushed:
            if self.command == 0:
                self.is_end = True
            elif self.command == 1:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.arrow, (20, 100 + self.command * 74))

        for i, option in enumerate(self.options):
            self.screen.blit(option, (94, 100 + i * 74))

        pygame.display.update()  # 画面更新
