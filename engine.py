import math
import random
from ball import Ball
from player import Player
from random import randint


class Level:
    def __init__(self, caption, width, height, types, checkpoints,
                 ball_amount, ball_radius, ball_speed, player_pos,
                 player_rotaion, player_bullet_speed, tex_name_prefix,
                 highscores, bonuses):
        self.bonuses = bonuses
        self.types = types
        self.modes = list(types.keys())
        self.mode = self.modes[1]
        self.ball_amount = self.types[self.mode]
        self.caption = caption
        self.ball_count = ball_amount
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
        self.highscores = highscores
        self.music_queue = []
        # times in milliseconds
        self.debuffs = {}

    def switch_modes(self):
        '''
        Changes textures mod to next one and returns value of current mode
        '''
        index = self.modes.index(self.mode)
        self.mode = self.modes[(index + 1) % len(self.modes)]
        self.ball_amount = self.types[self.mode]
        return self.mode

    def update_highscores(self):
        '''
        Checking current highscores and record it if it's higher than Top 5
        '''
        for i in range(len(self.highscores)):
            if self.score >= self.highscores[i]:
                self.highscores.insert(i, self.score)
                self.highscores.pop()
                break

    def check_sequence(self, start_index):
        '''
        Scanning ball sequence in both directions to find subsequence of balls
        with same color as ball with start_index
        '''
        st = start_index
        fin = start_index
        type = self.balls[start_index].type
        i = start_index - 1
        while i >= 0:
            if self.balls[i].type == type or self.balls[i].status == 3:
                st -= 1
            else:
                break
            i -= 1
        i = start_index + 1
        while i < len(self.balls):
            if self.balls[i].type == type or self.balls[i].status == 3:
                fin += 1
            else:
                break
            i += 1
        return (st, fin)

    def check_bonuses(self, hit_index):
        '''
        Check ball neighbours for bonuses
        if find some, return index
        '''
        result = []
        if hit_index >= 1 and self.balls[hit_index - 1].type < 0:
            result.append(hit_index - 1)
        if hit_index < len(self.balls) - 1 and \
           self.balls[hit_index + 1].type < 0:
            result.append(hit_index + 1)
        return result

    def clear_trash(self):
        '''
        Removes unused balls (which was deleted in drawer)
        '''
        for ball in self.balls:
            if ball.status == 4:
                self.balls.remove(ball)
        for bull in self.p.bullets:
            if bull[0].status == 4:
                self.p.bullets.remove(bull)

    def update_debuffs(self, time_delta):
        '''
        Updates debuffs status
        '''
        for i in list(self.debuffs):
            v = self.debuffs[i] - time_delta * 1000
            if v <= 0:
                del self.debuffs[i]
            else:
                self.debuffs[i] = v

    def update(self, time_delta):
        self.update_debuffs(time_delta)
        '''
        Updates game condition

        time_delta is time passed from last call
        '''
        if len(self.come_back) == 0:
            if 'slow' in self.debuffs:
                self.move_balls_head_by_time(len(self.balls), time_delta / 2)
            else:
                self.move_balls_head_by_time(len(self.balls), time_delta)
        else:
            amount = self.come_back[0]
            self.move_balls_head_by_time(amount, time_delta * 3, True)
            d = self.get_ball_distance(self.balls[amount - 1],
                                       self.balls[amount])
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
            if luck_check(7) and len(self.bonuses) > 0:
                b = Ball(random.randint(-len(self.bonuses), -1),
                         self.r, self.cp[0])
            else:
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
            self.update_highscores()

    def get_ball_distance(self, ball1, ball2):
        '''
        Gets distance between ball on a road
        '''
        cp2 = ball2.goal - 1
        cp1 = ball1.goal
        if cp1 == cp2 + 1:
            return get_distance(ball1.pos, ball2.pos)
        return (self.get_distance_between_checkpoint(cp1, cp2) +
                get_distance(ball1.pos, self.cp[cp1]) +
                get_distance(ball2.pos, self.cp[cp2]))

    def get_distance_between_checkpoint(self, i1, i2):
        '''
        Gets distance between 2 checkpoints on a road
        '''
        ma = max(i1, i2)
        mi = min(i1, i2)
        dist = 0
        while mi != ma:
            dist += get_distance(self.cp[mi], self.cp[mi + 1])
            mi += 1
        return dist

    def handle_bonuses(self, bonuses):
        '''
        Handle bonuses
        '''
        pairs = [(x, self.bonuses[- self.balls[x].type - 1]) for x in bonuses]
        for p in pairs:
            if p[1] == 'slow':
                self.debuffs['slow'] = 5000
                self.music_queue.append('score_up')
                self.balls[p[0]].status = 3
                if p[0] > 0 and p[0] < len(self.balls) - 1:
                    self.move_balls_head_by_distance(p[0], self.r * 2, True)

