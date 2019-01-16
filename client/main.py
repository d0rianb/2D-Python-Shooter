import tkinter as tk
import sys
import math
import random
import keyboard
from player import Player
from tir import Tir

framerate = 60
players = []
shoots = []
mouse = {'x':0, 'y':0}

fen = tk.Tk()
fen.title('2PQSTD')
width, height = fen.winfo_screenwidth()//2, fen.winfo_screenheight()//2

def mouse_move(event):
    global mouse
    mouse['x'], mouse['y'] = event.x, event.y

def fire(event):
    shoots.append(dorian.shoot())

def move_player():
    global dorian
    x = 0
    y = 0
    if keyboard.is_pressed('z'):
        y = -1
    if keyboard.is_pressed('s'):
        y = 1
    if keyboard.is_pressed('d'):
        x = 1
    if keyboard.is_pressed('q'):
        x = -1
    dorian.move(x, y)

env = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC')

def update():
    global env, mouse
    env.delete('all')
    move_player()
    keyboard.on_press_key(56, dorian.dash, suppress=True) # shift
    for player in players:
        player.update(mouse)
        player.render(env)

    for shoot in shoots:
        shoot.update()
        shoot.render(env)
    env.pack()
    fen.after(1000//framerate, update)


fen.bind('<Motion>', mouse_move)
fen.bind('<Button-1>', fire)

if __name__ == '__main__':
    dorian = Player(100, 100)
    players.append(dorian)
    update()
    fen.mainloop()
    sys.exit(0)
