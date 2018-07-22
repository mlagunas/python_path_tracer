from core.vec3 import Vec3


def vec3_type_error(var, name='A'):
    assert isinstance(var, Vec3), 'Variable ' + name + ' must be Vec3 class, now ' + type(var)


class Ray(object):

    def __init__(self, origin, direction):
        # Consider the ray as p(t) = A + t*B
        vec3_type_error(origin)
        vec3_type_error(direction)

        self.origin = origin
        self.direction = direction

    def point_at_parameter(self, t):
        return self.origin + t * self.direction
