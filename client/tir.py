import math

class Tir:
    def __init__(self, id, x, y, dir, from_player):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = 20
        self.speed = 15 * 60/from_player.env.framerate
        self.size = 12
        self.head = { 'x': x, 'y': y }
        self.from_player = from_player
        self.env = from_player.env

    def checkWallCollide(self, map): #doesn't work
        for object_id in map.objects:
            for rect_id in map.objects[object_id].rects:
                rect = map.objects[object_id].rects[rect_id]
                if self.head['x'] >= rect.rendered['x'] and self.head['x'] <= rect.rendered['x'] + rect.rendered['height']:
                    if self.head['y'] >= rect.rendered['y'] and self.head['y'] <= rect.rendered['y'] + rect.rendered['height']:
                        print('Hit a Wall')
                    # self.env.shoots.remove(self)

    def update(self):
        self.x += math.cos(self.dir)*self.speed
        self.y += math.sin(self.dir)*self.speed
        self.head = {
            'x': self.x + math.cos(self.dir)*self.size,
            'y': self.y + math.sin(self.dir)*self.size
        }
        # self.checkWallCollide(self.env.map)

    def render(self, canvas):
        canvas.create_line(self.x, self.y, self.head['x'], self.head['y'])
