from PyQt5.QtWidgets import QApplication
from graphics import Textures
import sys
import os
import applogic
import engine
import parser

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    offset = 50
    w, h = 800, 600
    lw, lh = w, h - offset
    app = QApplication(sys.argv)
    tex = Textures()
    levels = parser.parse_levels(lw, lh, len(tex.balls))
    window = applogic.Application('Zuma', w, h, offset, tex, levels, 2)
    window.start()
    sys.exit(app.exec_())
