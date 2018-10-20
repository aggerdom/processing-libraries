from math import sin, cos, sqrt
from operator import add, mul


def circle_coord(h, k, r, t):
    """
    :param h: x-coordinate of center
    :param k: y-coordinate of center
    :param r: Radius of circle
    :param t: Angle in radians
    """
    x = r * cos(t) + h
    y = r * sin(t) + k
    return (x, y)


def slope(p, q):
    return (p[1] - q[1]) / (p[0] - q[0])


def colinear(a, b, c):
    return slope(a, b) == slope(b, c) == slope(a, c)


def dot(p, q):
    return sum(map(mul, zip(p, q)))


def opp_reciprocal(m):
    return -1 / m


def magnitude(p):
    return sqrt(sum(map(lambda x: x ** 2, p)))


def normalized_unit_vector(p, q):
    """Given two vectors, p and q, that define a line,
    convert them to a normalized unit vector."""
    x1, y1 = p
    x2, y2 = q

    # Get component differences
    dx = x2 - x1
    dy = y2 - y1
    # Calculate the length of the components
    mag = magnitude((dx, dy))
    dx /= mag
    dy /= mag
    return dx, dy


def minkowski_distance(order):
    """
    Construct distance functions using Minkowski metric of a given order

    :param p: Order of Minkowski function
    :return: Distance function
    """
    power = 1.0 / order

    def distance(p, q):
        return (sum(abs(p_i - q_i) ** order for p_i, q_i in zip(p, q))) ** power

    return distance


d_manhattan = minkowski_distance(1.0)
d_euclidian = minkowski_distance(2.0)
d_chebyshev = minkowski_distance(13.0)  # Should be sufficient
