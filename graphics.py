import random
import os
from PyQt5.QtGui import QPixmap


class Colors:
    bg_gray = (100, 100, 100)
    invisible = (-1, -1, -1)
    ball_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                   (255, 165, 0), (0, 0, 0)]

    def generate_rnd(colors):
        return colors[random.randint(0, len(colors) - 1)]


class Textures():
    def __init__(self):
        self.balls = []
        self.others = {}
        for file in os.listdir(r'images'):
            if file.endswith('.png'):
                value = os.path.join('images', file)
                if file.startswith('ball'):
                    self.balls.append(QPixmap(value))
                else:
                    self.others[file.split('.')[0]] = QPixmap(value)

    def scale(self, tex_name, w, h):
        self.others[tex_name].scaled(w, h)

    def scale_balls(self, r):
        for i in range(len(self.balls)):
            new_map = self.balls[i].scaled(2 * r, 2 * r)
            self.balls[i] = new_map
