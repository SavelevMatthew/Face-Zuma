from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QBasicTimer, Qt
from drawing import Drawer
import sys
import engine
import math
from copy import deepcopy
from parser import save_levels


class Application(QMainWindow):
    def __init__(self, caption, w, h, offset, tex, levels):
        '''
        Initialize Game Application
        '''
        super().__init__()
        self.caption = caption
        self.size = (w, h)
        self.setFixedSize(w, h)
        self.pressed_keys = {'K_RIGHT': False, 'K_LEFT': False,
                             'K_A': False, 'K_D': False}
        self.levels = levels
        self.level = levels[0]
        self.timer = QBasicTimer()
        self.frame_delta = 16
        self.offset = offset
        self.level_window = Level_Window(self)
        self.header = Header_Window(self)
        self.tex = tex
        self.drawer = Drawer(self.level_window, self.header, tex.balls,
                             tex.others, self.level.mode)

        self.help = Help_Window(w / 1.5, h / 2)
        self.level_select = Level_Select_Window(self)
        self.main_menu = Menu_Window(self, self.level.mode)

        self.show()
        self.main_menu.show()
        self.update_title()

    def save_levels(self):
        '''
        Saves current highscores in files
        '''
        save_levels(self.levels)

    def switch_modes(self):
        '''
        Changes mode to next one
        '''
        for i in range(len(self.levels)):
            mode = self.levels[i].switch_modes()
            self.levels[i].p.mode = mode
            self.levels[i].p.refill_balls()
        self.drawer.mode = mode

    def got_to_main(self):
        '''
        Closes level-select menu and opening Main one
        '''
        self.level_select.hide()
        self.main_menu.show()

    def start(self, level_id):
        '''
        Prepare level environment and then start the GAME

        level_id used to choose, which level we want to run
        '''
        self.level = self.levels[level_id]
        self.tex.scale_balls(self.level.r)
        self.show()
        self.drawer.init_level(self.size[0], self.size[1],
                               self.offset, self.level.tex_name)
        self.level_window.show()
        self.header.show()
        self.level.p.refill_balls()
        self.timer.start(16, self)

    def finish_game(self):
        '''
        Stops the game and clean all visual trash, which is left from previous
        game.
        '''
        self.timer.stop()
        self.level.amount = self.level.ball_count
        self.level_window.deleteLater()
        self.level_window = Level_Window(self)
        self.drawer.labels.clear()
        self.drawer.parent = self.level_window
        self.drawer.bg = None
        self.level.balls.clear()
        self.level.p.bullets.clear()

    def timerEvent(self, event):
        '''
        Running every frame and update game and drawing condition
        '''
        if(self.level.finished):
            self.update_title()
            self.timer.stop()
            self.level.finished = False
            return
        self.keyHoldEvent()
        self.level.update(self.frame_delta / 1000)
        self.drawer.update_header(self.level.caption, self.level.score)
        self.update_title()
        self.drawer.draw_frame(self.level)
        self.level.clear_trash()

    def update_title(self):
        '''
        Updates game title
        '''
        win_cond = ''
        if self.level.finished:
            if self.level.won:
                win_cond = ' YOU WON! '
            else:
                win_cond = ' YOU LOST! GAME IS OVER... '
        title = '{0} {1}'.format(self.caption, win_cond)
        self.setWindowTitle(title)

    def mousePressEvent(self, event):
        '''
        Handles mouse press events
        '''
        if event.button() == Qt.LeftButton:
            pos = (event.x(), event.y() - self.offset)
            angle = engine.get_angle(self.level.p.pos, pos)
            self.level.p.set_rotation(math.pi * 2 - angle)
            self.level.p.shoot()

    def closeEvent(self, event):
        '''
        Handles app closing event
        '''
        self.save_levels()
        self.help.hide()
        print('Зочем закрыл? Открой абратна,' +
              'а то Стасян уже выехал за тобой!))0)')

    def keyPressEvent(self, event):
        '''
        Handles key pressing events
        '''
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
            if not self.level_window.isHidden():
                self.finish_game()
                self.level_window.hide()
                self.main_menu.show()
            elif not self.level_select.isHidden():
                self.level_select.hide()
                self.main_menu.show()
            elif not self.main_menu.isHidden():
                self.save_levels()
                self.help.hide()
                sys.exit()
        elif key == Qt.Key_Space or key == Qt.Key_Up:
            self.level.p.shoot()
        elif key == Qt.Key_X or key == Qt.Key_Down:
            self.level.p.swap()

    def keyReleaseEvent(self, event):
        '''
        Handles key releasing events
        '''
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
        '''
        Handles holding keys events
        '''
        if self.pressed_keys['K_RIGHT'] or self.pressed_keys['K_D']:
            self.level.p.rotate(-self.level.rot)
        elif self.pressed_keys['K_LEFT'] or self.pressed_keys['K_A']:
            self.level.p.rotate(self.level.rot)


