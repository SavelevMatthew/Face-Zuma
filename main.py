from PyQt5.QtWidgets import QApplication
from graphics import Textures
import sys
import os
import applogic
import engine

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    w, h = 800, 600
    checkpoints = [(-40, 40), (40, 40), (w - 40, 40),
                   (w - 40, h - 40), (40, h - 40), (40, 120), (w - 120, 120),
                   (w - 120, h - 120), (120, h - 120)]
    app = QApplication(sys.argv)
    tex = Textures()
    levels = [engine.Level('Level 1', w, h, len(tex.balls), checkpoints,
                           30, 25, 100, 5, 250)]
    window = applogic.Application('Zuma', w, h, tex, levels)
    window.start()
    sys.exit(app.exec_())
