from .material import Material
from core.ray import Ray
from core.vec_utils import random_in_unit_sphere
import numpy as np


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in, hit_record):
        target = hit_record.point + hit_record.normal + random_in_unit_sphere()
        self.scattered = Ray(hit_record.point, target - hit_record.point)
        self.attenuation = self.albedo

        return True

    @staticmethod
    def reflect(ray_in, normal):
        return ray_in - 2 * np.dot(ray_in, normal) * normal
