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
import pygame
from pygame.locals import *
from orbit import *
from satellite import Satellite
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

"""MAIN LOOP FOR DRAWING ORBITS AND UPDATING"""

class Game:
    def __init__(self):
        self.factor = 1 # set default factor

    def graph_orbits(self, orbit_list, draw_surface, num_points=300, visible=True):
        """Given a list of orbit objects, plot them on the screen"""

        max_radius = get_max_radius(orbit_list)

        # calculate scaling factor based on the max orbit
        self.factor = max_radius / (WIDTH / SCALING_CONST) # slightly more than 2 so that there are margins

        # plot each trajectory, scaling w.r.t. the factor
        for orbit in orbit_list:
            curr_points_list = orbit.get_orbit(num_points)
            for point in curr_points_list:
                x = int((point[0] / self.factor) + WIDTH / 2)
                y = int((point[1] / self.factor) + HEIGHT / 2.5)
                if visible and y < GUI_Y - 1: # extra -1 to prevent drawing on GUI region with excess pixels
                    draw_surface.set_at((x, y), WHITE)

    def game_loop(self):
        """
        parabola = Orbit(epsilon=1)  # parabola
        parabola_neg = Orbit(epsilon=-1)  # parabola negative
        hyperbola = Orbit(epsilon=1.9)  # hyperbola
        hyperbola_neg = Orbit(epsilon=-1.9)  # hyperbola negative
        """
        esc = False # escape set to false until window is closed

        # create orbit objects
        parabola = Orbit(epsilon=1, l=0.8*10**24)  # parabola
        circle = Orbit(epsilon=0)  # circle
        hyperbola = Orbit(epsilon=1.7, l=0.8 * 10 ** 24)  # hyperbola
        ellipse = Orbit(epsilon=0.3)  # ellipse

        # graph the orbits based on the largest orbit's scaling factor
        orbits = [circle, parabola, hyperbola, ellipse]
        self.graph_orbits(orbits, surface, visible=False)

        # create satellite objects
        sat_circle = Satellite(circle, self.factor)
        sat_parabola = Satellite(parabola, self.factor)
        sat_hyperbola = Satellite(hyperbola, self.factor)
        sat_ellipse = Satellite(ellipse, self.factor)

        # GUI sliders
        surface.fill(BLUE) # GUI background
        slider = Slider(surface, int(WIDTH / 2 - SLIDER_WIDTH / 2), int(GUI_Y + SLIDER_HEIGHT), SLIDER_WIDTH, SLIDER_HEIGHT,
                        min=0, max=0.9, initial=0, step=0.01, colour=BLACK, handleColour=LIGHT_BLUE)

        clock = pygame.time.Clock() # for frame rate
        while not esc:
            clock.tick(FPS)

            pygame.draw.rect(surface, BLACK,(0, 0, WIDTH, GUI_Y)) # background

            self.graph_orbits(orbits, surface) # redraw orbit

            # draw satellite
            sat_circle.draw_satellite(surface)
            sat_parabola.draw_satellite(surface)
            sat_hyperbola.draw_satellite(surface)
            sat_ellipse.draw_satellite(surface)

            pygame.display.update()

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    esc = True
                    pygame.quit()

            # update satellite position
            sat_circle.update_satellite()
            sat_parabola.update_satellite()
            sat_hyperbola.update_satellite()
            sat_ellipse.update_satellite()

            # update the slider value
            surface.fill(BLUE)  # GUI background
            ellipse.set_epsilon(slider.getValue())
            pygame_widgets.update(events)

"""TODO: 
- create slider to change epsilon between specific values (orbit.py update_epsilon)
"""