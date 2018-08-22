from .hitable import Hitable
import numpy as np


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
        t0 = np.minimum(a, b)
        t1 = np.maximum(a, b)

        t_min = np.maximum(t0, t_min)
        t_max = np.minimum(t1, t_max)

        if np.any(t_max <= t_min):
            return False

        return True

    @staticmethod
    def ffmin(a, b):
        return np.mi(a < b, a, b)

    @staticmethod
    def ffmax(a, b):
        return np.where(a > b, a, b)

    @staticmethod
    def sorrounding_box(box0, box1):
        return AABB(np.minimum(box0.min, box1.min), np.maximum(box0.max, box1.max))
