import numba as nb
import numpy as np

from .hitable import Hitable

spec = [
    ('min', nb.typeof((np.empty(3)))),  # a float field
    ('max', nb.typeof((np.empty(3)))),  # a float field
]


@nb.jit()
def ffmin(a, b):
    return np.where(a < b, a, b)


@nb.jit()
def ffmax(a, b):
    return np.where(a > b, a, b)


@nb.jit()
def sorrounding_box(box0, box1):
    return AABB(ffmin(box0.min, box1.min), ffmax(box0.max, box1.max))


# @nb.jitclass(spec)
class AABB(Hitable):
    """
    Axis-Aligned Bounding Box (AABB)


        |     |
    -------------- b_0
        |*****|
        |*****|
    -------------- b_1
        |     |
        a_0   a_1

    """

    def __init__(self, min, max):
        self.max = max
        self.min = min

    def hit(self, ray, t_min, t_max):
        a = (self.min - ray.origin) / ray.direction
        b = (self.max - ray.origin) / ray.direction
        t0 = ffmin(a, b)
        t1 = ffmax(a, b)

        t_min = ffmax(t0, t_min)
        t_max = ffmin(t1, t_max)

        if np.any(t_max <= t_min):
            return False, None

        return True, None
