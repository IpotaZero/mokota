import pygame

import main
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
        scale, offset = self.scale()
        screen = pygame.display.get_surface()
        scaled_buffer = pygame.transform.scale(buffer, scale)
        screen.blit(scaled_buffer, offset)

    def scale(self): 
        """ 画面サイズに合わせて移動、拡大する量を決める

        Parameters
        ----------
        x : _type_
            _description_
        y : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        win = pygame.display.get_window_size()
        scale = min(win[0] / main.ScreenSize[0], win[1] / main.ScreenSize[1])
        scaled_size = (main.ScreenSize[0] * scale, main.ScreenSize[1] * scale)
        scaled_pos = ((win[0] - scaled_size[0]) / 2, (win[1] - scaled_size[1]) / 2)

        return scaled_size, scaled_pos