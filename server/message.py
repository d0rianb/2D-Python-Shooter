#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import logging

ENDING_CHAR = '!#'

class Message:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.infos = {
            'timestamp': time.time()
        }

    def encode(self):
        return (json.dumps(self.__dict__) + ENDING_CHAR).encode('utf-8')
