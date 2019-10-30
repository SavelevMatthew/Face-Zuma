from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QBasicTimer, Qt
from graphics import Textures
from drawing import Drawer
import sys

class Application(QMainWindow):
    def __init__(self, caption, w, h, tex, levels, cur_lvl = 1):
        super().__init__()
        self.caption = caption
        self.size = (w, h)
        self.setFixedSize(w, h)
        self.pressed_keys = {'K_RIGHT': False, 'K_LEFT': False,
                             'K_SPACE': False, 'K_DOWN': False, 'K_UP': False,
                             'K_A': False, 'K_D': False, 'K_X': False}
        self.levels = levels
        self.level = levels[cur_lvl - 1]
        self.cur_lvl = cur_lvl
        self.timer = QBasicTimer()
        self.frame_delta = 16
        self.level_window = Level_Window(self)
        self.setStyleSheet('background-color:#646464;')
        self.tex = tex
        self.drawer = Drawer(self.level_window, tex.balls)

    def start(self):
        self.tex.scale_balls(self.level.r)
        self.show()
        self.level_window.show()
        self.timer.start(16, self)

    def timerEvent(self, event):
        self.setWindowTitle(self.caption + ' : ' +
                            self.levels[self.cur_lvl - 1].caption)
        self.level.update(self.frame_delta / 1000)
        self.drawer.draw_frame(self.level)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.pressed_keys['K_LEFT'] = True
        elif key == Qt.Key_A:
            self.pressed_keys['K_A'] = True
        elif key == Qt.Key_Right:
            self.pressed_keys['K_RIGHT'] = True
        elif key == Qt.Key_D:
            self.pressed_keys['K_D'] = True
        elif key == Qt.Key_Up:
            self.pressed_keys['K_UP'] = True
        elif key == Qt.Key_Space:
            self.pressed_keys['K_SPACE'] = True
        elif key == Qt.Key_Down:
            self.pressed_keys['K_DOWN'] = True
        elif key == Qt.Key_X:
            self.pressed_keys['K_X'] = True
        elif key == Qt.Key_Escape:
            sys.exit()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.pressed_keys['K_LEFT'] = False
        elif key == Qt.Key_A:
            self.pressed_keys['K_A'] = False
        elif key == Qt.Key_Right:
            self.pressed_keys['K_RIGHT'] = False
        elif key == Qt.Key_D:
            self.pressed_keys['K_D'] = False
        elif key == Qt.Key_Up:
            self.pressed_keys['K_UP'] = False
        elif key == Qt.Key_Space:
            self.pressed_keys['K_SPACE'] = False
        elif key == Qt.Key_Down:
            self.pressed_keys['K_DOWN'] = False
        elif key == Qt.Key_X:
            self.pressed_keys['K_X'] = False


class Level_Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.size[1])
