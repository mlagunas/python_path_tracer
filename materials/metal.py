from .material import Material
from core.ray import Ray
from core.vec3 import Vec3


class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in, hit_record):
        reflected = self.reflect(ray_in.direction.unit_vector(), hit_record['normal'])
        self.scattered = Ray(hit_record['point'], reflected)
        self.attenuation = self.albedo

        return Vec3.dot(self.scattered.direction, hit_record['normal']) > 0.

    @staticmethod
    def reflect(ray_in, normal):
        return ray_in - 2 * Vec3.dot(ray_in, normal) * normal
