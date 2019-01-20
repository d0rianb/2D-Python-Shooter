import os
from map.object import Object


class Map:
    def __init__(self, env, file, name='Map1'):
        self.env = env
        self.env.map = self
        self.name = name
        self.objects = {}
        self.file = file

        #open map file and put all lines in list
        dir = os.path.dirname(os.path.realpath(__file__))
        mapFile = open(os.path.join(dir, file), "r")
        lines = []
        for line in mapFile.readlines():
            lines.append(line.strip("\n").split(" "))

        #process lines and create objects
        inObject = False
        currentId = 0
        for l in lines:
            if l[0] == "object" and len(l) >= 5:
                inObject = True
                self.objects[l[1]] = Object(l[1], l[2], l[3], l[4], env)
                currentId = l[1]
            elif l[0] == "endObject":
                inObject = False
            elif inObject == True and l[0] == "rect" and len(l) >= 6:
                self.objects[currentId].addRect(l[1], l[2], l[3], l[4], l[5])


    def render(self):
        for key in self.objects:
            self.objects[key].render(self.env)
