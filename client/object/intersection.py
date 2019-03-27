#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def line_line(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) if (y4-y3)*(x2-x1) != (x4-x3)*(y2-y1) else 0
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) if (y4-y3)*(x2-x1) != (x4-x3)*(y2-y1) else 0
    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        intersectionX = x1 + (uA * (x2-x1));
        intersectionY = y1 + (uA * (y2-y1));
        return intersectionX, intersectionY
    return False


def line_rect(x1, y1, x2, y2, rx, ry, rw, rh):
    left = line_line(x1, y1, x2, y2, rx,ry, rx, ry+rh)
    right = line_line(x1, y1, x2, y2, rx+rw, ry, rx+rw, ry+rh)
    top = line_line(x1, y1, x2, y2, rx, ry, rx+rw, ry)
    bottom = line_line(x1, y1, x2, y2, rx, ry+rh, rx+rw, ry+rh)
    closest_point = (math.inf, math.inf)
    for point in [left, right, top, bottom]:
        if point:
            dist = math.sqrt((x1 - point[0])**2 + (y1 - point[1])**2)
            closest_dist = math.sqrt((x1 - closest_point[0])**2 + (y1 - closest_point[1])**2)
            if dist <= closest_dist:
                closest_point = point
    if closest_point != (math.inf, math.inf):
        return closest_point
