from PyQt5.QtWidgets import QApplication
from graphics import Textures
import sys
import os
import applogic
import engine

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    offset = 50
    w, h = 800, 600
    lw, lh = w, h - offset
    checkpoints = [(-40, 40), (40, 40), (lw - 40, 40),
                   (lw - 40, lh - 40), (40, lh - 40), (40, 120),
                   (lw - 120, 120),
                   (lw - 120, lh - 120), (120, lh - 120), (120, 200)]
    app = QApplication(sys.argv)
    tex = Textures()
    levels = [engine.Level('Level 1', lw, lh, len(tex.balls), checkpoints,
                           1, 25, 50, 3, 350, 'lvl1')]
    window = applogic.Application('Zuma', w, h, offset, tex, levels)
    window.start()
    sys.exit(app.exec_())
