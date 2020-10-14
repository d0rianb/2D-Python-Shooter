#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import pip._internal as pip  # import pkg_resources


## INSTALLATION SCRIPT

def isMac():
    return platform.system() == 'Darwin'


def isWindows():
    return platform.system() == 'Windows'


pkgs = ['keyboard', 'pygame']

for package in pkgs:
    try:
        import package
    except ImportError:
        pip.main(['install', package])
