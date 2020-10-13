#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Stats:
    def __init__(self, env):
        self.env = env
        self.last_frame_timestamp = 0   #ms
        self.frame_timestamp = 0       #ms
        self.frametime = 0              #ms
        self.framerate = self.env.max_framerate

    def calculate(self, sample=10):
        end_time = time.time()
        self.frametime = (end_time - self.last_frame_timestamp)
        framerate = int(sample / self.frametime)
        self.framerate = framerate if framerate != 0 and framerate <= self.env.max_framerate else self.env.max_framerate
        self.last_frame_timestamp = end_time