import json
import os
import pygame
from pygame.locals import *
import sys
import time

import title_scene
import main_scene
import name_scene
import darkening_scene
from story import Save

from Ifunctions import keyboard, mouse


def main():
    saves: list[Save] = []

    if os.path.isfile("save.dat"):
        with open("save.dat") as f:
            try:
                for save in json.loads(f.read()):
                    saves.append(Save(save))
            except json.JSONDecodeError:
                print("データが破損しているのです!")

    else:
        with open("save.dat", "w") as f:
            f.write(json.dumps(saves))

    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((1200, 800))  # 800*600の画面

    pygame.display.set_caption("MicroComputerReserch!")

    clock = pygame.time.Clock()

    key_pressed_time = {}

    scenes = {
        "main": main_scene.MainScene(screen, saves),
        "name": name_scene.NameScene(screen),
        "title": title_scene.TitleScene(screen, saves),
        "darkening": darkening_scene.DarkeningScene(screen),
    }

    current_scene = scenes["title"]

    frame = 0

    while True:
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:  # 閉じるボタンが押されたら
                pygame.quit()  # 全てのpygameモジュールの初期化を解除
                sys.exit()  # 終了（ないとエラーで終了することになる）
            elif event.type == KEYDOWN:
                keyboard["pressed"].append(event.key)
                keyboard["pushed"].append(event.key)

                if event.key not in key_pressed_time:
                    key_pressed_time[event.key] = time.time()

            elif event.type == KEYUP:
                keyboard["pressed"].remove(event.key)

                if event.key in key_pressed_time:
                    del key_pressed_time[event.key]

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    current_time = time.time()
                    if current_time - mouse["last_click_time"] <= 0.3:
                        mouse["double_clicked"] = True

                    mouse["last_click_time"] = time.time()

                    mouse["clicked"] = True
                elif event.button == 3:
                    mouse["right_clicked"] = True
                elif event.button == 4:
                    mouse["up"] = True
                elif event.button == 5:
                    mouse["down"] = True

                mouse["position"] = event.pos

        keyboard["long_pressed"].clear()

        for key in list(key_pressed_time):
            is_long_pressed = False

            current_time = time.time()
            if key in key_pressed_time:
                pressed_duration = current_time - key_pressed_time[key]
                if pressed_duration >= 0.5 and frame % 3 == 0:
                    is_long_pressed = True

            if is_long_pressed:
                keyboard["long_pressed"].append(key)

        keyboard["long_pressed"] += keyboard["pushed"]

        result = current_scene.mainloop()

        if current_scene.is_end:
            current_scene.is_end = False

            if current_scene.scene_name == "title":
                scenes["main"].save_data_num = result

                if result is None:
                    scenes["darkening"].next_scene = "name"
                    current_scene = scenes["darkening"]
                else:
                    scenes["darkening"].next_scene = "main"
                    current_scene = scenes["darkening"]

            elif current_scene.scene_name == "name":
                scenes["darkening"].next_scene = "main"
                current_scene = scenes["darkening"]
                scenes["main"].name = result

            elif current_scene.scene_name == "main":
                scenes["darkening"].next_scene = "title"
                current_scene = scenes["darkening"]

            elif current_scene.scene_name == "darkening":
                current_scene = scenes[current_scene.next_scene]

            current_scene.start()

        keyboard["pushed"].clear()
        mouse["clicked"] = False
        mouse["double_clicked"] = False
        mouse["right_clicked"] = False
        mouse["up"] = False
        mouse["down"] = False
        clock.tick(60)
        frame += 1


if __name__ == "__main__":
    main()
