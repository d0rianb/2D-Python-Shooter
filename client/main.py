import tkinter as tk
import os, sys
import math
import random
import keyboard
from player import Player
from tir import Tir
from env import Env
from interface import Interface
from map.map import Map


fen = tk.Tk()
fen.title('2PQSTD')
width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()

canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC', highlightthickness=0)

if __name__ == '__main__':
    env = Env(fen, 2560, 1440, canvas)
    map = Map(env, 'map1.txt', 'Test')

    dorian = Player(0, 100, 100, env, 'Dorian', own=True)
    test1 = Player(1, 500, 150, env, 'Test1')
    test2 = Player(1, 300, 400, env, 'Test2')

    interface = Interface(dorian, env)

    env.update()
    interface.update()

    fen.mainloop()
    sys.exit(0)
