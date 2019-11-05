import json
import os
from engine import Level


def read_level(filename, w, h, types):
    with open(filename) as f:
        data = json.load(f)
        name = data.get('Name')
        amount = data.get('Amount')
        radius = data.get('Raduis')
        ball_speed = data.get('BallSpeed')
        bull_speed = data.get('BulletSpeed')
        tex_prefix = data.get('TexturesPrefix')
        points = [(i[0], i[1]) for i in data.get('Checkpoints')]
        highscores = data.get('Highscores')
        pos = data.get('PlayerPos')
        player_pos = (pos[0], pos[1])
        while len(highscores) < 5:
            highscores.append(0)
        return Level(name, w, h, types, points, amount, radius, ball_speed,
                     player_pos, 3, bull_speed, tex_prefix)


def parse_levels(w, h, types):
    levels = []
    for file in sorted(os.listdir('levels')):
        if 'level' in file and file.endswith('.json'):
            name = os.path.join('levels', file)
            levels.append(read_level(name, w, h, types))
    return levels
