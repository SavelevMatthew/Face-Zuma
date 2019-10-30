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

    def update_ball(self, ball):
        if ball.status == 0:
            label = QLabel(self.parent)
            label.setStyleSheet('background-color: rgba(0,0,0,0%)')
            label.setPixmap(self.tex[ball.type])
            label.show()
            self.labels[ball] = label
            self.draw_ball(ball)
            ball.status = 1
        elif ball.status == 1:
            self.draw_ball(ball)
        elif ball.status == 3:
            self.labels[ball].hide()
            self.labels[ball].deleteLater()
            ball.status == 4
            self.labels.remove(ball)

    def draw_ball(self, ball):
        self.labels[ball].move(ball.pos[0] - ball.r, ball.pos[1] - ball.r)
