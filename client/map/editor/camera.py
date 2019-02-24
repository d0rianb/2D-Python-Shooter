#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import keyboard

from render import RenderedObject
from object.rect import Rect
from object.circle import Circle

default_keys = {
    'up': 'z',
    'down': 's',
    'left': 'q',
    'right': 'd',
}

class Camera:
    def __init__(self, x, y, env, name="Camera"):
        self.id = 0
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.env.camera = self
        self.size = 10  # Radius
        self.color = '#0066ff'
        self.theorical_speed = 8
        self.speed = self.theorical_speed * 60 / self.env.framerate   # computed value
        self.key = default_keys
        keyboard.on_press_key('&', lambda *e: self.env.change_scale(value=1))

    def detect_keypress(self):
        x, y = 0, 0
        if keyboard.is_pressed(self.key['up']):
            y = -1
        if keyboard.is_pressed(self.key['down']):
            y = 1
        if keyboard.is_pressed(self.key['right']):
            x = 1
        if keyboard.is_pressed(self.key['left']):
            x = -1
        self.move(x, y)


    def collide_wall(self):
        x, y = self.x, self.y
        collide_x, collide_y = False, False
        delta = {'x': 0, 'y': 0}
        for obj in self.env.objects:
            if isinstance(obj, Rect):
                rect = obj
                delta_x, delta_y = 0, 0
                if y + self.size > rect.y and y - self.size < rect.y2 and x + self.size > rect.x and x - self.size < rect.x2:
                    delta_x_left = rect.x - (x + self.size)
                    delta_x_right = (x - self.size) - rect.x2
                    delta_x_left = delta_x_left if delta_x_left < 0 else 0
                    delta_x_right = delta_x_right if delta_x_right < 0 else 0
                    delta_x = max(delta_x_left, delta_x_right)
                    if delta_x == delta_x_right:
                        delta_x *= -1

                    delta_y_top = rect.y - (y + self.size)
                    delta_y_bottom = (y - self.size) - rect.y2
                    delta_y_top = delta_y_top if delta_y_top < 0 else 0
                    delta_y_bottom = delta_y_bottom if delta_y_bottom < 0 else 0
                    delta_y = max(delta_y_top, delta_y_bottom)
                    if delta_y == delta_y_bottom:
                        delta_y *= -1

                delta_min = min(abs(delta_x), abs(delta_y))
                delta_x = delta_x if abs(delta_x) == delta_min else 0
                delta_y = delta_y if abs(delta_y) == delta_min else 0
                ## Add the delta of each rectangle to the total delta (dict)
                if delta_x != 0 and delta['x'] == 0:
                    delta['x'] = delta_x
                if delta_y != 0 and  delta['y'] == 0:
                     delta['y'] = delta_y
            elif isinstance(obj, Circle):
                circle = obj
                dist = math.sqrt((self.x - circle.x)**2 + (self.y - circle.y)**2)
                if dist <= self.size + circle.radius:
                    delta_dist = dist - self.size - circle.radius
                    angle = math.atan2(circle.y - self.y, circle.x - self.x)
                    if delta['x'] == 0:
                        delta['x'] = math.cos(angle)*delta_dist
                    if delta['y'] == 0:
                        delta['y'] = math.sin(angle)*delta_dist
        return delta['x'], delta['y']

    def move(self, x, y):
        self.x += x * self.speed
        self.y += y * self.speed

        offset_x, offset_y = self.collide_wall()
        self.x += offset_x
        self.y += offset_y

        # Restreint le joueur à l'environnement
        if self.x - self.size <= 0:
            self.x = self.size
        elif self.x + self.size >= self.env.width:
            self.x = self.env.width - self.size
        if self.y - self.size <= 0:
            self.y = self.size
        elif self.y + self.size >= self.env.height:
            self.y = self.env.height - self.size

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def update(self):
        self.speed = self.theorical_speed * 60 / self.env.framerate
        self.detect_keypress()
        viewBox = self.env.viewArea
        if self.x >= viewBox['width'] / 2 and self.x <= self.env.width - viewBox['width'] / 2:
            viewBox['x'] = self.x - viewBox['width'] / 2
        else:
            viewBox['x'] = 0 if self.x <= viewBox['width'] / 2 else self.env.width - viewBox['width']
        if self.y >= viewBox['height'] / 2 and self.y <= self.env.height - viewBox['height'] / 2:
            viewBox['y'] = self.y - viewBox['height'] / 2
        else:
            viewBox['y'] = 0 if self.y <=viewBox['height'] / 2 else self.env.height - viewBox['height']

    def render(self):
        head_text = self.name
        self.env.rendering_stack.append(RenderedObject('oval', self.x - self.size, self.y - self.size, x2=self.x + self.size, y2=self.y + self.size, color=self.color, width=0))
        self.env.rendering_stack.append(RenderedObject('text', self.x - len(self.name) / 2, self.y - 20, text=head_text, color='#787878', zIndex=3))
