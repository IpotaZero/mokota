from ctypes import util
import pygame

import utill
class Scene:
    def __init__(self, *layer) -> None:
        self.layers = []
        if(layer is not None):
            for l in layer:
                self.layers.append(l)

    def addlayer(self, *layer: pygame.Surface):
        for l in layer:
            self.layers.append(l)

    def blit(self):
        for l in self.layers:
            self.scaled_blit(l)
        pygame.display.update()  # 画面更新

    def scaled_blit(self, buffer):
        scale_screen, offset, scale = utill.scale()
        screen = pygame.display.get_surface()
        print(scale_screen)
        scaled_buffer = pygame.transform.scale(buffer, scale_screen)
        screen.blit(scaled_buffer, offset)
