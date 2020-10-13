#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import json


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise ValueError(f'{filepath} is not a valid file path')
        with open(filepath, 'r') as conf_file:
            self.config = json.load(conf_file)
            self.new_config = self.config.copy()

    def get_config(self):
        return self.config

    def get(self, attr):
        if attr in self.config:
            return self.config[attr]

    def set(self, attr, value):
        self.new_config[attr] = value

    def save(self):
        with open(self.filepath, 'w') as config:
            config.write(json.dumps(self.new_config))
        self.config = self.new_config
