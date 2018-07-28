import math
from .ray import Ray
from .vec3 import Vec3


class Camera(object):

    def __init__(self, lookfrom, lookat, vup, vertical_fov, aspect_ratio, aperture, focus_dist):
        assert isinstance(lookfrom, Vec3), 'lookfrom must be Vec3 type'
        assert isinstance(lookat, Vec3), 'lookat must be Vec3 type'
        assert isinstance(vup, Vec3), 'vup must be Vec3 type'

        theta = vertical_fov * math.pi / 180.  # vertical fov from degrees to radians
        half_height = math.tan(theta / 2.)  # get height of the camera
        half_width = aspect_ratio * half_height

        self.w = Vec3.unit_vector(lookfrom - lookat)
        self.u = Vec3.unit_vector(Vec3.cross(vup, self.w))
        self.v = Vec3.cross(self.w, self.u)

        # get canvas low left corner
        self.low_left_corner = lookfrom - half_width * focus_dist * self.u - \
                               half_height * focus_dist * self.v - self.w * focus_dist

        # get camera origin
        self.origin = lookfrom

        # get lens radius
        self.lens_radius = aperture / 2

        # step to take on the horizontal and vertical direction
        self.horizontal = 2 * half_width * self.u * focus_dist
        self.vertical = 2 * half_height * self.v * focus_dist

    def get_ray(self, s, t):
        random_lens_point = self.lens_radius * Vec3.random_in_unit_disk()
        offset = self.u * random_lens_point.x() + self.v * random_lens_point.y()
        return Ray(origin=self.origin + offset,
                   direction=self.low_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)