<<<<<<< HEAD
=======

>>>>>>> 9fb8ba86f348e69cb31fcceb82605607fc810de6
    def insert_ball(self, index, ball):
        '''
        Inserts ball in sequence on index position
        '''
        self.music_queue.append('hit')
        self.balls.insert(index, ball)
        if index == len(self.balls) - 1:
            self.balls[index].pos = self.balls[index - 1].pos
            self.balls[index].goal = self.balls[index - 1].goal
            self.move_ball_by_distance(self.balls[index], self.r * 2, True)
        else:
            self.balls[index].pos = self.balls[index + 1].pos
            self.balls[index].goal = self.balls[index + 1].goal
            self.move_balls_head_by_distance(index + 1, self.r * 2)
        bonuses = self.check_bonuses(index)
        self.handle_bonuses(bonuses)
        s = self.check_sequence(index)
        if s[1] - s[0] >= 2:
            self.delete_ball_sequence(s[0], s[1])

    def delete_ball_sequence(self, start, end):
        '''
        Deletes balls from start to end positions
        '''
        self.music_queue.append('score_up')
        amount = end - start + 1
        scored = 0
        for i in range(amount):
            if self.balls[start + i].status != 3:
                scored += 1
                self.balls[start + i].status = 3
        if len(self.balls) - 1 != end and start != 0:
            self.come_back.append(start)
        self.score += scored * (50 + 10 * (scored - 3))

    def move_ball_by_distance(self, ball, dx, backward=False):
        '''
        Moves ball on a checkpoints road

        dx - distance to move
        ball - ball to move
        backward - should it go back or forward
        '''
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
                    self.update_highscores()
                    return
                dx -= dist
                dist = get_distance(ball.pos, self.cp[ball.goal])
            angle = get_angle(self.cp[ball.goal - 1], self.cp[ball.goal])
        ball.move(dx * math.cos(angle), dx * math.sin(angle))

    def move_ball_by_time(self, ball, time_delta, backward=False):
        '''
        Moves ball on a checkpoints road

        time_delta - how many time was spent from last update
        ball - ball to move
        backward - should it go back or forward
        '''
        dx = self.v * time_delta
        self.move_ball_by_distance(ball, dx, backward)

    def move_balls_head_by_time(self, amount, time_delta, backward=False):
        '''
        Moves balls sequence head on a checkpoints road

        time_delta - how many time was spent from last update
        ball - ball to move
        backward - should it go back or forward
        '''
        for i in range(amount):
            self.move_ball_by_time(self.balls[i], time_delta, backward)

    def move_balls_head_by_distance(self, amount, dx, backward=False):
        '''
        Moves balls sequence head on a checkpoints road

        dx - distance to move
        ball - ball to move
        backward - should it go back or forward
        '''
        for i in range(amount):
            self.move_ball_by_distance(self.balls[i], dx, backward)


def get_distance(p1, p2):
    '''
    Returns a distance between p1 and p2
    '''
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_angle(p1, p2):
    '''
    Returns an angle between p1-p2 line and OX axis
    '''
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_angle2(end1, corner, end2):
    '''
    Returns an angle between end1-corner and corner-end2 lines
    '''
    a = math.fabs(get_angle(end1, corner) - get_angle(end2, corner))
    if a > math.pi:
        return math.pi * 2 - a
    return math.fabs(a)


def luck_check(chance):
    '''
    With a chosen chance return True
    '''
    return randint(0, 100) < chance


def is_in_border(p, b1, b2):
    return p[0] < max([b1[0], b2[0]]) and p[0] > min([b1[0], b2[0]]) and \
           p[1] < max([b1[1], b2[1]]) and p[1] > min([b1[1], b2[1]])
