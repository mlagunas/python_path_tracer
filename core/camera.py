import math
from .ray import Ray
import numpy as np
from .vec_utils import unit_vector, random_in_unit_disk


class Camera(object):

    def __init__(self, lookfrom, lookat, vup, vertical_fov, aspect_ratio, aperture, focus_dist):
        theta = vertical_fov * math.pi / 180.  # vertical fov from degrees to radians
        half_height = math.tan(theta / 2.)  # get height of the camera
        half_width = aspect_ratio * half_height

        self.w = unit_vector(lookfrom - lookat)
        self.u = unit_vector(np.cross(vup, self.w))
        self.v = np.cross(self.w, self.u)

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
        random_lens_point = self.lens_radius * random_in_unit_disk()
        offset = self.u * random_lens_point[0] + self.v * random_lens_point[1]
        return Ray(origin=self.origin + offset,
                   direction=self.low_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)
