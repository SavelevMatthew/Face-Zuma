import math
import random
from ball import Ball
from player import Player


class Level:
    def __init__(self, caption, width, height, types, checkpoints,
                 ball_amount, ball_radius, ball_speed, player_pos,
                 player_rotaion, player_bullet_speed, tex_name_prefix):
        self.types = types
        self.modes = list(types.keys())
        self.mode = self.modes[1]
        self.ball_amount = self.types[self.mode]
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
        self.p = Player(types, self.mode, ball_radius,
                        player_pos, player_bullet_speed)
        self.rot = player_rotaion
        self.come_back = []
        self.score = 0
        self.won = False
        self.tex_name = tex_name_prefix

    def switch_modes(self):
        index = self.modes.index(self.mode)
        self.mode = self.modes[(index + 1) % len(self.modes)]
        self.ball_amount = self.types[self.mode]
        return self.mode

    def check_sequence(self, start_index):
        st = start_index
        fin = start_index
        type = self.balls[start_index].type
        i = start_index - 1
        while i >= 0:
            if self.balls[i].type == type:
                st -= 1
            else:
                break
            i -= 1
        i = start_index + 1
        while i < len(self.balls):
            if self.balls[i].type == type:
                fin += 1
            else:
                break
            i += 1
        return (st, fin)

    def clear_trash(self):
        for ball in self.balls:
            if ball.status == 4:
                self.balls.remove(ball)
        for bull in self.p.bullets:
            if bull[0].status == 4:
                self.p.bullets.remove(bull)

    def update(self, time_delta):
        if len(self.come_back) == 0:
            self.move_balls_head_by_time(len(self.balls), time_delta)
        else:
            amount = self.come_back[0]
            self.move_balls_head_by_time(amount, time_delta * 3, True)
            d = get_distance(self.balls[amount - 1].pos,
                             self.balls[amount].pos)
            if d < self.r * 2:
                self.move_balls_head_by_distance(amount, self.r * 2 - d)
                self.come_back.clear()
                s1 = self.check_sequence(amount - 1)
                s2 = self.check_sequence(amount)
                if s1 == s2 and s1[1] - s1[0] >= 2:
                    self.delete_ball_sequence(s1[0], s1[1])
        if self.amount > 0 and (len(self.balls) == 0 or
                                get_distance(self.cp[0],
                                             self.balls[len(self.balls) - 1]
                                                 .pos) >=
                                self.r * 2):
            b = Ball(random.randint(0, self.ball_amount - 1),
                     self.r, self.cp[0])
            self.balls.append(b)
            self.amount -= 1
        if len(self.come_back) == 0:
            counter = 0
            for bul_pair in self.p.bullets:
                dx = self.p.b_speed * time_delta
                bul_pair[0].move(dx * math.cos(bul_pair[1]),
                                 -dx * math.sin(bul_pair[1]))
                if not is_in_border(bul_pair[0].pos, (-self.r, -self.r),
                                    (self.w + self.r, self.h + self.r)):
                    bul_pair[0].status = 3
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
        if len(self.balls) == 0 and self.amount == 0:
            self.won = True
            self.finished = True

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
        s = self.check_sequence(index)
        if s[1] - s[0] >= 2:
            self.delete_ball_sequence(s[0], s[1])

    def delete_ball_sequence(self, start, end):
        amount = end - start + 1
        self.score += amount * (50 + 10 * (amount - 3))
        for i in range(amount):
            self.balls[start + i].status = 3
        if len(self.balls) - 1 != end and start != 0:
            self.come_back.append(start)

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
