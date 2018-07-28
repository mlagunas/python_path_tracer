from .material import Material
from core.ray import Ray
from core.vec3 import Vec3


class Metal(Material):
    def __init__(self, albedo, fuzzy):
        self.albedo = Vec3(albedo)
        self.fuzzy = fuzzy

    def scatter(self, ray_in, hit_record):
        reflected = Vec3.reflect(ray_in.direction.unit_vector(), hit_record.normal)
        self.scattered = Ray(hit_record.point, reflected + self.fuzzy * Vec3.random_in_unit_sphere())
        self.attenuation = self.albedo

        return Vec3.dot(self.scattered.direction, hit_record.normal) > 0.
