import tkinter as tk
import os
import sys
import math
import random
import keyboard
from player import Player, Target
from tir import Tir
from env import Env
from interface import Interface
from map.map import Map


fen = tk.Tk()
fen.title('2PQSTD')
width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()

canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC', highlightthickness=0)

if __name__ == '__main__':
    env = Env(fen, width, height, canvas)
    map = Map(env, 'map1.txt', 'Test')

    dorian = Player(0, 50, 50, env, 'Dorian', own=True)
    test1 = Player(1, 500, 150, env, 'Test1')
    test2 = Player(2, 300, 400, env, 'Test2')
    for i in range(1, 5):
        Target(2 + i, random.randint(0, width), random.randint(100, height - 100), env)

    interface = Interface(dorian, env)

    env.update()
    interface.update()

    fen.mainloop()
    sys.exit(0)
