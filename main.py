"""THEORY

General Kepler Orbit Equation:

r(phi) = c/(1 + epsilon * cos(phi))

- c and epsilon are constants

Energy of a comet/body:

E = gamma**2 * mu * (epsilon**2 - 1) / 2 * l**2

- l = const. angular momentum
- gamma = G * m1 * m2
- mu = l**2 / c * gamma

Key: eccentricity determines the orbit's shape:
- epsilon = 0     -- E < 0 -- circle
- 0 < epsilon < 1 -- E < 0 -- ellipse
- epsilon = 1     -- E = 0 -- parabola
- epsilon > 1     -- E > 0 -- hyperbola

"""
from graph_orbits import graph_orbits

if __name__ == '__main__':
    graph_orbits()