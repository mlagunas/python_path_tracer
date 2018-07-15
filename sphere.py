from vec3 import Vec3
import numbers


class Sphere(object):

    def __init__(self, center, radius):
        assert isinstance(radius, numbers.Number), 'radius must be a number'

        self.center = Vec3(center)
        self.radius = radius

    def ray_intersect(self, ray):
        ray_to_center = ray.origin() - self.center

        first = ray.direction().dot(ray.direction())
        second = 2. * ray.direction().dot(ray_to_center)
        third = ray_to_center.dot(ray_to_center) - self.radius ** 2
        discriminant = second ** 2 - 4 * first * third

        return discriminant > 0
