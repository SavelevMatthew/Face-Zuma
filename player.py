from ball import Ball
from graphics import Colors
import math
import random
class Player:
    def __init__(self, ball_types_amout, radius, pos, bullet_speed):
        self.pos = pos
        self.types = ball_types_amout
        self.b_speed = bullet_speed
        self.distance = radius
        self.bullets = []
        self.first = Ball(random.randint(0, self.types - 1), radius, pos)
        self.second = Ball(random.randint(0, self.types - 1),
                           int(2 * radius / 3),
                           (pos[0], pos[1] + radius))
        self.angle = math.pi / 2

    def swap(self):
        type = self.first.type
        self.first.type = self.second.type
        self.second.type = type

    def set_rotation(self, angle):
        self.angle = angle % (math.pi * 2)
        self.second.pos = (int(self.first.pos[0] +
                               self.distance * math.cos(angle + math.pi)),
                           int(self.first.pos[1] -
                               self.distance * math.sin(angle + math.pi)))

    def rotate(self, delta_angle):
        self.angle += delta_angle * math.pi / 180
        self.set_rotation(self.angle)

    def shoot(self):
        self.bullets.append((Ball(self.first.type, self.first.r,
                                  self.first.pos), self.angle))
        self.first.type = self.second.type
        self.second.type = random.randint(0, self.types - 1)
