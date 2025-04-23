"""SOURCES
1. https://inventwithpython.com/pygameHelloWorld.py
2. Taylor, John R. Classical Mechanics. University Science Books, 2005.
"""
from satellite import Satellite

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
import pygame
from pygame.locals import *
from orbit import *

pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

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
    graph_orbits(orbits, surface)

    # satellite test
    sat = Satellite(circle)

    clock = pygame.time.Clock() # for frame rate
    while not esc:
        clock.tick(FPS)
        sat.draw_satellite(surface)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                esc = True
                pygame.quit()
