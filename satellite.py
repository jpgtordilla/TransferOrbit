import pygame as pg
from constants import *

class Satellite:
    """Creates a satellite that follows a specific trajectory"""
    def __init__(self, init_orbit, factor):
        self.factor = factor # scaling factor calculated in game_loop

        self.width = SAT_WIDTH
        self.height = SAT_HEIGHT
        self.orbit = init_orbit
        self.x = self.translate_coord_x(self.orbit.r_orbit(0)) # screen initial x coordinate position
        self.y = HEIGHT / 2 - self.height / 2 # screen initial y coordinate position

        self.image = pg.transform.scale(pg.image.load("sat-sprite.jpg").convert(), (self.width, self.height))
        self.image.set_colorkey(BLACK)
        self.sat_rect = pg.Rect(self.get_x_coord(), self.get_y_coord(), self.width, self.width)

        self.orbit_points : list[list[float]] = self.orbit.get_orbit()
        self.current_index = 0 # track which orbit coordinate to use in the update method

    def translate_coord_x(self, x_unscaled):
        """Converts the unscaled x coordinate in meters to a pixel value"""
        return int((x_unscaled / self.factor) + WIDTH / 2) - self.width / 2

    def translate_coord_y(self, y_unscaled):
        """Converts the unscaled y coordinate in meters to a pixel value"""
        return int((y_unscaled / self.factor) + HEIGHT / 2) - self.height / 2

    def set_x_coord(self, x_unscaled):
        self.x = self.translate_coord_x(x_unscaled)

    def set_y_coord(self, y_unscaled):
        self.y = self.translate_coord_y(y_unscaled)

    def get_x_coord(self):
        return self.x

    def get_y_coord(self):
        return self.y

    def set_orbit(self, new_orbit):
        """Set to a new orbit, as well as set orbit points, such as when transfer occurs"""
        self.orbit = new_orbit
        self.orbit_points = new_orbit.get_orbit()

    def get_orbit_points(self):
        """Returns the xy pairs for the current orbit"""
        return self.orbit.get_orbit() # xy pairs for the orbit

    def draw_satellite(self, draw_surface):
        draw_surface.blit(self.image, self.sat_rect)

    def get_orbit_index(self):
        return self.current_index

    def set_orbit_index(self):
        """Increment the current orbit index"""
        if self.current_index < len(self.orbit_points) - 1:
            self.current_index += 1
        else:
            self.current_index = 0

    def update_satellite(self):
        """update the satellite position based on the orbit position array"""
        self.set_orbit_index()
        self.set_x_coord(self.get_orbit_points()[self.get_orbit_index()][0])
        self.set_y_coord(self.get_orbit_points()[self.get_orbit_index()][1])
        self.sat_rect = pg.Rect(self.get_x_coord(), self.get_y_coord(), self.width, self.width)

