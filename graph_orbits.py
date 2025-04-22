"""SOURCES
1. https://inventwithpython.com/pygameHelloWorld.py
2. Taylor, John R. Classical Mechanics. University Science Books, 2005.
"""

"""THEORY
(Taylor, John R. Classical Mechanics. University Science Books, 2005.)

General Kepler Orbit Equation:

r(phi) = c/(1 + epsilon * cos(phi))

- epsilon is a const.
- l is angular momentum, and is const.
- c = l**2 / (gamma * mu)
- gamma = G * m1 * m2
- mu = m1 * m2 / (m1 + m2) # reduced mass

Energy of a comet/body:

E = gamma**2 * mu * (epsilon**2 - 1) / 2 * l**2

Key: eccentricity determines the orbit's shape:
- epsilon = 0     -- E < 0 -- circle
- 0 < epsilon < 1 -- E < 0 -- ellipse
- epsilon = 1     -- E = 0 -- parabola
- epsilon > 1     -- E > 0 -- hyperbola

"""
import numpy as np
import pygame
from pygame.locals import *

"""PYGAME CONSTANTS: (https://inventwithpython.com/pygameHelloWorld.py)"""
surface = None
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

class Orbit:
    """Graphs conic section orbits based on general Kepler Orbit Equation"""
    def __init__(self, epsilon=0.0, l=10**24, m1=5.97219*10**24, m2=10**13):
        self.G = 6.67430 * 10 ** -11  # gravitational const.
        self.M1 = m1  # mass of Earth
        self.M2 = m2  # mass of a typical comet
        self.GAMMA = self.G * self.M1 * self.M2
        self.MU = (self.M1 * self.M2) / (self.M1 + self.M2) # reduced mass
        self.L = l # angular momentum
        self.EPSILON = epsilon # eccentricity
        self.C = self.L**2 / (self.GAMMA * self.MU)

    def r_orbit(self, phi):
        return self.C/(1 + self.EPSILON * np.cos(phi))

    def energy(self):
        return self.GAMMA ** 2 * self.MU * (self.EPSILON ** 2 - 1) / 2 * self.L ** 2

    def get_orbit(self, num_points=300, percent=0.1) -> list[list[float]]:
        """Returns a list of (x, y) pairs for a given orbit"""
        # graph orbit
        # - for (default=360) equally spaced points, calculate r and add to 2D list
        # - graph each point in each array (x and y)
        r_list = [] # 2D array
        xy_point_list = [] # 2D array

        current_phi = 0

        # get the points and add to array
        for i in range (num_points):
            radian_increment = 2*np.pi / num_points
            current_phi += radian_increment
            current_r = self.r_orbit(current_phi)
            r_list.append([current_r, current_phi])

        # if hyperbola or parabola (EPSILON = 1 or "..." > 1), shave off (default 10%) the longer r values
        end_percent_index = int(len(r_list) - len(r_list) * percent)

        if self.EPSILON == 1 or self.EPSILON == -1:
            r_list.sort(key=lambda l:l[0]) # sort by the first value (r)
            r_list = r_list[:end_percent_index]
        elif self.EPSILON > 1 or self.EPSILON < -1:
            r_list.sort(key=lambda l:abs(l[0])) # sort by the abs. value of first value (r)
            r_list = r_list[:end_percent_index]

        for i in range(len(r_list)):
            current_r = r_list[i][0]
            current_phi = r_list[i][1]
            # recall:
            # - x = r * np.cos(phi)
            # - y = r * np.sin(phi)
            try:
                current_x = int(current_r * np.cos(current_phi))
            except OverflowError:
                continue
            current_y = int(current_r * np.sin(current_phi))

            xy_point_list.append([current_x, current_y])

        return xy_point_list

def graph_orbits(orbit_list, num_points=300):
    """Given a list of orbit objects, plot them on the screen"""

    """
    # get max in the list
    # find dividing factor that reduced it to the width of the screen (divided by 2)
    r_max = max([abs(elem[0]) for elem in r_list])
    factor = r_max / (WIDTH / 2)

    # graph each point
    for i in range(len(xy_point_list)):
        current_x_coord = int((xy_point_list[i][0] / factor) + WIDTH / 2)
        current_y_coord = int((xy_point_list[i][1] / factor) + HEIGHT / 2)
        # plot point
        surface.set_at((current_x_coord, current_y_coord), WHITE)
    """

    max_radius = get_max_radius(orbit_list)

    # calculate scaling factor based on the max orbit
    factor = max_radius / (WIDTH / 2)

    # plot each trajectory, scaling w.r.t. the factor
    for orbit in orbit_list:
        curr_points_list = orbit.get_orbit(num_points)
        for point in curr_points_list:
            x = int((point[0] / factor) + WIDTH / 2)
            y = int((point[1] / factor) + WIDTH / 2)
            surface.set_at((x, y), WHITE)

"""HELPER FUNCTIONS FOR SCALING ORBITS TO FIT THE SCREEN"""

def get_key_with_max_value(orbit_dict):
    """Gets the key with the max value in a dictionary"""
    max_key = max(orbit_dict.keys(), key=orbit_dict.get) # same as passing in orbit_dict.keys()
    return max_key

def get_max_radius(orbit_objs: list[Orbit]):
    """Returns the max radius given a list of Orbit objects"""
    radius_list = []
    for orbit in orbit_objs:
        radius_list.append(orbit.r_orbit(0))  # radius at 0 phi
    return max(radius_list)

def get_orbit_with_max_radius(orbit_objs: list[Orbit]):
    """Returns the orbit that has the max radius given a list of Orbit objects"""
    orbit_dict = {}
    for orbit in orbit_objs:
        orbit_dict[orbit] = orbit.r_orbit(0) # radius at 0 phi
    return get_key_with_max_value(orbit_dict)

def get_orbit_type(orbit_obj: Orbit) -> str:
    if orbit_obj.EPSILON == 0:
        return "CIRCLE"
    elif (0 < orbit_obj.EPSILON < 1) or (0 > orbit_obj.EPSILON > -1):
        return "ELLIPSE"
    elif orbit_obj.EPSILON == 1 or orbit_obj.EPSILON == -1:
        return "PARABOLA"
    else:
        return "HYPERBOLA"

"""MAIN LOOP FOR DRAWING ORBITS AND UPDATING"""

def game_loop():
    parabola = Orbit(epsilon=1)  # parabola
    hyperbola = Orbit(epsilon=1.9)  # hyperbola
    circle = Orbit(epsilon=0)  # circle
    circle_small = Orbit(epsilon=0, l=0.8*10**24)  # small circle
    orbits = [parabola, hyperbola, circle, circle_small]

    graph_orbits(orbits)

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

"""NOTES: 

ISSUE
- scaling breaks when negative epsilon is used
- should be an easy fix, but it is not necessary 

FUTURE
- short-term goal: animate a satellite following the trajectory of the orbit (1 point per frame, display velocity) 
"""
