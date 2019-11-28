import unittest
from ball import Ball
from player import Player
from math import pi
from engine import *


class TestBall(unittest.TestCase):
    def test_move(self):
        b = Ball(0, 50, (0, 0))
        b.move(50, 75)
        self.assertEqual(b.pos, (50, 75))
        b.move(-100, -100)
        self.assertEqual(b.pos, (-50, -25))


class TestPlayer(unittest.TestCase):
    def test_swap(self):
        p = Player({'1': 10}, '1', 50, (0, 0), 100)
        first = p.first.type
        second = p.second.type
        p.swap()
        self.assertEqual(p.first.type, second)
        self.assertEqual(p.second.type, first)

    def test_refill(self):
        p = Player({'1': 10}, '1', 50, (0, 0), 100)
        first = p.first
        second = p.second
        p.refill_balls()
        self.assertNotEqual(first, p.first)
        self.assertNotEqual(second, p.second)

    def test_set_rotation(self):
        p = Player({'1': 10}, '1', 75, (0, 0), 100)
        pos = (p.second.pos[0], p.second.pos[1])
        p.set_rotation(pi)
        self.assertEqual(pi, p.angle)
        self.assertEqual(p.second.pos, (pos[1], pos[0]))

    def test_rotation(self):
        p = Player({'1': 10}, '1', 75, (0, 0), 100)
        p2 = Player({'1': 10}, '1', 75, (0, 0), 100)
        angle = p.angle + pi / 2
        p.rotate(90)
        p2.set_rotation(angle)
        self.assertEqual(angle, p.angle)
        self.assertEqual(p.second.pos, p2.second.pos)
        self.assertEqual(p.angle, p2.angle)

    def test_shoot(self):
        p = Player({'1': 10}, '1', 75, (0, 0), 100)
        second = p.second.type
        bullets = len(p.bullets)
        p.shoot()
        self.assertEqual(p.first.type, second)
        self.assertEqual(len(p.bullets), bullets + 1)


class TestEngine(unittest.TestCase):
    def test_init(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (100, 100)], 3, 50,
                  10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        l.update(16 / 1000)
        self.assertEqual(len(l.balls), 1)

    def test_update_highscores(self):
        l = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                  10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        l.score = 2000
        l.update_highscores()
        self.assertEqual(l.highscores, [2000, 0, 0, 0, 0])
        l.score = 3000
        l.update_highscores()
        self.assertEqual(l.highscores, [3000, 2000, 0, 0, 0])
        l.score = 2
        l.update_highscores()
        self.assertEqual(l.highscores, [3000, 2000, 2, 0, 0])

    def test_check_sequence(self):
        l = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                  10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        b = Ball(0, 50, (0, 0))
        l.balls.append(b)
        l.balls.append(b)
        l.balls.append(b)
        b2 = Ball(1, 50, (0, 0))
        self.assertEqual(l.check_sequence(2), (0, 2))
        l.balls.insert(2, b2)
        self.assertEqual(l.check_sequence(2), (2, 2))

    def test_check_bonuses(self):
        l = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                  10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        b = Ball(-1, 50, (0, 0))
        b2 = Ball(0, 50, (0, 0))
        l.balls.append(b)
        l.balls.append(b2)
        self.assertEqual(l.check_bonuses(1), [0])
        l.balls.append(b)
        self.assertEqual(l.check_bonuses(1), [0, 2])

    def test_clear_trash(self):
        l = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                  10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        b = Ball(-1, 50, (0, 0))
        b2 = Ball(-1, 50, (0, 0), 4)
        l.balls.append(b)
        l.balls.append(b2)
        b3 = Ball(-1, 50, (0, 0), 4)
        l.p.bullets.append((b3, 0))
        l.clear_trash()
        self.assertEqual(len(l.balls), 1)
        self.assertEqual(len(l.p.bullets), 0)

    def test_functions(self):
        b1 = (1, 1)
        b2 = (-1, -1)
        self.assertEqual(is_in_border((0, 0), b1, b2), True)
        self.assertEqual(is_in_border((-2, -2), b1, b2), False)

        c = (1, -1)
        self.assertEqual(get_angle2(b1, c, b2), pi / 2)

        self.assertEqual(get_angle(b2, b1), pi / 4)

        self.assertEqual(get_distance(b1, c), 2)

    def test_distance(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)], 3,
                  50, 10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        self.assertEqual(l.get_distance_between_checkpoint(0, 2), 20)

        b = Ball(0, 10, (0, 5))
        b2 = Ball(0, 10, (5, 10))
        b2.goal = 2
        self.assertEqual(l.get_ball_distance(b, b2), 10)
        b2.pos = (5, 5)
        b2.goal = 1
        self.assertEqual(l.get_ball_distance(b, b2), 5)

    def test_update_debuffs(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)], 3,
                  50, 10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        l.debuffs['slow'] = 5000
        l.update_debuffs(1)
        self.assertEqual(l.debuffs['slow'], 4000)
        l.update_debuffs(4)
        self.assertEqual(len(l.debuffs), 0)

    def test_update(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)], 2,
                  5, 2, (50, 50), 0, 2, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        l.balls.append(Ball(0, 5, (0, 5)))
        dt = 2 / l.v
        l.update(dt)
        self.assertEqual(l.balls[0].pos[1], 7)
        l.debuffs['slow'] = 99999
        l.update(dt)
        self.assertEqual(l.balls[0].pos[1], 8)
        l.balls.clear()

        l.balls.append(Ball(0, 2, (0, 3)))
        l.balls.append(Ball(0, 2, (0, 8)))
        l.balls.append(Ball(0, 2, (0, 9)))
        l.come_back.append(2)
        l.update(dt)
        self.assertEqual(len(l.come_back), 0)
        self.assertEqual(l.balls[0].status, 3)

        l.balls.clear()
        l.amount = 0
        l.update(dt)
        self.assertTrue(l.finished)
        self.assertTrue(l.won)

    def test_update_inserts(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)], 2,
                  5, 2, (50, 50), 0, 1, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        dt = 2 / l.v
        l.balls.append(Ball(0, 2, (0, 3)))
        l.p.bullets.append((Ball(0, 2, (0, 5)), 0))
        l.update(2)
        self.assertEqual(len(l.balls), 2)

    def test_ball_moving(self):
        l = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)], 3,
                  5, 2, (50, 50), 0, 2, 'lvl1', [0, 0, 0, 0, 0],
                  ['slow', 'bomb'])
        l.balls.append(Ball(0, 5, (0, 5)))
        l.move_ball_by_distance(l.balls[0], 10)
        self.assertEqual(l.balls[0].pos, (5, 10))
        l.move_ball_by_distance(l.balls[0], 5, True)
        self.assertEqual(l.balls[0].pos, (0, 10))
        l.move_ball_by_distance(l.balls[0], 100)
        self.assertEqual(l.balls[0].pos, (10, 10))
        l.move_ball_by_distance(l.balls[0], 100, True)
        self.assertEqual(l.balls[0].pos, (0, 0))


if __name__ == '__main__':
    unittest.main()
