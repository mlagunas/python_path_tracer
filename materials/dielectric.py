import math
import random
from core import Vec3, Ray
from materials import Material


class Dielectric(Material):

    def __init__(self, refraction_index):
        self.refraction_index = refraction_index
        self.attenuation = Vec3(1., 1., 1.)

    def scatter(self, ray_in, hit_record):
        reflected = Vec3.reflect(ray_in.direction, hit_record.normal)

        # If the ray is inside the sphere set values accordingly
        if Vec3.dot(ray_in.direction, hit_record.normal) > 0.:
            outward_normal = -hit_record.normal
            ni_over_nt = self.refraction_index
            cosine = self.refraction_index * Vec3.dot(ray_in.direction, hit_record.normal) / ray_in.direction.length()
        else:
            outward_normal = hit_record.normal
            ni_over_nt = 1. / self.refraction_index
            cosine = -Vec3.dot(ray_in.direction, hit_record.normal) / ray_in.direction.length()

        is_refracted, refracted = Vec3.refract(ray_in.direction, outward_normal, ni_over_nt)

        # get probability of reflection over refraction with schlick approximation
        reflect_prob = self._schlick(cosine) if is_refracted else 1

        # set the scattered ray as either the reflection or refraction according to reflect_prob
        if random.random() < reflect_prob:
            self.scattered = Ray(hit_record.point, reflected)
        else:
            self.scattered = Ray(hit_record.point, refracted)

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
