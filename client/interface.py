#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.font as tkFont
import keyboard
from render import RenderedObject


class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.env.interface = self
        self.margin_x = 8
        self.margin_y = 20
        self.width = env.viewArea['width']
        self.height = env.viewArea['height']
        self.padding = 20
        self.informations = {}
        self.color = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')

    def display_help(self, *args):
        text = ' Se déplacer : Z, Q, S, D (ou flèches directionnelles)\n Tirer : Clic Droit\n Dash : Majuscule gauche\n' + 'Recharger : R\n Restart Game: G (only local)\n Toggle Dash Preview: A\n Display Help : H\n Panic : P '
        self.env.rendering_stack.append(RenderedObject('text', self.env.width/2, 100, text=text, font=self.font, color=self.color, zIndex=10))

    def parse(self, position, x, y, anchor):
        infos = self.informations[position]
        for (index, info) in enumerate(infos):
            self.env.rendering_stack.append(RenderedObject('text', x, y + index*self.padding,
                text='{0}: {1}'.format(info, infos[info]),
                anchor=anchor,
                color=self.color,
                font=self.font))

    def update(self):
        self.informations = {
            'TopLeft': {
                'Player Name': self.player.name,
                'FrameRate': self.env.framerate,
                'Ping': '{0:.2g} ms'.format(self.player.client.ping) if self.player.client else 0
            },
            'TopRight': {
                'People Alive': len(list(filter(lambda player: player.alive, self.env.players))),
                'Kills': len(self.player.kills),
                'Assists': len(self.player.assists)
            },
            'BottomRight': {
                'Health': self.player.health,
                'Ammo': self.player.ammo if not self.player.is_reloading else 'Rechargement',
                'Dash': self.player.dash_left
            }
        }
        if keyboard.is_pressed('h'):
            self.display_help()


    def render(self):
        for position in self.informations:
            x, y = self.margin_x, self.margin_y
            anchor = 'w'
            if position == 'TopRight' or position == 'BottomRight':
                x = self.width - self.margin_x
                anchor = 'e'
            if position == 'BottomRight':
                y = self.height - 2.5*len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y, anchor)


class InterfaceMessage:
    def __init__(self, interface, type, text):
        self.interface = interface
        self.type = type
        self.text = text

        self.x = interface.env.viewArea['x'] / 2
        self.y = interface.env.viewArea['y'] / 2

        if self.type == 'info':
            self.color = "#AAA"

    def update(self):
        self.y += 1
        self.color

    def render(self):
        pass
