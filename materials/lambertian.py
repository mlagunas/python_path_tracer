from .material import Material
from core.ray import Ray
from core.vec3 import Vec3


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = Vec3(albedo)

    def scatter(self, ray_in, hit_record):
        target = hit_record.point + hit_record.normal + Vec3.random_in_unit_sphere()
        self.scattered = Ray(hit_record.point, target - hit_record.point)
        self.attenuation = self.albedo

        return True

    @staticmethod
    def reflect(ray_in, normal):
        return ray_in - 2 * Vec3.dot(ray_in, normal) * normal
