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
from constants import *
import pygame
from pygame.locals import *
from orbit import Orbit, get_max_radius

pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

def graph_orbits(orbit_list, num_points=300):
    """Given a list of orbit objects, plot them on the screen"""

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

"""MAIN LOOP FOR DRAWING ORBITS AND UPDATING"""

def game_loop():
    """
    parabola = Orbit(epsilon=1)  # parabola
    parabola_neg = Orbit(epsilon=-1)  # parabola negative
    hyperbola = Orbit(epsilon=1.9)  # hyperbola
    hyperbola_neg = Orbit(epsilon=-1.9)  # hyperbola negative
    """
    esc = False # escape set to false until window is closed

    circle = Orbit(epsilon=0)  # circle
    circle_small = Orbit(epsilon=0, l=0.8*10**24)  # small circle

    orbits = [circle, circle_small]
    graph_orbits(orbits)

    clock = pygame.time.Clock() # for frame rate
    while not esc:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                esc = True
                pygame.quit()
