from vec3 import Vec3


def vec3_type_error(var, name='A'):
    assert isinstance(var, Vec3), 'Variable ' + name + ' must be Vec3 class, now ' + type(var)


class Ray(object):

    def __init__(self, A, B):
        # Consider the ray as p(t) = A + t*B
        vec3_type_error(A)
        vec3_type_error(B)

        self.A = A
        self.B = B

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_parameter(self, t):
        return self.A + t * self.B
