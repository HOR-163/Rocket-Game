
import pygame
from CONSTANTS import *
def cubic_bezier(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int, t: float, screen = None, color = (255,0,0), position = (WIDTH - 100, HEIGHT - 100)) -> float:
    """Given 2 anchors (control points) and 2 handles, calculate the y coordinate of given cubic bezier curve.
    x1, y1 - control point 1
    x2, y2 - first points handle
    x3, y3 - control point 2
    x4, y4 - second points handle
    t - a 0 to 1 value inputted to calculate the x and y coordinate of a point in bezier curve. 0 is control point 1 and 1 is control point 2
    """

    y1, y2, y3, y4 = -y1, -y2, -y3, -y4
    negative = False
    if t < 0:
        t = abs(t)
        negative = True
    
    # For debugging draw the bezier curve
    if screen is not None:
        pygame.draw.rect(screen, 'white', pygame.Rect(position[0], position[1], 100, 100))
        for _t in range (100):
            _t = _t / 100
            x = ((1 - _t) ** 3) * x1 + ((1 - _t) ** 2) * 3 * _t * x2 + (_t ** 3) * x4  + (1 - _t) * 3 * (_t ** 2) * x3
            y = ((1 - _t) ** 3) * y1 + ((1 - _t) ** 2) * 3 * _t * y2 + (_t ** 3) * y4 + (1 - _t) * 3 * (_t ** 2) * y3
            pygame.draw.circle(screen, 'black', (position[0] + x, position[1] + y + 100), 1)

    # In this is becase we don't need the x coordinate, it's basically what we fetch into the formula, to get the y coordinate
    y = ((1 - t) ** 3) * y1 + ((1 - t) ** 2) * 3 * t * y2 + (t ** 3) * y4 + (1 - t) * 3 * (t ** 2) * y3

    # For debugging draw the point on to the bezier curve
    if screen is not None:
        x = ((1 - t) ** 3) * x1 + ((1 - t) ** 2) * 3 * t * x2 + (t ** 3) * x4 + (1 - t) * 3 * (t ** 2) * x3
        pygame.draw.circle(screen, color, (position[0] + x, position[1] + y + 100), 2)
    
    if negative:
         return -y / 2
    return y / 2 