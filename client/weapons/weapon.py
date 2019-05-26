#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import pygame.mixer as mixer

from weapons.tir import Tir, Ray
from threading import Timer

mixer.init()

SOUND_PATH = 'ressources/sound/'

class Weapon:
    def __init__(self, player):
        self.player = player
        self.name = 'Anonymous Weapon'
        self.shot_sound = None
        self.reload_sound = None
        self.bullets_drawn = 0
        self.bullets_hit = 0
        self.max_ammo = 20
        self.damage = 20
        self.shoot_speed = 22
        self.munition_size = 12
        self.shoot_cooldown = .2
        self.reload_cooldown = 1
        self.nb_shoot = 1
        self.dispersion = 0
        self.damage_decrease = {'range': math.inf, 'factor': 1}
        self.range = math.inf
        self.can_shoot = True
        self.is_reloading = False
        self.autofire = False
        self.ammo = self.max_ammo

    def proceed_shoot(self, *event):
        if self.ammo > 0 and not self.is_reloading:
            if event:
                self.autofire = True
                self.proceed_shoot()
            elif self.autofire:
                self.shoot()
                Timer(self.shoot_cooldown, self.proceed_shoot).start()
        else:
            self.reload()

    def pre_shoot(self):
        pass

    def shoot(self):
        if not self.can_shoot: return
        self.pre_shoot()
        x = self.player.x + math.cos(self.player.dir) * 20
        y = self.player.y + math.sin(self.player.dir) * 20

        for i in range(self.nb_shoot):
            dispersion = ((-1)**i)*self.dispersion*i/10
            tir = Tir(x, y, self.player.dir + dispersion, self)
            self.player.play_sound(self.shot_sound)
        self.ammo -= 1
        self.bullets_drawn += self.nb_shoot
        self.can_shoot = False
        Timer(self.shoot_cooldown, self.allow_shoot).start()

    def allow_shoot(self):
        self.can_shoot = True

    def stop_fire(self, *event):
        self.autofire = False

    def reload(self, *event):
        if self.ammo < self.max_ammo and not self.is_reloading:
            self.player.message('info', 'Reloading')
            self.is_reloading = True
            self.player.play_sound(self.reload_sound)
            Timer(self.reload_cooldown, self.has_reload).start()

    def has_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False
        if self.autofire:
            self.proceed_shoot()

class Sniper(Weapon):
    def __init__(self, player):
        super(Sniper, self).__init__(player)
        self.name = 'Sniper'
        self.max_ammo = 5
        self.damage = 55
        self.shoot_speed = 28
        self.munition_size = 16
        self.shoot_cooldown = .68
        self.reload_cooldown = 1.9
        self.ammo = self.max_ammo


class Shotgun(Weapon):
    def __init__(self, player):
        super(Shotgun, self).__init__(player)
        self.name = 'Fusil à pompe'
        self.max_ammo = 5
        self.damage = 15
        self.shoot_speed = 20
        self.munition_size = 6
        self.shoot_cooldown = .45
        self.reload_cooldown = 1.42
        self.nb_shoot = 5
        self.range = 335
        self.damage_decrease = {'range': self.range / 2, 'factor': 0.67}
        self.dispersion = math.pi/15
        self.ammo = self.max_ammo

class AR(Weapon):
    def __init__(self, player):
        super(AR, self).__init__(player)
        self.name = 'Fusil d\'assaut'
        self.shot_sound = mixer.Sound(SOUND_PATH + f'piou{random.randint(1, 3)}.wav')
        self.reload_sound = mixer.Sound(SOUND_PATH + 'reload.wav')
        self.max_ammo = 20
        self.damage = 20
        self.damage_decrease = {'range': 400, 'factor': 0.88}
        self.shoot_speed = 22
        self.munition_size = 12
        self.shoot_cooldown = .21
        self.reload_cooldown = 1.1
        self.ammo = self.max_ammo


class SMG(Weapon):
    def __init__(self, player):
        super(SMG, self).__init__(player)
        self.name = 'SMG'
        self.max_ammo = 35
        self.damage = 12
        self.damage_decrease = {'range': 300, 'factor': 0.8}
        self.shoot_speed = 25
        self.munition_size = 6
        self.shoot_cooldown = .1
        self.reload_cooldown = .9
        self.dispersion = math.pi/35
        self.ammo = self.max_ammo

    def pre_shoot(self):
        self.player.dir += random.random()*self.dispersion

class Beam(Weapon):
    def __init__(self, player):
        super().__init__(player)
        self.name = 'Rayon'
        self.max_ammo = 100
        self.damage = 1 # /frame
        self.shoot_speed = 100
        self.munition_size = 500
        self.reload_cooldown = 1.8
        self.ammo = self.max_ammo
        self.is_shooting = False
        self.ray = Ray(self.player.x + math.cos(self.player.dir) * 12, self.player.y + math.sin(self.player.dir) * 12, self.player.dir, self)

    def proceed_shoot(self, *event):
        if self.ammo > 0 and not self.is_reloading:
            self.shoot()
        else:
            self.reload()

    def shoot(self):
        if not self.can_shoot: return
        self.ray.toggle_state('active')

    def stop_fire(self, *event):
        self.ray.toggle_state('inactive')
