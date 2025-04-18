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
import sys

import numpy as np
import pygame
from pygame.locals import *

"""CONSTANTS"""
G = 6.67430 * 10**-11 # gravitational const.
M1 = 5.97219*10**24 # mass of Earth
M2 = 10**13 # mass of a typical comet
GAMMA = G * M1 * M2
MU = (M1 * M2) / (M1 + M2)

"""CONSTANTS that should be CHANGED for experimentation"""
L = 10**24 # angular momentum
EPSILON = 0.9 # circle
C = L**2 / (GAMMA * MU)

"""INITIATE PYGAME
(https://inventwithpython.com/pygameHelloWorld.py)
"""
WIDTH = 500
HEIGHT = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")
surface.fill(BLACK)

def r_orbit(phi):
    return C/(1 + EPSILON * np.cos(phi))

def energy():
    return GAMMA ** 2 * MU * (EPSILON ** 2 - 1) / 2 * L ** 2

def graph_orbits(num_points=3000, percent=10):
    # energy and orbit information
    print(f"Energy: {energy()}")
    print(f"Orbit for 0 phi: {r_orbit(0)}")
    print(f"Orbit for 3PI/2 phi: {r_orbit(3 * np.pi / 2)}")

    # graph orbit
    # - for (default=360) equally spaced points, calculate r and add to 2D list
    # - graph each point in each array (x and y)
    r_list = []
    x_point_list = []
    y_point_list = []

    current_phi = 0

    # get the points and add to array
    for i in range (num_points):
        radian_increment = 2*np.pi / num_points
        current_phi += radian_increment
        current_r = r_orbit(current_phi)
        r_list.append(current_r)

    # if hyperbola or parabola (EPSILON = 1 or "..." > 1), shave off (default 10%) the longer r values
    if EPSILON == 1 or EPSILON > 1:
        percent_index = int(len(r_list) - len(r_list) / percent)
        """
        # sort by absolute value, but don't actually change signs
        r_list.sort(key=abs)
        # r_list = r_list[:percent_index]
        """

    current_phi = 0 # reset to zero

    for i in range(len(r_list)):
        radian_increment = 2 * np.pi / num_points
        current_phi += radian_increment
        current_r = r_list[i]
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

    """
    x_max = max([abs(elem) for elem in x_point_list])
    y_max = max([abs(elem) for elem in y_point_list])
    x_factor = x_max / (WIDTH / 2)
    y_factor = y_max / (HEIGHT / 2)
    """

    r_max = max([abs(elem) for elem in r_list])
    factor = r_max / (WIDTH / 2)

    # graph each point
    for i in range(len(x_point_list)):
        current_x_coord = int((x_point_list[i] / factor) + WIDTH / 2)
        current_y_coord = int((y_point_list[i] / factor) + HEIGHT / 2)
        # plot point
        surface.set_at((current_x_coord, current_y_coord), WHITE)

    # draw the window and run the game loop
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

"""
NOTES: 
- Plots too many extreme points for parabolas and hyperbolas
- flickering effect due to loop condition
"""