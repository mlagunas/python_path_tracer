import math
import numpy as np
from core.vec_utils import unit_vector


def reflect(ray_in, normal):
    return ray_in - 2 * np.dot(ray_in, normal) * normal


def refract(vec, normal, ni_over_nt):
    unit_v = unit_vector(vec)
    dt = np.dot(unit_v, normal)
    discriminant = 1. - ni_over_nt ** 2 * (1 - dt ** 2)

    if discriminant > 0:
        refracted = ni_over_nt * (unit_v - normal * dt) - normal * math.sqrt(discriminant)
        return True, refracted
    return False, None
