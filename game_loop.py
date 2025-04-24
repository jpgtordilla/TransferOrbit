"""SOURCES
1. https://inventwithpython.com/pygameHelloWorld.py
2. Taylor, John R. Classical Mechanics. University Science Books, 2005.
"""
import time

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
from pygame_widgets.button import Button

pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

"""MAIN LOOP FOR DRAWING ORBITS AND UPDATING"""

class Game:
    def __init__(self):
        self.factor = 1 # set default factor

    def graph_orbits(self, orbit_list, draw_surface, num_points=300, visible=True):
        """Given a list of orbit objects, plot them on the screen"""

        """OLD SCALING BASED ON MAX RADIUS
        # max_radius = get_max_radius(orbit_list)
        # print(max_radius)
        """

        # calculate scaling factor based on the max orbit
        self.factor = RADIUS / (WIDTH / SCALING_CONST) # slightly more than 2 so that there are margins

        # plot each trajectory, scaling w.r.t. the factor
        for orbit in orbit_list:
            curr_points_list = orbit.get_orbit_points(num_points)
            for point in curr_points_list:
                x = int((point[0] / self.factor) + WIDTH / 2)
                y = int((point[1] / self.factor) + HEIGHT / 2.5)
                if visible and y < GUI_Y - 1: # extra -1 to prevent drawing on GUI region with excess pixels
                    draw_surface.set_at((x, y), WHITE)

    def change_velocity(self, circle, slider):
        # change velocity of circular satellite by velocity slider
        # - Note: L = r m v --> v = L / r m
        v_init = circle.get_l() / (circle.r_orbit(0) * circle.M2)
        v_delta = slider.getValue()  # -1 -> 1 scale in terms of percentage decrease -> increase

        v_new = v_init + v_init * v_delta
        l_new = circle.r_orbit(0) * circle.M2 * v_new
        c_new = l_new ** 2 / (circle.GAMMA * circle.MU)

        circle.set_l(l_new)
        circle.set_c(c_new)

    def game_loop(self):
        """
        parabola = Orbit(epsilon=1)  # parabola
        parabola_neg = Orbit(epsilon=-1)  # parabola negative
        hyperbola = Orbit(epsilon=1.9)  # hyperbola
        hyperbola_neg = Orbit(epsilon=-1.9)  # hyperbola negative
        """
        esc = False # escape set to false until window is closed

        # create orbit objects
        circle = Orbit(epsilon=0)  # circle
        ellipse = Orbit(epsilon=0.3)  # ellipse

        # graph the orbits based on the largest orbit's scaling factor
        orbits = [circle, ellipse]
        self.graph_orbits(orbits, surface, visible=False)

        # create satellite objects
        sat_circle = Satellite(circle, self.factor)
        sat_ellipse = Satellite(ellipse, self.factor)

        # GUI sliders
        surface.fill(BLUE) # GUI background
        # ellipse eccentricity slider
        eccentricity_slider = Slider(surface, int(WIDTH / 2 - SLIDER_WIDTH / 2), int(GUI_Y + SLIDER_HEIGHT),
                                     SLIDER_WIDTH, SLIDER_HEIGHT,
                                     min=-1.9, max=1.9, initial=0, step=0.01, colour=BLACK, handleColour=LIGHT_BLUE)
        # delta velocity slider
        velocity_slider = Slider(surface, int(WIDTH / 2 - SLIDER_WIDTH / 2), int(GUI_Y + 3 * SLIDER_HEIGHT),
                                 SLIDER_WIDTH, SLIDER_HEIGHT,
                                 min=-0.2, max=0.2, initial=0.0, step=0.001, colour=BLACK, handleColour=LIGHT_BLUE)
        # velocity button
        button = Button(surface, int(WIDTH / 2 - BUTTON_WIDTH / 2), int(GUI_Y + 4.5 * SLIDER_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT,
                        text='change vel', fontSize=20, margin=20, inactiveColour=(200, 50, 0),
                        pressedColour=(0, 200, 20), radius=20,
                        onClick=lambda: self.change_velocity(circle, velocity_slider))

        clock = pygame.time.Clock() # for frame rate
        while not esc:
            clock.tick(FPS)

            pygame.draw.rect(surface, BLACK,(0, 0, WIDTH, GUI_Y)) # background

            self.graph_orbits(orbits, surface) # redraw orbit

            # draw satellite
            sat_circle.draw_satellite(surface)
            sat_ellipse.draw_satellite(surface)

            pygame.display.update()

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    esc = True
                    pygame.quit()

            # update the slider values
            surface.fill(BLUE)  # GUI background
            # eccentricity slider
            ellipse.set_epsilon(eccentricity_slider.getValue())

            # update satellite position
            sat_circle.update_satellite()
            sat_ellipse.update_satellite()

            pygame_widgets.update(events)

"""IDEAS: 
- execute a transfer orbit by instantaneously changing velocity
- second slider and button to control delta velocity
"""