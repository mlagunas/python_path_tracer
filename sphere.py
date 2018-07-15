from vec3 import Vec3
import numbers
import math


class Sphere(object):

    def __init__(self, center, radius):
        assert isinstance(radius, numbers.Number), 'radius must be a number'

        self.center = Vec3(center)
        self.radius = radius

    def ray_intersect(self, ray):
        ray_to_center = ray.origin - self.center

        first = Vec3.dot(ray.direction, ray.direction)
        second = 2. * Vec3.dot(ray.direction, ray_to_center)
        third = Vec3.dot(ray_to_center, ray_to_center) - self.radius ** 2

        discriminant = second ** 2 - 4 * first * third

        if discriminant < 0:
            return -1.
        else:
            return (-second - math.sqrt(discriminant)) / (2. * first)

    def get_normal(self, ray):
        t = self.ray_intersect(ray)
        if t > 0.:
            normal = (ray.point_at_parameter(t) - self.center).unit_vector()
            return 0.5 * normal.apply(lambda x: x + 1.)
        else:
            return None
