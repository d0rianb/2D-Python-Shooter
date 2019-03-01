#!/usr/bin/env python
# -*- coding: utf-8 -*-

import builtins

try:
    profile = builtins.__dict__['profile']
except KeyError:
    def profile(func): return func
finally:
    builtins.profile = profile
