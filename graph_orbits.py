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

def game_loop():
    parabola = OrbitGrapher(epsilon=1.5)  # parabola
    parabola.graph_orbit()
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

class OrbitGrapher:
    def __init__(self, epsilon=0.0, l=10**24, m1=5.97219*10**24, m2=10**13):
        self.G = 6.67430 * 10 ** -11  # gravitational const.
        self.M1 = m1  # mass of Earth
        self.M2 = m2  # mass of a typical comet
        self.GAMMA = self.G * self.M1 * self.M2
        self.MU = (self.M1 * self.M2) / (self.M1 + self.M2) # reduced mass
        self.L = l # angular momentum
        self.EPSILON = epsilon # eccentricity
        self.C = self.L**2 / (self.GAMMA * self.MU)

        """PYGAME CONSTANTS
        (https://inventwithpython.com/pygameHelloWorld.py)
        """
        self.surface = None
        self.WIDTH = 800
        self.HEIGHT = 800
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Orbit Graph")

    def r_orbit(self, phi):
        return self.C/(1 + self.EPSILON * np.cos(phi))

    def energy(self):
        return self.GAMMA ** 2 * self.MU * (self.EPSILON ** 2 - 1) / 2 * self.L ** 2

    def graph_orbit(self, num_points=300, percent=0.1):
        # graph orbit
        # - for (default=360) equally spaced points, calculate r and add to 2D list
        # - graph each point in each array (x and y)
        r_list = [] # 2D array
        x_point_list = [] # 1D array
        y_point_list = [] # 1D array

        current_phi = 0

        # get the points and add to array
        for i in range (num_points):
            radian_increment = 2*np.pi / num_points
            current_phi += radian_increment
            current_r = self.r_orbit(current_phi)
            r_list.append([current_r, current_phi])

        # if hyperbola or parabola (EPSILON = 1 or "..." > 1), shave off (default 10%) the longer r values
        start_percent_index = int(len(r_list) * percent)
        end_percent_index = int(len(r_list) - len(r_list) * percent)

        if self.EPSILON == 1:
            r_list.sort(key=lambda l:l[0]) # sort by the first value (r)
            r_list = r_list[:end_percent_index]
        elif self.EPSILON > 1:
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

            x_point_list.append(current_x)
            y_point_list.append(current_y)

        # get max in the list
        # find dividing factor that reduced it to the width of the screen (divided by 2)
        r_max = max([abs(elem[0]) for elem in r_list])
        factor = r_max / (self.WIDTH / 2)

        # graph each point
        for i in range(len(x_point_list)):
            current_x_coord = int((x_point_list[i] / factor) + self.WIDTH / 2)
            current_y_coord = int((y_point_list[i] / factor) + self.HEIGHT / 2)
            # plot point
            self.surface.set_at((current_x_coord, current_y_coord), self.WHITE)

        # draw the window and run the game loop
        # pygame.display.update()