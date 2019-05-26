#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class Event:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def submit(self):
        pass

    @staticmethod
    def handle(self, event):
        pass
