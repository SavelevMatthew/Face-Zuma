from PyQt5.QtWidgets import QApplication
from graphics import Textures
import sys
import os
import applogic
import parser
import sound

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    modes = [file for file in os.listdir(r'images')
             if os.path.isdir(os.path.join(os.getcwd(), 'images', file))
             and file[0].isupper()]
    bonuses = ['slow', 'bomb']
    offset = 50
    w, h = 800, 600
    lw, lh = w, h - offset
    app = QApplication(sys.argv)
    tex = Textures(modes)
    packs = parser.find_music(modes)
    music = sound.SoundPlayer(packs, modes[0])
    types = {i: len(j) for i, j in tex.balls.items()}
    levels = parser.parse_levels(lw, lh, types, bonuses)
    window = applogic.Application('Zuma', w, h, offset, tex, levels, music,
                                  bonuses, modes)
    sys.exit(app.exec_())
