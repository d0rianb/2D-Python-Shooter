#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Color:
    def __init__(self, rgb=(0, 0, 0)):
        self.rgb = rgb
        self.r = self.rgb[0]
        self.g = self.rgb[1]
        self.b = self.rgb[2]

    def to_hex(self):
        return f"#{''.join(f'{hex(c)[2:].upper():0>2}' for c in self.rgb)}"

    @staticmethod
    def blend(color1, color2, alpha):
        alpha = alpha if alpha <= 1 else 1
        r = (1-alpha)*color1.r   + alpha*color2.r
        g = (1-alpha)*color1.g + alpha*color2.g
        b = (1-alpha)*color1.b  + alpha*color2.b
        return Color((int(r), int(g), int(b)))
