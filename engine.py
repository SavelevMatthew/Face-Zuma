import pygame
import sys
import math
import player
import random
from graphics import Colors
from ball import Ball
from player import Player
from collections import deque



class Level:
    def __init__(self, caption, width, height, types, checkpoints,
                 ball_amount, ball_radius, ball_speed,
                 player_rotaion, player_bullet_speed):
        self.types = types
        self.caption = caption
        self.amount = ball_amount
        self.w = width
        self.h = height
        self.cx = self.w // 2
        self.cy = self.h // 2
        self.cp = checkpoints
        self.r = ball_radius
        self.v = ball_speed
        self.balls = []
        self.finished = False
        self.p = Player(types, ball_radius,
                        (self.cx, self.cy), player_bullet_speed)
        self.rot = player_rotaion

    def handle_events(self, keys):
        if self.finished:
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_x or event.key == pygame.K_DOWN:
                    self.p.swap()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.p.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    angle = get_angle(self.p.pos,
                                      (event.pos[0], self.h - event.pos[1]))
                    self.p.set_rotation(angle)
                    self.p.shoot()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.p.rotate(self.rot)
        if keys[pygame.K_RIGHT]:
            self.p.rotate(-self.rot)

    def draw_frame(self):
        self.screen.fill(self.bg)
        for ball in self.balls:
            if ball.clr != Colors.invisible:
                rounded_pos = (int(ball.pos[0]), int(ball.pos[1]))
                pygame.draw.circle(self.screen, ball.clr, rounded_pos, ball.r)

        for bul_pair in self.p.bullets:
            rounded_pos = (int(bul_pair[0].pos[0]), int(bul_pair[0].pos[1]))
            pygame.draw.circle(self.screen, bul_pair[0].clr,
                               rounded_pos, bul_pair[0].r)

        ball = self.p.second
        pygame.draw.circle(self.screen, ball.clr, ball.pos, ball.r)
        ball = self.p.first
        pygame.draw.circle(self.screen, ball.clr, ball.pos, ball.r)

        pygame.display.flip()

    def update(self, time_delta):
        for ball in self.balls:
            if ball.status == 4:
                del ball
        #if len(self.balls) == 10:
        #    self.delete_ball_sequence(3, 6)
        self.move_balls_head_by_time(len(self.balls), time_delta)
        if self.amount > 0 and (len(self.balls) == 0 or
                                get_distance(self.cp[0],
                                             self.balls[len(self.balls) - 1]
                                                 .pos) >=
                                self.r * 2):
            b = Ball(random.randint(0, self.types - 1),
                                   self.r, self.cp[0])
            self.balls.append(b)
            self.amount -= 1
        counter = 0
        for bul_pair in self.p.bullets:
            dx = self.p.b_speed * time_delta
            bul_pair[0].move(dx * math.cos(bul_pair[1]),
                             -dx * math.sin(bul_pair[1]))
            if not is_in_border(bul_pair[0].pos, (-self.r, -self.r),
                                (self.w + self.r, self.h + self.r)):
                self.p.bullets.remove(bul_pair)
            for i in range(len(self.balls)):
                if get_distance(bul_pair[0].pos, self.balls[i].pos) <= \
                   self.r * 2:
                    if len(self.balls) == 1:
                        a1 = get_angle2(bul_pair[0].pos, self.balls[0].pos,
                                        self.cp[self.balls[0].goal])
                        a2 = get_angle2(bul_pair[0].pos, self.balls[0].pos,
                                        self.cp[self.balls[0].goal - 1])
                        if a1 < a2:
                            self.insert_ball(0, bul_pair[0])
                        else:
                            self.insert_ball(1, bul_pair[0])

                    elif i == 0:
                        if get_angle2(bul_pair[0].pos, self.balls[i].pos,
                                      self.balls[i + 1].pos) < math.pi / 2:
                            self.insert_ball(1, bul_pair[0])
                        else:
                            self.insert_ball(0, bul_pair[0])
                    elif i == len(self.balls) - 1:
                        if get_angle2(bul_pair[0].pos, self.balls[i].pos,
                                      self.balls[i - 1].pos) < math.pi / 2:
                            self.insert_ball(i, bul_pair[0])
                        else:
                            self.insert_ball(i + 1, bul_pair[0])
                    else:
                        d1 = get_distance(bul_pair[0].pos,
                                          self.balls[i - 1].pos)
                        d2 = get_distance(bul_pair[0].pos,
                                          self.balls[i + 1].pos)
                        if d1 < d2:
                            self.insert_ball(i, bul_pair[0])
                        else:
                            self.insert_ball(i + 1, bul_pair[0])
                    counter -= 1
                    self.p.bullets.remove(bul_pair)
                    break
            counter += 1

    def insert_ball(self, index, ball):
        self.balls.insert(index, ball)
        if index == len(self.balls) - 1:
            self.balls[index].pos = self.balls[index - 1].pos
            self.balls[index].goal = self.balls[index - 1].goal
            self.move_ball_by_distance(self.balls[index], self.r * 2, True)
        else:
            self.balls[index].pos = self.balls[index + 1].pos
            self.balls[index].goal = self.balls[index + 1].goal
            self.move_balls_head_by_distance(index + 1, self.r * 2)

    def delete_ball_sequence(self, start, end):
        amount = end - start + 1
        for i in range(amount):
            self.balls.remove(self.balls[start])
        self.move_balls_head_by_distance(start, self.r * amount * 2, True)


    def move_ball_by_distance(self, ball, dx, backward=False):
        if (backward):
            dist = get_distance(ball.pos, self.cp[ball.goal - 1])
            while dist <= dx:
                ball.pos = self.cp[ball.goal - 1]
                ball.goal -= 1
                if ball.goal == 0:
                    ball.goal == 1
                    return
                dx -= dist
                dist = get_distance(ball.pos, self.cp[ball.goal - 1])
            angle = get_angle(self.cp[ball.goal], self.cp[ball.goal - 1])
        else:
            dist = get_distance(ball.pos, self.cp[ball.goal])
            while dist <= dx:
                ball.pos = self.cp[ball.goal]
                ball.goal += 1
                if ball.goal == len(self.cp):
                    self.finished = True
                    return
                dx -= dist
                dist = get_distance(ball.pos, self.cp[ball.goal])
            angle = get_angle(self.cp[ball.goal - 1], self.cp[ball.goal])
        ball.move(dx * math.cos(angle), dx * math.sin(angle))

    def move_ball_by_time(self, ball, time_delta, backward=False):
        dx = self.v * time_delta
        self.move_ball_by_distance(ball, dx, backward)

    def move_balls_head_by_time(self, amount, time_delta, backward=False):
        for i in range(amount):
            self.move_ball_by_time(self.balls[i], time_delta, backward)

    def move_balls_head_by_distance(self, amount, dx, backward=False):
        for i in range(amount):
            self.move_ball_by_distance(self.balls[i], dx, backward)






def get_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_angle2(end1, corner, end2):
    a = math.fabs(get_angle(end1, corner) - get_angle(end2, corner))
    if a > math.pi:
        return math.pi * 2 - a
    return math.fabs(a)


def is_in_border(p, b1, b2):
    return p[0] < max([b1[0], b2[0]]) and p[0] > min([b1[0], b2[0]]) and \
           p[1] < max([b1[1], b2[1]]) and p[1] > min([b1[1], b2[1]])
