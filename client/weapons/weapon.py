#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from weapons.tir import Tir
from threading import Timer

class Weapon:
    def __init__(self, player):
        self.player = player
        self.name = 'Anonymous Weapon'
        self.max_ammo = 20
        self.damage = 20
        self.shoot_speed = 22
        self.munition_size = 12
        self.shoot_cooldown = .2
        self.reload_cooldown = 1
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

    def shoot(self):
        if not self.can_shoot: return
        tir = Tir(self.player.x, self.player.y, self.player.dir, self)
        self.ammo -= 1
        self.can_shoot = False
        Timer(self.shoot_cooldown, self.allow_shoot).start()

    def allow_shoot(self):
        self.can_shoot = True

    def stop_fire(self, *event):
        self.autofire = False

    def reload(self, *event):
        if self.ammo < self.max_ammo:
            self.is_reloading = True
            Timer(self.reload_cooldown, self.has_reload).start()

    def has_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False
        if self.autofire:
            self.proceed_shoot()

class Sniper(Weapon):
    def __init__(self, player):
        super(Sniper, self).__init__(player)
        self.name = 'sniper'
        self.max_ammo = 5
        self.damage = 65
        self.shoot_speed = 25
        self.munition_size = 18
        self.shoot_cooldown = .6
        self.reload_cooldown = 2
        self.ammo = self.max_ammo


class Shotgun(Weapon):
    def __init__(self, player):
        super(Shotgun, self).__init__(player)
        self.name = 'fusil à pompe'
        self.max_ammo = 5
        self.damage = 15
        self.shoot_speed = 20
        self.munition_size = 7
        self.shoot_cooldown = .45
        self.reload_cooldown = 1.5
        self.nb_shoot = 5
        self.range = 350
        self.dispersion = math.pi/12
        self.ammo = self.max_ammo

    def shoot(self):
        if not self.can_shoot: return
        for i in range(self.nb_shoot):
            dispersion = ((-1)**i)*self.dispersion*i/10
            tir = Tir(self.player.x, self.player.y, self.player.dir + dispersion, self)
        self.ammo -= 1
        self.can_shoot = False
        Timer(self.shoot_cooldown, self.allow_shoot).start()


class AR(Weapon):
    def __init__(self, player):
        super(AR, self).__init__(player)
        self.name = 'fusil d\'assaut'
        self.max_ammo = 20
        self.damage = 20
        self.shoot_speed = 22
        self.munition_size = 12
        self.shoot_cooldown = .15
        self.reload_cooldown = 1.1
        self.ammo = self.max_ammo
