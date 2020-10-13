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

    def get(self, attr, use_new_config=False):
        if use_new_config and attr in self.new_config:
            return self.new_config[attr]
        if attr in self.config:
            return self.config[attr]

    def set(self, attr, value):
        nested = attr.split('.')
        if isinstance(self.new_config[nested[0]], dict) and len(nested) > 1:
            self.new_config[nested[0]][nested[1]] = value
        else:
            self.new_config[attr] = value

    def save(self):
        with open(self.filepath, 'w') as config:
            config.write(json.dumps(self.new_config))
        self.config = self.new_config
