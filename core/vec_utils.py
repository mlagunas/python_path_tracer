import numpy as np
from numpy import linalg as LA
import random

rnd = random.random


def _random_in_shpere():
    """
    helper funtion to create a random array with three elements
    """
    return np.array([rnd(), rnd(), rnd()])


def random_in_unit_sphere():
    """
    helper funtion to create a random array with three elements but the last one is zero
    """
    p = 2. * _random_in_shpere() - np.ones(3)
    while (squared_length(p) >= 1.):
        p = 2. * _random_in_shpere() - np.ones(3)
    return p


def _random_in_disk():
    return np.array([rnd(), rnd(), 0])


def random_in_unit_disk():
    p = 2. * _random_in_disk() - np.array([1, 1, 0])
    while np.dot(p, p) >= 1.:
        p = 2. * _random_in_disk() - np.array([1, 1, 0])
    return p


def length(array):
    return LA.norm(array)


def squared_length(array):
    return LA.norm(array) ** 2


def unit_vector(array):
    return array / LA.norm(array)
