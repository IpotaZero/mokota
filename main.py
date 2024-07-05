import json
import os
import pygame
from pygame.locals import *
import sys

import title_scene
import main_scene
import name_scene


def main():
    saves = []

    if os.path.isfile("save.dat"):
        with open("save.dat") as f:
            saves = json.loads(f.read())
    else:
        with open("save.dat", "w") as f:
            f.write(json.dumps(saves))

    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面

    pygame.display.set_caption("MicroComputerReserch!")

    clock = pygame.time.Clock()

    pressed = []
    pushed = []
    mouse = {"clicked": False, "position": (0, 0)}

    scenes = {
        "main": main_scene.MainScene(screen, pushed, mouse, saves),
        "name": name_scene.NameScene(screen, pushed, mouse),
        "title": title_scene.TitleScene(screen, pushed, mouse, saves),
    }

    frame = 0

    current_scene = scenes["title"]

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
            elif event.type == MOUSEBUTTONDOWN:
                mouse["clicked"] = True
                mouse["position"] = event.pos

        r = current_scene.mainloop()

        if current_scene.is_end:
            current_scene.is_end = False
            if current_scene.scene_name == "title":
                if r is None:
                    current_scene = scenes["name"]
                else:
                    current_scene = scenes["main"]
                    current_scene.load_save_data(r)

            elif current_scene.scene_name == "name":
                current_scene = scenes["main"]
                current_scene.name = r

            elif current_scene.scene_name == "main":
                current_scene = scenes["title"]

            current_scene.start()

        pushed.clear()
        mouse["clicked"] = False
        clock.tick(60)


if __name__ == "__main__":
    main()
