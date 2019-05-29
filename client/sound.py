# -*- coding: utf-8 -*-

import os
import pygame.mixer as mixer


SOUND_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ressources', 'sound/')

mixer.init()

class Sound:
    def __init__(self, file, from_player=None):
        self.file = file
        self.player = from_player
        self.audio = mixer.Sound(os.path.join(SOUND_PATH, self.file))

    def __repr__(self):
        return f'Sound of {self.file} at <{id(self)}>'

    def set_volume(self, volume):
        self.audio.set_volume(volume)

    def play(self):
        self.audio.play()