class Level_Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.size[1] - app.offset)
        self.move(0, app.offset)


class Header_Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.offset)


class Menu_Window(QWidget):
    def __init__(self, app, mode):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.size[1])
        self.bg = QLabel(self)
        self.bg.setPixmap(app.tex.others['menu_bg'].scaled(app.size[0],
                                                           app.size[1]))
        self.bg.show()

        bg_clr = 'rgba(229,190,149,40%)'
        border_clr = 'rgba(88,65,49,100%)'
        style = 'background-color: {0}; border: {2}px solid {1}; \
                 font-weight: bold; font-family: Phosphate, sans-serif; \
                 color: {1}; font-size: {3}px'.format(bg_clr, border_clr,
                                                      int(app.size[0] / 100),
                                                      int(app.size[0] * 0.094))
        self.play = QPushButton("Play", self)
        self.play.setFixedSize(app.size[0] / 2, app.size[1] / 5)
        self.play.move(app.size[0] / 4, app.size[1] * 0.265)
        self.play.setStyleSheet(style)
        self.play.clicked.connect(self.hide)
        self.play.clicked.connect(app.level_select.show)
        self.play.show()
        style = 'background-color: {0}; border: {2}px solid {1}; \
                 font-weight: bold; font-family: Phosphate, sans-serif; \
                 color: {1}; font-size: {3}px'.format(bg_clr, border_clr,
                                                      int(app.size[0] / 100),
                                                      int(app.size[0] * 0.05))

        self.mode = QPushButton("Mode: " + mode, self)
        self.mode.setFixedSize(app.size[0] / 2, app.size[1] / 5)
        self.mode.move(app.size[0] / 4, app.size[1] * 0.49)
        self.mode.clicked.connect(app.switch_modes)
        self.mode.clicked.connect(lambda: self.switch_mode(app.drawer.mode))
        self.mode.setStyleSheet(style)
        self.mode.show()

        self.exit = QPushButton("Quit", self)
        self.exit.setFixedSize(app.size[0] / 4, app.size[1] / 6)
        self.exit.move(app.size[0] * 0.375, app.size[1] * 0.715)
        self.exit.setStyleSheet(style)
        self.exit.clicked.connect(app.save_levels)
        self.exit.clicked.connect(sys.exit)
        self.exit.show()

        self.help = QPushButton("?", self)
        self.help.setFixedSize(app.size[0] * 0.1, app.size[1] / 6)
        self.help.move(app.size[0] * 0.65, app.size[1] * 0.715)
        self.help.setStyleSheet(style)
        self.help.clicked.connect(app.help.show)
        self.help.show()

    def switch_mode(self, name):
        '''
        Updates button text

        name used to pass mode caption
        '''
        self.mode.setText('Mode: ' + name)


