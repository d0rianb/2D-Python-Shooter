#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Stats:
    def __init__(self, env):
        self.env = env
        self.last_frame_timestamp = 0   #ms
        self.frame_timestamp = 0        #ms
        self.frametime = 0              #ms
        self.framerate = self.env.max_framerate
        self.current_frame_duration  = 0
        self.theorical_max_fps = 0

    def time(self):
        # To replace with a more accurate timer
        return time.time()

    def frame_start(self):
        self.current_frame_duration = self.time()

    def frame_end(self):
        self.frametime = self.time() - self.current_frame_duration
        self.theorical_max_fps = int(1 / self.frametime)

    def calculate_fps(self, sample=10):
        end_time = self.time()
        delta_time = end_time - self.last_frame_timestamp
        framerate = int(sample / delta_time)
        self.framerate = framerate if framerate != 0 and framerate <= self.env.max_framerate else self.env.max_framerate
        self.last_frame_timestamp = end_time

