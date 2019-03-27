#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Config pour Cx_Freeze '''

import sys, os
import cx_Freeze as cx
import main

build_options = {
    'path': sys.path,
    'includes': ['keyboard', 'encodings'],
    'optimize': 2,
    'silent': True
}

base = None
if sys.platform == "win32":
    options["include_msvcr"] = True
    base = "Win32GUI"

executable = cx.Executable(
    script='main.py',
    base=base
)


cx.setup(
    name = '2PQSTD',
    targetName = 'app',
    version = main.__version__,
    description = 'A 2D online multiplayer game',
    options = {'build_exe': build_options} ,
    executables = [executable]
)
