from .ray import Ray


class Camera(object):

    def __init__(self, origin, horizontal, vertical, low_left_corner):
        # camera origin
        self.origin = origin

        # step to take on the horizontal and vertical direction
        self.horizontal = horizontal
        self.vertical = vertical

        # position of the lower-left corner of the canvas
        self.low_left_corner = low_left_corner

    def get_ray(self, u, v):
        return Ray(self.origin, self.low_left_corner + u * self.horizontal + v * self.vertical - self.origin)
