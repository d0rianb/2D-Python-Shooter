#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.font as tkFont
import tkinter as tk
import keyboard
import math
import time
import sys

from object.color import Color
from render import RenderedObject

BG_COLOR = Color((241, 231, 220))

class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.env.interface = self
        self.player.interface = self
        self.menu = Menu(self)
        self.margin_x = 8
        self.margin_y = 20
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.padding = 20
        self.informations = {}
        self.messages = []
        self.color = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')

    def display_help(self, *args):
        text = (' Se déplacer : {up}, {down}, {left}, {right}\n' +
               ' Tirer : Clic Droit\n' +
               ' Dash : {dash}\n' +
               ' Recharger : {reload}\n' +
               ' Restart Game: G (only local)\n' +
               ' Toggle Dash Preview: {dash_preview}\n' +
               ' Display Help : {help}\n' +
               ' Panic : {panic} ').format(**{key: str(val).upper() if val != 56 else 'Shift' for key, val in self.player.key.items()})
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
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.informations = {
            'TopLeft': {
                'FrameRate': self.env.framerate,
                'Ping': '{0:.2g} ms'.format(self.player.client.ping) if self.player.client else 0
            },
            'TopRight': {
                'People Alive': len(list(filter(lambda player: player.alive, self.env.players))),
                'Kills': len(self.player.kills),
                'Assists': len(self.player.assists),
                'Damage': int(self.player.total_damage)
            },
            'BottomRight': {
                'Health': math.ceil(self.player.health),
                'Ammo': '|' * self.player.weapon.ammo if not self.player.weapon.is_reloading else 'Rechargement',
                'Dash': self.player.dash_left
            }
        }
        for msg in self.messages:
            msg.update()

    def render(self):
        for position in self.informations:
            x, y = self.x + self.margin_x, self.y + self.margin_y
            anchor = 'w'
            if position == 'TopRight' or position == 'BottomRight':
                x = self.x + self.width - self.margin_x
                anchor = 'e'
            if position == 'BottomRight':
                y = self.y + self.height - len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y, anchor)
        for msg in self.messages:
            msg.render()
        if self.menu:
            self.menu.render()

class ChatInfo:
    def __init__(self, env):
        self.env = env
        self.message = {}
        self.text = tk.StringVar()
        self.entry = tk.Entry(self.env.fen, width=50, bd=0, takefocus=0, highlightthickness=0, textvariable=self.text)
        self.entry_y = 0
        keyboard.on_press_key('/', self.focus_entry)
        keyboard.on_press_key('esc', self.unfocus_entry)
        keyboard.on_press_key('enter', self.parse)

    def focus_entry(self, *event):
        if self.entry_y == 0:
            entry_height = self.entry.winfo_height()
            self.entry_y = (self.env.height - entry_height) / self.env.height
        self.entry.place(relx=0, rely=self.entry_y, anchor=tk.SW)
        self.entry.focus()
        self.entry.selection_range(0, tk.END)
        self.env.command_entry_focus = True

    def unfocus_entry(self, *event):
        self.entry.place_forget()
        self.env.command_entry_focus = False

    def parse(self, *event):
        split = self.text.get().split(' ')
        command, *args = split
        if command == 'debug':
            type, value = args[0], args[1]
            self.debug(type, value)
        elif command == 'kill' or command == 'killall': ## Doesn't work
            if len(args) > 0:
                if args[0] == 'bot' or args[0] == 'bots':
                    self.env.players = [player for player in self.env.players if player.own]
                else:
                    player = self.select_player(args[0], args[1])
                    if player:
                        player.dead()
                        self.env.players.remove(player)
            else:
                self.env.players = []


    def debug(self, type, value):
        debug_fen = tk.Toplevel(self.env.fen)
        player = self.select_player(type, value)
        for key, val in player.__dict__.items():
            entry = tk.Label(debug_fen, text='{}: {}'.format(key, val))
            entry.pack(anchor=tk.W)

    def select_player(self, type, value):
        ''' return the first player where player.type = value '''
        for player in self.env.players:
            if str(player.__dict__[type]) == value:
                return player

    def update(self):
        pass

    def render(self):
        pass

