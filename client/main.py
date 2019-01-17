import tkinter as tk
import sys
import math
import random
import keyboard
from player import Player
from tir import Tir
from env import Env


fen = tk.Tk()
fen.title('2PQSTD')
width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()//2

canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC')

if __name__ == '__main__':
    env = Env(fen, width, height, canvas)
    dorian = Player(0, 100, 100, env, 'Dorian', own=True)
    test = Player(1, 300, 100, env, 'Test')
    env.update()
    fen.mainloop()
    sys.exit(0)
