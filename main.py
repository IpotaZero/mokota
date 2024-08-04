import json
import os
import pygame
from pygame.locals import *
import sys
import time

from scene_main import SceneMain
from scene_title import SceneTitle
from scene_name import SceneName
from scene_darkening import SceneDarkening
from scene_edit import SceneEdit

from save import Save

from Ifunctions import *


def make_save_data():
    saves: list[Save] = []

    if not os.path.isfile("save.dat"):
        with open("save.dat", "w") as f:
            f.write(json.dumps(saves))
        return saves

    with open("save.dat") as f:
        try:
            for save in json.loads(f.read()):
                saves.append(Save(save))
        except json.JSONDecodeError:
            print("データが破損しているのです!")

    return saves


def make_config_data():
    config = {
        "window_size": screen_option["default_size"],
        "volume_bgm": 0,
        "volume_se": 0,
        "text_speed": 3,
        "passed_branches": {},
        "debug_skip": True,
    }

    if not os.path.isfile("config.dat"):
        with open("config.dat", "w") as f:
            f.write(json.dumps(config))
        return config

    with open("config.dat") as f:
        try:
            for key, value in json.loads(f.read()).items():
                config[key] = value
        except json.JSONDecodeError:
            print("データが破損しているのです!")

    return config


def main():
    saves = make_save_data()
    config = make_config_data()

    pygame.init()  # Pygameの初期化

    if config["window_size"] == [0, 0]:
        pygame.display.set_mode(screen_option["default_size"])
    else:
        pygame.display.set_mode(config["window_size"])

    screen_option["real_size"] = pygame.display.get_desktop_sizes()[0]

    set_window_size(config["window_size"])

    pygame.display.set_caption("MicroComputerReserch!")

    clock = pygame.time.Clock()

    key_pressed_time = {}

    scenes = {
        "main": SceneMain(saves, config),
        "name": SceneName(),
        "title": SceneTitle(saves, config),
        "darkening": SceneDarkening(),
        "edit": SceneEdit(),
    }

    current_scene = scenes["title"]

    frame = 0

    while True:
        # print(screen_ratio)
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:  # 閉じるボタンが押されたら
                pygame.quit()  # 全てのpygameモジュールの初期化を解除
                sys.exit()  # 終了（ないとエラーで終了することになる）
            elif event.type == KEYDOWN:
                keyboard["pressed"].add(event.key)
                keyboard["pushed"].add(event.key)

                if event.key not in key_pressed_time:
                    key_pressed_time[event.key] = time.time()

            elif event.type == KEYUP:
                keyboard["pressed"].remove(event.key)

                if event.key in key_pressed_time:
                    del key_pressed_time[event.key]

            elif event.type == MOUSEBUTTONDOWN:
                # print(event.button)
                if event.button == 1:
                    current_time = time.time()
                    if current_time - mouse["last_click_time"] <= 0.3:
                        mouse["double_clicked"] = True

                    mouse["last_click_time"] = time.time()

                    mouse["clicked"] = True
                    mouse["long_clicked"] = True
                elif event.button == 3:
                    mouse["right_clicked"] = True
                elif event.button == 4:
                    mouse["up"] = True
                elif event.button == 5:
                    mouse["down"] = True

                mouse["position"] = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse["long_clicked"] = False

        keyboard["long_pressed"].clear()

        for key in list(key_pressed_time):
            is_long_pressed = False

            current_time = time.time()
            if key in key_pressed_time:
                pressed_duration = current_time - key_pressed_time[key]
                if pressed_duration >= 0.5 and frame % 3 == 0:
                    is_long_pressed = True

            if is_long_pressed:
                keyboard["long_pressed"].add(key)

        keyboard["long_pressed"] |= keyboard["pushed"]

        result = current_scene.mainloop()

        if current_scene.is_end:
            current_scene.is_end = False

            if current_scene.scene_name == "title":
                if result == "edit":
                    current_scene = scenes["edit"]

                else:
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

            elif current_scene.scene_name == "edit":
                current_scene = scenes["title"]

            current_scene.start()

        keyboard["pushed"].clear()
        mouse["clicked"] = False
        mouse["double_clicked"] = False
        mouse["right_clicked"] = False
        mouse["up"] = False
        mouse["down"] = False
        clock.tick(5)
        frame += 1


if __name__ == "__main__":
    main()
