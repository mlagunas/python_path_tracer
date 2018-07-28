from core.vec3 import Vec3
import numbers
import math
from .hitable import Hitable
from core import HitPoint


class Sphere(Hitable):

    def __init__(self, center, radius, material):
        assert isinstance(radius, numbers.Number), 'radius must be a number'

        self.center = Vec3(center)
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max):
        ray_to_center = ray.origin - self.center

        first = Vec3.dot(ray.direction, ray.direction)
        second = Vec3.dot(ray.direction, ray_to_center)
        third = Vec3.dot(ray_to_center, ray_to_center) - self.radius ** 2

        discriminant = second ** 2 - first * third

        if discriminant > 0.:
            temp = (-second - math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                self.hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center) / self.radius,
                    material=self.material)
                return True

            temp = (-second + math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                self.hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center) / self.radius,
                    material=self.material)
                return True
        return False

    def get_normal(self, ray):
        t = self.ray_intersect(ray)
        if t > 0.:
            normal = (ray.point_at_parameter(t) - self.center).unit_vector()
            return 0.5 * normal.apply(lambda x: x + 1.)
        else:
            return None
