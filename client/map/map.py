import os
from map.rect import Rect


class Map:
    def __init__(self, env, file, name='Map1'):
        self.env = env
        self.env.map = self
        self.name = name
        self.rects = []
        self.file = file

        # open map file and put all lines in list
        dir = os.path.dirname(os.path.realpath(__file__))
        mapFile = open(os.path.join(dir, file), 'r')
        lines = []
        keyword = ['rect', 'object']
        for line in mapFile.readlines():
            if len(line.split()) > 0 and line.split()[0] in keyword:
                lines.append(line.strip('\n').split())

        for line in lines:
            if line[0] == 'rect':
                self.rects.append(Rect(len(self.rects) + 1, line[1], line[2], line[3], line[4], self))

    def render(self):
        for rect in self.rects:
            rect.render()
