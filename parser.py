import json
import os
from engine import Level


def read_level(filename, w, h, types):
    with open(filename, 'r') as f:
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
                     player_pos, 3, bull_speed, tex_prefix, highscores)


def parse_levels(w, h, types):
    levels = []
    for file in sorted(os.listdir('levels')):
        if 'level' in file and file.endswith('.json'):
            name = os.path.join('levels', file)
            levels.append(read_level(name, w, h, types))
    return levels


def save_levels(levels):
    high_score_dict = {}
    for level in levels:
        high_score_dict[level.caption] = level.highscores
    captions = high_score_dict.keys()
    for file in os.listdir('levels'):
        if 'level' in file and file.endswith('.json'):
            name = os.path.join('levels', file)
            with open(name, 'r+') as f:
                data = json.load(f)
                caption = data.get('Name')
                if caption in captions:
                    data['Highscores'] = high_score_dict[caption]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
