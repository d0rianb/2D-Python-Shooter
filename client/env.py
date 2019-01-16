import tkinter as tk

class Env:
    def __init__(self,fen, width, height, canvas):
        self.fen = fen
        self.canvas = canvas
        self.width = width
        self.height = height
        self.framerate = 60
        self.players = []
        self.shoots = []
        self.viewArea = { 'x': 0, 'y': 0, 'width': self.width, 'height': self.height }


    def update(self):
        self.canvas.delete('all')
        for player in self.players:
            player.update()
        for shoot in self.shoots:
            shoot.update()
        self.render()
        self.fen.after(1000//self.framerate, self.update)

    def render(self):
        for player in self.players:
            player.render(self.canvas)
        for shoot in self.shoots:
            shoot.render(self.canvas)
        self.canvas.pack()