class TempMessage:
    def __init__(self, type, text, interface, duration=0.8):
        self.interface = interface
        self.env = self.interface.env
        self.type = type
        self.text = text

        self.start = time.time()
        self.duration = duration  # s
        self.tick = 0


        self.x = self.interface.player.x
        self.y = self.interface.player.y + 20
        self.delta_y = 1
        self.speed = 1

        if self.type == 'global_info':
            self.x = self.interface.width / 2
            self.y = self.interface.height / 4
            self.initial_color = Color((96, 125, 139))
        elif self.type == 'info':
            self.initial_color = Color((96, 125, 139))
        elif self.type == 'warning':
            self.initial_color = Color((251, 140, 0))
        elif self.type == 'alert':
            self.initial_color = Color((211, 47, 47))
        elif self.type == 'hit':
            self.initial_color = Color((198, 40, 40))
        else:
            self.initial_color = Color((200, 200, 200))

        self.color = self.initial_color

        self.interface.messages.append(self)

    def destroy(self):
        self.interface.messages.remove(self)

    def update(self):
        delta_time = self.start + self.duration - time.time()
        if delta_time <= 0:
            return self.destroy()
        self.y += self.delta_y*self.speed
        self.color = Color.blend(self.initial_color, BG_COLOR, 1 - delta_time/self.duration)
        self.tick += 1

    def render(self):
        self.interface.env.rendering_stack.append(RenderedObject('text', self.x, self.y + self.interface.messages.index(self)*self.delta_y*self.interface.padding,
            text=self.text,
            anchor=tk.CENTER,
            color=self.color.to_hex(),
            font=self.interface.font,
            zIndex=5))

class DamageMessage(TempMessage):
    def __init__(self, player, text, interface):
        TempMessage.__init__(self, 'hit', text, interface, duration=0.95)
        self.player = player
        self.x = self.player.x + 15
        self.y = self.player.y - 20
        self.delta_y = -1
        self.speed = .75

class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.env = self.interface.env
        self.player = self.interface.player
        self.interface.menu = self
        self.stats = {}
        self.x = self.env.viewArea['width'] / 2
        self.y = self.env.viewArea['height'] / 2
        self.is_active = False
        self.font = tkFont.Font(family='Avenir Next', size=28, weight='normal')
        self.padding = 30

    def toggle(self, state=None):
        if state:
            if state == 'on':
                self.is_active = True
            if state == 'off':
                self.is_active = False
        else:
            self.is_active = not self.is_active

    def display_stats(self, animation=False):
        stats = self.player.stats()
        bgcolor = Color.blend(Color((20, 20, 20)), BG_COLOR, 0.8).to_hex() #(self.env.tick % 100) / 100
        stat_label = {'total_damage': 'Dommage Infligés', 'kills': 'Eliminiations', 'assists': 'Assistance', 'accuracy': 'Précision'}
        stat_suffixe = {'total_damage': '', 'kills': '', 'assists': '', 'accuracy': '%'}

        stat_text = ''
        for index, stat in enumerate(stats):
            stat_text += f'{stat_label[stat]} : {int(stats[stat])}{stat_suffixe[stat]}\n'
            deltaX =  self.env.viewArea['x'] + 0
            deltaY =  self.env.viewArea['y'] - (len(stats) / 2) * (self.padding)
        rect_width, rect_height = 400, 200
        self.env.rendering_stack.append(RenderedObject('text', self.x + deltaX, self.y + deltaY + index*self.padding, text=stat_text, color='#222', font=self.font, zIndex=10, anchor='center'))
        self.env.rendering_stack.append(RenderedObject('rect', self.x + self.env.viewArea['x'] - rect_width/2, self.y + self.env.viewArea['y'] - rect_height/2, width=rect_width, height=rect_height, color=bgcolor, zIndex=9))

    def render(self):
        if not self.is_active: return
        self.display_stats()
