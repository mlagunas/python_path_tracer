import numba as nb
import numpy as np

from core.ray import Ray
from core.vec_utils import random_in_unit_sphere, unit_vector
from .material import Material
from .utils import reflect

# spec = [
#     ('albedo', nb.float64[:]),
#     ('fuzzy', nb.float64),
#     ('scattered', Ray.class_type.instance_type),
#     ('attenuation', nb.float64[:]),
# ]


# @nb.jitclass(spec)
class Metal(Material):
    def __init__(self, albedo, fuzzy):
        self.albedo = np.array(albedo)
        self.fuzzy = fuzzy

    def scatter(self, ray, hit_record):
        reflected = reflect(unit_vector(ray.direction), hit_record.normal)
        self.scattered = Ray(hit_record.point, reflected + self.fuzzy * random_in_unit_sphere(), ray.time)
        self.attenuation = self.albedo

        return np.dot(self.scattered.direction, hit_record.normal) > 0.
