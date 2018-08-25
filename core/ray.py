import numba as nb

spec = [
    ('origin', nb.float64[:]),
    ('direction', nb.float64[:]),
    ('time', nb.float64),
]


@nb.jitclass(spec)
class Ray(object):

    def __init__(self, origin, direction, time):
        self.origin = origin
        self.direction = direction
        self.time = time

    def point_at_parameter(self, t):
        return self.origin + t * self.direction
