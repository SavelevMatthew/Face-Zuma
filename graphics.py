import random
import os
from PyQt5.QtGui import QPixmap


class Colors:
    bg_gray = (100, 100, 100)
    invisible = (-1, -1, -1)
    ball_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                   (255, 165, 0), (0, 0, 0)]

    @staticmethod
    def generate_rnd(colors):
        """
        Generate random color of passed colors
        """
        return colors[random.randint(0, len(colors) - 1)]


class Textures:
    def __init__(self, modes):
        self.balls = {}
        self.others = {}
        for mode in modes:
            self.balls[mode] = []
        for file in os.listdir(r'images'):
            directory = os.path.join('images', file)
            if os.path.isdir(directory) and file in modes:
                for img in os.listdir(directory):
                    if img.endswith('.png'):
                        value = os.path.join(directory, img)
                        self.balls[file].append(QPixmap(value))
            elif file.endswith('.png'):
                value = os.path.join('images', file)
                self.others[file.split('.')[0]] = QPixmap(value)

    def scale(self, tex_name, w, h):
        """
        Return scaled to w and h texture with name of tex_name
        """
        return self.others[tex_name].scaled(w, h)

    def scale_balls(self, r):
        """
        Scales balls textures to new radius
        """
        for k, v in self.balls.items():
            new_value = []
            for i in range(len(v)):
                new_map = v[i].scaled(2 * r, 2 * r)
                new_value.append(new_map)
            self.balls[k] = new_value
