import unittest
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
        player = Player({'1': 10}, '1', 50, (0, 0), 100)
        first = player.first.type
        second = player.second.type
        player.swap()
        self.assertEqual(player.first.type, second)
        self.assertEqual(player.second.type, first)

    def test_refill(self):
        player = Player({'1': 10}, '1', 50, (0, 0), 100)
        first = player.first
        second = player.second
        player.refill_balls()
        self.assertNotEqual(first, player.first)
        self.assertNotEqual(second, player.second)

    def test_set_rotation(self):
        player = Player({'1': 10}, '1', 75, (0, 0), 100)
        pos = (player.second.pos[0], player.second.pos[1])
        player.set_rotation(pi)
        self.assertEqual(pi, player.angle)
        self.assertEqual(player.second.pos, (pos[1], pos[0]))

    def test_rotation(self):
        player = Player({'1': 10}, '1', 75, (0, 0), 100)
        player2 = Player({'1': 10}, '1', 75, (0, 0), 100)
        angle = player.angle + pi / 2
        player.rotate(90)
        player2.set_rotation(angle)
        self.assertEqual(angle, player.angle)
        self.assertEqual(player.second.pos, player2.second.pos)
        self.assertEqual(player.angle, player2.angle)

    def test_shoot(self):
        player = Player({'1': 10}, '1', 75, (0, 0), 100)
        second = player.second.type
        bullets = len(player.bullets)
        player.shoot()
        self.assertEqual(player.first.type, second)
        self.assertEqual(len(player.bullets), bullets + 1)


class TestEngine(unittest.TestCase):
    def test_init(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (100, 100)], 3, 50,
                    10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.update(16 / 1000)
        self.assertEqual(len(lvl.balls), 1)

    def test_update_highscores(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                    10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.score = 2000
        lvl.update_highscores()
        self.assertEqual(lvl.highscores, [2000, 0, 0, 0, 0])
        lvl.score = 3000
        lvl.update_highscores()
        self.assertEqual(lvl.highscores, [3000, 2000, 0, 0, 0])
        lvl.score = 2
        lvl.update_highscores()
        self.assertEqual(lvl.highscores, [3000, 2000, 2, 0, 0])

    def test_check_sequence(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                    10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        ball = Ball(0, 50, (0, 0))
        lvl.balls.append(ball)
        lvl.balls.append(ball)
        lvl.balls.append(ball)
        ball2 = Ball(1, 50, (0, 0))
        self.assertEqual(lvl.check_sequence(2), (0, 2))
        lvl.balls.insert(2, ball2)
        self.assertEqual(lvl.check_sequence(2), (2, 2))

    def test_check_bonuses(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                    10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        ball = Ball(-1, 50, (0, 0))
        ball2 = Ball(0, 50, (0, 0))
        lvl.balls.append(ball)
        lvl.balls.append(ball2)
        self.assertEqual(lvl.check_bonuses(1), [0])
        lvl.balls.append(ball)
        self.assertEqual(lvl.check_bonuses(1), [0, 2])

    def test_clear_trash(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10, '2': 1}, [(0, 0)], 3, 50,
                    10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        ball = Ball(-1, 50, (0, 0))
        ball2 = Ball(-1, 50, (0, 0), 4)
        lvl.balls.append(ball)
        lvl.balls.append(ball2)
        ball3 = Ball(-1, 50, (0, 0), 4)
        lvl.p.bullets.append((ball3, 0))
        lvl.clear_trash()
        self.assertEqual(len(lvl.balls), 1)
        self.assertEqual(len(lvl.p.bullets), 0)

    def test_functions(self):
        ball1 = (1, 1)
        ball2 = (-1, -1)
        self.assertEqual(is_in_border((0, 0), ball1, ball2), True)
        self.assertEqual(is_in_border((-2, -2), ball1, ball2), False)

        corner = (1, -1)
        self.assertEqual(get_angle2(ball1, corner, ball2), pi / 2)

        self.assertEqual(get_angle(ball2, ball1), pi / 4)

        self.assertEqual(get_distance(ball1, corner), 2)

    def test_distance(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)],
                    3, 50, 10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        self.assertEqual(lvl.get_distance_between_checkpoint(0, 2), 20)

        ball = Ball(0, 10, (0, 5))
        ball2 = Ball(0, 10, (5, 10))
        ball2.goal = 2
        self.assertEqual(lvl.get_ball_distance(ball, ball2), 10)
        ball2.pos = (5, 5)
        ball2.goal = 1
        self.assertEqual(lvl.get_ball_distance(ball, ball2), 5)

    def test_update_debuffs(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)],
                    3, 50, 10, (50, 50), 0, 15, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.debuffs['slow'] = 5000
        lvl.update_debuffs(1)
        self.assertEqual(lvl.debuffs['slow'], 4000)
        lvl.update_debuffs(4)
        self.assertEqual(len(lvl.debuffs), 0)

    def test_update(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)],
                    2, 5, 2, (50, 50), 0, 2, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.balls.append(Ball(0, 5, (0, 5)))
        dt = 2 / lvl.v
        lvl.update(dt)
        self.assertEqual(lvl.balls[0].pos[1], 7)
        lvl.debuffs['slow'] = 99999
        lvl.update(dt)
        self.assertEqual(lvl.balls[0].pos[1], 8)
        lvl.balls.clear()

        lvl.balls.append(Ball(0, 2, (0, 3)))
        lvl.balls.append(Ball(0, 2, (0, 8)))
        lvl.balls.append(Ball(0, 2, (0, 9)))
        lvl.come_back.append(2)
        lvl.update(dt)
        self.assertEqual(len(lvl.come_back), 0)
        self.assertEqual(lvl.balls[0].status, 3)

        lvl.balls.clear()
        lvl.amount = 0
        lvl.update(dt)
        self.assertTrue(lvl.finished)
        self.assertTrue(lvl.won)

    def test_update_inserts(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)],
                    2, 5, 2, (50, 50), 0, 1, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.balls.append(Ball(0, 2, (0, 3)))
        lvl.p.bullets.append((Ball(0, 2, (0, 5)), 0))
        lvl.update(2)
        self.assertEqual(len(lvl.balls), 2)

    def test_ball_moving(self):
        lvl = Level('Lvl1', 100, 100, {'1': 10}, [(0, 0), (0, 10), (10, 10)],
                    3, 5, 2, (50, 50), 0, 2, 'lvl1', [0, 0, 0, 0, 0],
                    ['slow', 'bomb'])
        lvl.balls.append(Ball(0, 5, (0, 5)))
        lvl.move_ball_by_distance(lvl.balls[0], 10)
        self.assertEqual(lvl.balls[0].pos, (5, 10))
        lvl.move_ball_by_distance(lvl.balls[0], 5, True)
        self.assertEqual(lvl.balls[0].pos, (0, 10))
        lvl.move_ball_by_distance(lvl.balls[0], 100)
        self.assertEqual(lvl.balls[0].pos, (10, 10))
        lvl.move_ball_by_distance(lvl.balls[0], 100, True)
        self.assertEqual(lvl.balls[0].pos, (0, 0))


if __name__ == '__main__':
    unittest.main()
