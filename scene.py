from ctypes import util
import pygame

import utill
class Scene:
    def __init__(self) -> None:
        self.layers = []

    def addlayer(self, *layer: pygame.Surface):
        for l in layer:
            self.layers.append(l)

    def bilt(self):
        for l in self.layers:
            self.scaled_blit(l)
        pygame.display.update()  # 画面更新

    def scaled_blit(self, buffer):
        scale, offset = utill.scale()
        screen = pygame.display.get_surface()
        scaled_buffer = pygame.transform.scale(buffer, scale)
        screen.blit(scaled_buffer, offset)
