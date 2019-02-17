#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tir import Tir

class Weapon:
    def __init__(self):
        self.max_ammo = 0
        self.ammo = self.max_ammo
        self.is_reloading = False
        self.autofire = False
        self.reload_cooldown = 1
        self.autofire_cooldown = .2

    def shoot(self, *event):
        if self.ammo > 0 and not self.is_reloading:
            if event:
                self.autofire = True
                self.shoot()
            if self.autofire and not event:
                tir = Tir(len(self.env.shoots), self.x, self.y, self.dir, self)
                self.env.shoots.append(tir)
                self.ammo -= 1
                Timer(self.autofire_cooldown, self.shoot).start()
        else:
            self.reload()

    def stop_fire(self, *event):
        self.autofire = False

    def reload(self, *arg):
        if self.ammo < self.max_ammo:
            self.is_reloading = True
            Timer(self.reload_cooldown, self.has_reload).start()

    def has_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False
        if self.autofire:
            self.shoot()

class Sniper(Weapon):
    def __init__(self):
        super(Sniper, self).__init__()

class Shotgun(Weapon):
    def __init__(self):
        super(Sniper, self).__init__()

class AR(Weapon):
    def __init__(self):
        super(Sniper, self).__init__()
