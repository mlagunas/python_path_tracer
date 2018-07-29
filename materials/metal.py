from .material import Material
from core.ray import Ray
from .utils import reflect
from core.vec_utils import random_in_unit_sphere, unit_vector
import numpy as np


class Metal(Material):
    def __init__(self, albedo, fuzzy):
        self.albedo = np.array(albedo)
        self.fuzzy = fuzzy

    def scatter(self, ray_in, hit_record):
        reflected = reflect(unit_vector(ray_in.direction), hit_record.normal)
        self.scattered = Ray(hit_record.point, reflected + self.fuzzy * random_in_unit_sphere())
        self.attenuation = self.albedo

        return np.dot(self.scattered.direction, hit_record.normal) > 0.
