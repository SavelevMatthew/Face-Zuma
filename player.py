from ball import Ball
from graphics import Colors
import math
import random


class Player:
    def __init__(self, ball_types_amout, mode, radius, pos, bullet_speed):
        self.pos = pos
        self.modes = ball_types_amout
        self.mode = mode
        self.types = self.modes[mode]
        self.b_speed = bullet_speed
        self.distance = radius
        self.bullets = []
        self.refill_balls()
        self.angle = math.pi / 2

    def refill_balls(self):
        self.types = self.modes[self.mode]
        self.first = Ball(random.randint(0, self.types - 1), self.distance,
                          self.pos)
        self.second = Ball(random.randint(0, self.types - 1),
                           int(2 * self.distance / 3),
                           (self.pos[0], self.pos[1] + self.distance))

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
