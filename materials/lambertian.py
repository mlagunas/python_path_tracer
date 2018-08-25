import numba as nb
import numpy as np

from core.ray import Ray
from core.vec_utils import random_in_unit_sphere
from .material import Material

# spec = [
#     ('albedo', nb.float64[:]),
#     ('scattered', Ray.class_type.instance_type),
#     ('attenuation', nb.float64[:]),
# ]


# @nb.jitclass(spec)
class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_record):
        target = hit_record.point + hit_record.normal + random_in_unit_sphere()
        self.scattered = Ray(hit_record.point, target - hit_record.point, ray.time)
        self.attenuation = self.albedo

        return True

    @staticmethod
    def reflect(ray_in, normal):
        return ray_in - 2 * np.dot(ray_in, normal) * normal
