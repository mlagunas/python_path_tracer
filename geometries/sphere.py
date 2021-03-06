import math

import numba as nb
import numpy as np

from core import HitPoint
from geometries import AABB, sorrounding_box
from .hitable import Hitable
from materials import Material

spec = [
    ('center', nb.float64[:]),
    ('radius', nb.float64),
    # ('material', Material.class_type.instance_type),
]

class Sphere(Hitable):

    def __init__(self, center, radius, material):
        self.center = np.array(center, dtype=np.float64)
        self.radius = float(radius)
        self.material = material

    def hit(self, ray, t_min, t_max):
        ray_to_center = ray.origin - self.center

        first = np.dot(ray.direction, ray.direction)
        second = np.dot(ray.direction, ray_to_center)
        third = np.dot(ray_to_center, ray_to_center) - self.radius ** 2

        discriminant = second ** 2 - first * third

        if discriminant > 0.:
            temp = (-second - math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center) / self.radius,
                    material=self.material)
                return True, hit_record

            temp = (-second + math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center) / self.radius,
                    material=self.material)
                return True, hit_record
        return False, None

    def bounding_box(self, t0, t1):
        return True, AABB(self.center - self.radius, self.center + self.radius)

    def get_normal(self, ray):
        t = self.ray_intersect(ray)
        if t > 0.:
            normal = (ray.point_at_parameter(t) - self.center).unit_vector()
            return 0.5 * (normal + 1.)
        else:
            return None


class MovingSphere(Sphere):

    def __init__(self, radius, material, center0, center1, time0, time1):

        self.radius = radius
        self.material = material
        self.center0 = center0
        self.center1 = center1
        self.time0 = time0
        self.time1 = time1

    def center(self, time):
        return self.center0 + ((time - self.time0) / (self.time1 - self.time0)) * (self.center1 - self.center0)

    def hit(self, ray, t_min, t_max):
        ray_to_center = ray.origin - self.center(ray.time)

        first = np.dot(ray.direction, ray.direction)
        second = np.dot(ray.direction, ray_to_center)
        third = np.dot(ray_to_center, ray_to_center) - self.radius ** 2

        discriminant = second ** 2 - first * third

        if discriminant > 0:
            temp = (-second - math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center(ray.time)) / self.radius,
                    material=self.material)
                return True, hit_record

            temp = (-second + math.sqrt(discriminant)) / first
            if temp < t_max and temp > t_min:
                point = ray.point_at_parameter(temp)
                hit_record = HitPoint(
                    t=temp,
                    point=point,
                    normal=(point - self.center(ray.time)) / self.radius,
                    material=self.material)
                return True, hit_record
        return False, None

    def bounding_box(self, t0, t1):
        bounding_box_t0 = AABB(self.center(self.time0) - self.radius, self.center(self.time0) + self.radius)
        bounding_box_t1 = AABB(self.center(self.time1) - self.radius, self.center(self.time1) + self.radius)
        return True, sorrounding_box(bounding_box_t0, bounding_box_t1)

    def get_normal(self, ray):
        t = self.ray_intersect(ray)
        if t > 0:
            normal = (ray.point_at_parameter(t) - self.center(ray.time)).unit_vector()
            return 0.5 * (normal + 1.)
        else:
            return None
