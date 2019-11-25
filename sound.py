from PyQt5.QtMultimedia import (QMediaPlaylist, QMediaContent,
                                QMediaPlayer, QSound)
from PyQt5.QtCore import QUrl
import os


class SoundPack():
    def __init__(self, name, bg, shoot, hit, score_up, swap, loose, win):
        '''
        Creates Soundpack

        name - soundpack name
        other params - non-absolute way to files
        '''
        self.name = name

        self.back = QMediaPlaylist()
        for sound in bg:
            url = QUrl.fromLocalFile(os.path.join(os.getcwd(), sound))
            self.back.addMedia(QMediaContent(url))
        self.back.setPlaybackMode(QMediaPlaylist.Loop)
        self.bg = QMediaPlayer()
        self.bg.setPlaylist(self.back)
        self.bg.setVolume(20)

        self.shoot = QSound(shoot)
        self.hit = QSound(hit)
        self.score_up = QSound(score_up)
        self.swap = QSound(swap)
        self.loose = QSound(loose)
        self.win = QSound(win)


class SoundPlayer():
    def __init__(self, packs, current):
        '''
        Creates Sound Player

        packs - dictionary with sounpacks
        current - name of current mode
        '''
        self.curr = current
        self.packs = packs
        self.actions = {
            'hit': self.hit,
            'score_up': self.score_up,
        }

    def play_bg(self):
        '''
        Plays background music
        '''
        self.packs[self.curr].bg.play()

    def shoot(self):
        '''
        Plays shooting sound
        '''
        self.packs[self.curr].shoot.play()

    def hit(self):
        '''
        Plays ball-hitting sound
        '''
        self.packs[self.curr].hit.play()

    def score_up(self):
        '''
        Plays when balls are removed from sequence
        '''
        self.packs[self.curr].score_up.play()

    def swap(self):
        '''
        Plays on ball swapping
        '''
        self.packs[self.curr].swap.play()

    def loose(self):
        '''
        Plays on game losing
        '''
        self.packs[self.curr].loose.play()

    def win(self):
        '''
        Plays on game winning
        '''
        self.packs[self.curr].win.play()

    def switch(self, new_mode):
        '''
        Switches the game mode to new_mode
        '''
        self.curr = new_mode

    def handle_events(self, queue):
        '''
        Handle sound events
        '''
        for action in queue:
            self.actions[action]()
