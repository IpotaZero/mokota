import pygame
from pygame.locals import *
import sys

import title_scene
import main_scene


def main():
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面

    pygame.display.set_caption("もこもこマイコン部")

    clock = pygame.time.Clock()

    pressed = []
    pushed = []

    scenes = {"main_scene": main_scene.MainScene(screen, pushed)}

    frame = 0

    current_scene = title_scene.TitleScene(screen, pushed)

    while True:
        frame += 1
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:  # 閉じるボタンが押されたら
                pygame.quit()  # 全てのpygameモジュールの初期化を解除
                sys.exit()  # 終了（ないとエラーで終了することになる）
            elif event.type == KEYDOWN:
                pressed.append(event.key)
                pushed.append(event.key)
            elif event.type == KEYUP:
                pressed.remove(event.key)

        current_scene.mainloop()

        if current_scene.is_end:
            current_scene = scenes[current_scene.next_scene_name]

        pushed.clear()
        clock.tick(60)


if __name__ == "__main__":
    main()
