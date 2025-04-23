import pygame as pg
from constants import *

class Satellite:
    """Creates a satellite that follows a specific trajectory"""

    def __init__(self, init_orbit):
        self.orbit = init_orbit
        self.x = self.orbit.r_orbit(0) # x coordinate position (translated later with draw_satellite)
        self.y = 0 # y coordinate position (translated later with draw_satellite)
        self.width = 40
        self.height = 40

        self.image = pg.transform.scale(pg.image.load("sat-sprite.jpg").convert(), (self.width, self.height))
        self.image.set_colorkey(BLACK)
        self.sat_rect = pg.Rect(0, 0, self.width, self.width)

    def set_orbit(self, new_orbit):
        self.orbit = new_orbit # set to a new orbit, such as when transfer occurs

    def draw_satellite(self, draw_surface):
        draw_surface.blit(self.image, self.sat_rect)

"""ISSUES:
- rect x coordinate is set to zero as a test 
- need to have a function that gets the current scaling factor before graphing
"""

