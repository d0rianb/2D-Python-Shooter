#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import threading

from render import RenderedObject

class MeleeAttack:
    def __init__(self, player):
        self.player = player
        self.env = self.player.env
        self.name = 'Coup de mêlée'
        self.attack_cooldown = .65
        self.range = 40
        self.damage = 10
        self.can_attack = True

    def attack(self, *event):
        if not self.can_attack: return
        closer_player = self.player.detect_closer_player()
        if closer_player and self.player.dist(closer_player) <= self.range:
            self.player.hit(closer_player, self.damage)
            closer_player.hit_by(self.player, self.damage)
            self.env.rendering_stack.append(RenderedObject('oval', self.player.x - self.range, self.player.y - self.range, x2=self.player.x + self.range, y2=self.player.y + self.range, color='lightgrey', zIndex=5))
            self.end_attack()

    def end_attack(self):
        self.can_attack = False
        threading.Timer(self.attack_cooldown, self.allow_attack).start()

    def allow_attack(self):
        self.can_attack = True
