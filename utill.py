import parameter
import pygame

def scale(): 
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
        scale = min(win[0] / parameter.ScreenSize[0], win[1] / parameter.ScreenSize[1])
        scaled_size = (parameter.ScreenSize[0] * scale, parameter.ScreenSize[1] * scale)
        scaled_pos = ((win[0] - scaled_size[0]) / 2, (win[1] - scaled_size[1]) / 2)

        return scaled_size, scaled_pos
