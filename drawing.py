from PyQt5.QtWidgets import QLabel
import engine


class Drawer():
    def __init__(self, parent_widget, textures):
        self.parent = parent_widget
        self.tex = textures
        self.labels = {}

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
            label.setPixmap(self.tex[ball.type])
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
        self.labels[ball].setPixmap(self.tex[ball.type].scaled(ball.r * 2,
                                                               ball.r * 2))
        self.labels[ball].move(ball.pos[0] - ball.r, ball.pos[1] - ball.r)
