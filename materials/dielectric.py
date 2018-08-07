import math
import random
from core import Ray
from core.vec_utils import length
from materials import Material
from .utils import reflect, refract
import numpy as np


class Dielectric(Material):

    def __init__(self, refraction_index):
        self.refraction_index = refraction_index
        self.attenuation = np.ones(1)

    def scatter(self, ray, hit_record):
        reflected = reflect(ray.direction, hit_record.normal)

        # If the ray is inside the sphere set values accordingly
        if np.dot(ray.direction, hit_record.normal) > 0.:
            outward_normal = -hit_record.normal
            ni_over_nt = self.refraction_index
            cosine = self.refraction_index * np.dot(ray.direction, hit_record.normal) / length(ray.direction)
        else:
            outward_normal = hit_record.normal
            ni_over_nt = 1. / self.refraction_index
            cosine = -np.dot(ray.direction, hit_record.normal) / length(ray.direction)

        is_refracted, refracted = refract(ray.direction, outward_normal, ni_over_nt)

        # get probability of reflection over refraction with schlick approximation
        reflect_prob = self._schlick(cosine) if is_refracted else 1

        # set the scattered ray as either the reflection or refraction according to reflect_prob
        if random.random() < reflect_prob:
            self.scattered = Ray(hit_record.point, reflected, ray.time)
        else:
            self.scattered = Ray(hit_record.point, refracted, ray.time)

        return True

    def _schlick(self, cosine):
        """
        Schlick approximation
        :param cosine:
        :return:
        """
        r0 = (1 - self.refraction_index) / (1 + self.refraction_index)
        r0 *= r0
        return r0 + (1 - r0) * math.pow(1 - cosine, 5)
