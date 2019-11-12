from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class Drawer():
    def __init__(self, level_widget, header_window, textures, others, mode):
        self.parent = level_widget
        self.header_window = header_window
        self.labels = {}
        self.tex_balls = textures
        self.tex_others = others
        self.mode = mode
        self.bg_texture = None
        self.header_texture = None
        self.bg = None
        self.header = {}

    def draw_frame(self, level):
        for ball in level.balls:
            self.update_ball(ball)
        for bull in level.p.bullets:
            self.update_ball(bull[0])
        self.update_ball(level.p.second)
        self.update_ball(level.p.first)

    def update_ball(self, ball):
        if ball.status == 0:
            label = QLabel(self.parent)
            label.setStyleSheet('background-color: rgba(0,0,0,0%)')
            label.setPixmap(self.tex_balls[self.mode][ball.type])
            label.setFixedSize(ball.r * 2, ball.r * 2)
            label.show()
            self.labels[ball] = label
            self.draw_ball(ball)
            ball.status = 1
        elif ball.status == 1:
            self.draw_ball(ball)
        elif ball.status == 3:
            self.labels[ball].hide()
            self.labels[ball].deleteLater()
            ball.status = 4

    def draw_ball(self, ball):
        self.labels[ball].setPixmap(
            self.tex_balls[self.mode][ball.type].scaled(ball.r * 2,
                                                        ball.r * 2))
        self.labels[ball].move(ball.pos[0] - ball.r, ball.pos[1] - ball.r)

    def init_level(self, w, h, offset, prefix):
        self.labels.clear()
        bg = prefix + '_bg'
        header = prefix + '_header'
        self.bg_texture = self.tex_others[bg]
        self.header_texture = self.tex_others[header]
        self.fill_bg(w, h - offset)
        self.init_header(w, offset)

    def fill_bg(self, w, h):
        if self.bg is None:
            self.bg = QLabel(self.parent)
        self.bg.setFixedSize(self.parent.size())
        self.bg.setPixmap(self.bg_texture.scaled(w, h))
        self.bg.show()

    def update_header(self, lvl_name, score):
        self.header['score'].setText('{}'.format(score))
        self.header['name'].setText(lvl_name)

    def init_header(self, w, h):
        if len(self.header) != 0:
            for label in self.header:
                self.header[label].deleteLater()
        self.header.clear()
        bg = QLabel(self.header_window)
        bg.setFixedSize(w, h)
        bg.setPixmap(self.header_texture.scaled(w, h))
        bg.show()
        self.header['bg'] = bg

        name = QLabel(self.header_window)
        style = 'font-size: {0}px; background-color: {1}; font-weight: {2}; \
                 color: {3}; font-family: {4}'.format(int(h / 2.5),
                                                      'rgba(0,0,0,65%)',
                                                      'bold', 'white',
                                                      'Impact, sans-serif')
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet(style)
        name.setFixedSize(w * 0.3, h * 3 / 4)
        name.move(w * 0.35, 0)
        name.show()
        name.setText('uknown')
        self.header['name'] = name

        score = QLabel(self.header_window)
        style = 'font-size: {0}px; background-color: {1}; font-weight: {2}; \
                 color: {3}; font-family: {4}'.format(int(h / 2.5),
                                                      'rgba(0,0,0,65%)',
                                                      'bold', 'white',
                                                      'Impact, sans-serif')
        score.setStyleSheet(style)
        score.setFixedSize(w * 0.2, h * 3 / 4)
        score.setAlignment(Qt.AlignCenter)
        score.move(w * 0.8, 0)
        score.show()
        score.setText('0')
        self.header['score'] = score
