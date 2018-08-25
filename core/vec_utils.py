import random

import numba as nb
import numpy as np
from numpy import linalg as LA

rnd = random.random


@nb.jit()
def _random_in_shpere():
    """
    helper funtion to create a random array with three elements
    """
    return np.array([rnd(), rnd(), rnd()])


@nb.jit()
def random_in_unit_sphere():
    """
    helper funtion to create a random array with three elements but the last one is zero
    """
    p = 2. * _random_in_shpere() - np.ones(3)
    while (squared_length(p) >= 1.):
        p = 2. * _random_in_shpere() - np.ones(3)
    return p


@nb.jit()
def _random_in_disk():
    return np.array([rnd(), rnd(), 0])


@nb.jit()
def random_in_unit_disk():
    p = 2. * _random_in_disk() - np.array([1, 1, 0])
    while np.dot(p, p) >= 1.:
        p = 2. * _random_in_disk() - np.array([1, 1, 0])
    return p


@nb.jit()
def length(array):
    return LA.norm(array)


@nb.jit()
def squared_length(array):
    return LA.norm(array) ** 2


@nb.jit()
def unit_vector(array):
    return array / LA.norm(array)


@nb.jit()
def cross(array1, array2):
    return np.array([array1[1] * array2[2] - array1[2] * array2[1],
                     array1[2] * array2[0] - array1[0] * array2[2],
                     array1[0] * array2[1] - array1[1] * array2[0]], dtype=np.float64)