class Level_Select_Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setParent(app)
        self.setFixedSize(app.size[0], app.size[1])
        self.bg = QLabel(self)
        self.bg.setPixmap(app.tex.others['level_menu'].scaled(app.size[0],
                                                              app.size[1]))
        self.bg.show()

        self.caption = QLabel(self)
        self.caption.setFixedSize(app.size[0], app.size[1] / 6)
        self.caption.setAlignment(Qt.AlignCenter)
        clr = 'rgba(88,65,49,100%)'
        style = 'font-size: {0}px; background-color: {1}; font-weight: {2}; \
                 color: {3}; font-family: {4}'.format(int(app.size[1] / 8),
                                                      'rgba(0,0,0,0%)',
                                                      'bold', clr,
                                                      'Phosphate, sans-serif')
        self.caption.setStyleSheet(style)
        self.caption.setText('Levels:')
        self.caption.show()

        width = app.size[0] * 0.7
        off_x = (app.size[0] - width) / 2
        off_y = app.size[1] / 6
        x_count = 5
        el_w = width / x_count
        dist = el_w / 5
        bg_clr = 'rgba(229,190,149,40%)'
        border_clr = 'rgba(88,65,49,100%)'
        style = 'background-color: {0}; border: {2}px solid {1}; \
                 font-weight: bold; font-family: Phosphate, sans-serif; \
                 color: {1}; font-size: {3}px'.format(bg_clr, border_clr,
                                                      int(dist / 2),
                                                      int(el_w / 2))

        level_buttons = []
        for i in range(len(app.levels)):
            btn = QButton(i, '{}'.format(i + 1), self)
            btn.setFixedSize(el_w - dist, el_w - dist)
            btn.setStyleSheet(style)
            pos_x = (i % x_count) * el_w + (dist / 2) + off_x
            pos_y = (i // x_count) * el_w + (dist / 2) + off_y
            btn.clicked.connect(self.hide)
            btn.clicked.connect(btn.on_click)
            btn.move(pos_x, pos_y)
            btn.show()
            level_buttons.append(btn)
        style = style.replace(border_clr, 'rgba(100,0,0,100%)')
        back_btn = QPushButton("←", self)
        back_btn.setFixedSize(el_w - dist, el_w - dist)
        back_btn.setStyleSheet(style)
        back_btn.move(dist / 2, app.size[1] - el_w + dist / 2)
        back_btn.clicked.connect(app.got_to_main)
        back_btn.show()
        self.back_btn = back_btn


class Help_Window(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.txt = 'Hello and Welcome to ZUMA! \n' + \
                   'By clicking Mode button you can' + \
                   ' switch game texture packs \n' + \
                   'Play button will move you to Level Select window \n\n' + \
                   'Move your mouse or use Arrows/A/D buttons to aim \n' + \
                   'Shoot balls with Space/↑ and swap them with X/↓ \n' + \
                   'When sequence will have 3+ of same balls in a row, \n' + \
                   'You will get 50 points for ball' + \
                   '(and 10 extra for each 4+ ball) \n' + \
                   'Don\'t let the balls hit the end of the road... \n' + \
                   'And the most important: HAVE FUN ;) \n\n' + \
                   'Author: Matthew Savelev, 2019, All rights reserved ©'
        self.text = QLabel(self)
        self.text.setAlignment = Qt.AlignCenter
        self.setFixedSize(w, h)
        self.text.setFixedSize(w, h)
        self.text.setText(self.txt)
        bg_clr = 'rgba(229,190,149,40%)'
        border_clr = 'rgba(88,65,49,100%)'
        style = 'background-color: {0}; border: {2}px solid {1}; \
                 font-weight: bold; font-family: Phosphate, sans-serif; \
                 color: {1}; font-size: {3}px'.format(bg_clr, border_clr,
                                                      int(w / 50),
                                                      int(w * 0.032))
        self.text.setStyleSheet(style)
        self.text.show


class QButton(QPushButton):
    '''
    Modified QPushButton with ID
    '''
    def __init__(self, id, text, parent):
        super().__init__(text, parent)
        self.id = id

    def on_click(self):
        '''
        Handles button clicking events
        '''
        self.parent().parent().start(self.id)
