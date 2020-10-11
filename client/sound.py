# -*- coding: utf-8 -*-

import os
import pygame.mixer as mixer

mixer.init()

SOUND_PATH = 'ressources/sound/'

class Sound:
    def __init__(self, file, from_player=None):
        self.file = file
        self.player = from_player
        self.audio = None # mixer.Sound(os.path.join(SOUND_PATH, self.file))

    def __repr__(self):
        return f'Sound of {self.file} at <{id(self)}>'

    def set_volume(self, volume):
        return
        self.audio.set_volume(volume)

    def play(self):
        return
        self.audio.play()
