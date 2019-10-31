from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QBasicTimer, Qt
from graphics import Textures
from drawing import Drawer
import sys


class Application(QMainWindow):
    def __init__(self, caption, w, h, tex, levels, cur_lvl=1):
        super().__init__()
        self.caption = caption
        self.size = (w, h)
        self.setFixedSize(w, h)
        self.pressed_keys = {'K_RIGHT': False, 'K_LEFT': False,
                             'K_A': False, 'K_D': False}
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
        if(self.level.finished):
            self.timer.stop()
            return
        self.keyHoldEvent()
        self.setWindowTitle(self.caption + ' : ' +
                            self.levels[self.cur_lvl - 1].caption)
        self.level.update(self.frame_delta / 1000)
        self.drawer.draw_frame(self.level)
        self.level.clear_trash()

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
        elif key == Qt.Key_Escape:
            sys.exit()
        elif key == Qt.Key_Space or key == Qt.Key_Up:
            self.level.p.shoot()
        elif key == Qt.Key_X or key == Qt.Key_Down:
            self.level.p.swap()

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

    def keyHoldEvent(self):
        if self.pressed_keys['K_RIGHT'] or self.pressed_keys['K_D']:
            self.level.p.rotate(-self.level.rot)
        elif self.pressed_keys['K_LEFT'] or self.pressed_keys['K_A']:
            self.level.p.rotate(self.level.rot)


class Level_Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.size[1])
