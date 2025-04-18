import pygame
from pygame.locals import *

"""INITIATE PYGAME
(https://inventwithpython.com/pygameHelloWorld.py)
"""
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Orbit Graph")

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()