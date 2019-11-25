import json
import os
from engine import Level
from sound import SoundPack


def read_level(filename, w, h, types):
    '''
    Gets level information from file and returns new level based on it

    w, h - level size
    types - amount of each type of ball
    '''
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
    '''
    Scans levels directory for json files named with "level", gets their data,
    and returns levels list

    w, h - app size
    '''
    levels = []
    for file in sorted(os.listdir('levels')):
        if 'level' in file and file.endswith('.json'):
            name = os.path.join('levels', file)
            levels.append(read_level(name, w, h, types))
    return levels


def save_levels(levels):
    '''
    Save updated highscores in levels files
    '''
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


def find_music(modes):
    '''
    Find music packs in music directory
    '''
    default_path = os.path.join('music', '_default')
    default_bg_path = os.path.join(default_path, 'bg')
    default_bg = []
    for f in os.listdir(default_bg_path):
        path = os.path.join(default_bg_path, f)
        if os.path.isfile(path) and \
           (path.endswith('.mp3') or path.endswith('.wav')):
            default_bg.append(path)
    def_shoot = os.path.join(default_path, 'shoot.wav')
    def_hit = os.path.join(default_path, 'hit.wav')
    def_score_up = os.path.join(default_path, 'score_up.wav')
    def_swap = os.path.join(default_path, 'swap.wav')
    def_loose = os.path.join(default_path, 'loose.wav')
    def_win = os.path.join(default_path, 'win.wav')

    packs = {}
    for f in modes:
        dir = os.path.join('music', f)
        if os.path.exists(dir):
            bg = []
            bg_folder = os.path.join(dir, 'bg')
            for fi in bg_folder:
                f_name = os.path.join(bg_folder, fi)
                if (fi.endswith('.mp3') or fi.endswith('.wav')) and \
                   os.path.isfile(f_name):
                    bg.append(f_name)
            if len(bg) == 0:
                bg = default_bg

            shoot = try_to_find_sound(dir, 'shoot', def_shoot)
            hit = try_to_find_sound(dir, 'hit', def_hit)
            score_up = try_to_find_sound(dir, 'score_up', def_score_up)
            swap = try_to_find_sound(dir, 'swap', def_swap)
            loose = try_to_find_sound(dir, 'loose', def_loose)
            win = try_to_find_sound(dir, 'win', def_win)

            packs[f] = SoundPack(f, bg, shoot, hit, score_up, swap, loose, win)
        else:
            packs[f] = SoundPack(f, default_bg, def_shoot, def_hit,
                                 def_score_up, def_swap, def_loose, def_win)
    return packs


def try_to_find_sound(dir, sound, default):
    '''
    Tries to find sound  with mp3 of wav ext in dir
    else returns default
    '''
    file = os.path.join(dir, sound + '.wav')
    if not os.path.exists(file):
        file = os.path.join(dir, sound + '.mp3')
        if not os.path.exists(file):
            file = default
    return file
