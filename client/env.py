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

    def manageShoots(self):
        for shoot in self.shoots:
            if shoot.x < 0 or shoot.x > self.width or shoot.y < 0 or shoot.y > self.height:
                self.shoots.remove(shoot)
            else:
                shoot.update()


    def update(self):
        self.canvas.delete('all')
        for player in self.players:
            player.update()
        self.manageShoots()
        self.render()
        self.fen.after(1000//self.framerate, self.update)

    def render(self):
        for player in self.players:
            player.render(self.canvas)
        for shoot in self.shoots:
            shoot.render(self.canvas)
        self.canvas.pack()
