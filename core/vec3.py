import numpy as np
import numbers
import random
import math


class Vec3(object):

    def __init__(self, x, y=None, z=None):
        if y is None and z is None:
            if isinstance(x, list) or isinstance(x, np.ndarray) or isinstance(x, tuple):
                assert len(x) == 3, 'list or np.array must have 3 elements'
                self.vec = np.array(x, dtype=np.float64)
            elif isinstance(x, numbers.Number):
                self.vec = np.array([x, x, x], dtype=np.float64)
            elif isinstance(x, Vec3):
                self.vec = x.vec
            else:
                raise ValueError(
                    'Vec3 can only by created by passing a 3 elements list or np.array or passing directly the three elements')
        elif x is not None and y is not None and z is not None:
            self.vec = np.array([x, y, z], dtype=np.float64)
        else:
            raise ValueError(
                'Vec3 can only by created by passing a 3 elements list or np.array or passing directly the three elements')

        self.dot = self._instance_dot
        self.cross = self._instance_cross
        self.sqrt = self._instance_sqrt

    def __getitem__(self, item):
        return self.vec[item]

    def x(self):
        return self.vec[0]

    def y(self):
        return self.vec[1]

    def z(self):
        return self.vec[2]

    def apply(self, f):
        # Apply a funcion to each element of vec
        return Vec3([f(x) for x in self.vec])

    def length(self):
        return np.sqrt(self.squared_length())

    def squared_length(self):
        return self.vec[0] ** 2 + self.vec[1] ** 2 + self.vec[2] ** 2

    def make_unit_vector(self):
        self.vec = self.unit_vector()

    def unit_vector(self):
        return Vec3(self.vec / self.length())

    def __add__(self, other):
        if isinstance(other, Vec3):  # if other is a vector
            return Vec3(self.vec + other.vec)
        elif isinstance(other, numbers.Number):  # if other is a number
            return Vec3(self.vec + other)

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.vec - other.vec)
        elif isinstance(other, numbers.Number):
            return Vec3(self.vec - other)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.vec * other.vec)
        elif isinstance(other, numbers.Number):
            return Vec3(self.vec * other)

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.vec / other.vec)
        elif isinstance(other, numbers.Number):
            return Vec3(self.vec / other)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self - other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self / other

    def __pos__(self):
        return Vec3(self.vec)

    def __neg__(self):
        return Vec3(-self.vec)

    def sqrt(self):
        return Vec3(np.sqrt(self.vec))

    def _instance_sqrt(vec3):
        return Vec3(np.sqrt(vec3.vec))

    @staticmethod
    def dot(vec_1, vec_2):
        return np.dot(vec_1.vec, vec_2.vec)

    def _instance_dot(self, other):
        return np.dot(self.vec, other.vec)

    @staticmethod
    def cross(vec1, vec2):
        return Vec3(np.cross(vec1.vec, vec2.vec))

    def _instance_cross(self, other):
        return Vec3(np.cross(self.vec, other.vec))

    @staticmethod
    def random_in_unit_sphere():
        p = 2. * Vec3(random.random(), random.random(), random.random()) - Vec3(1., 1., 1.)
        while (p.squared_length() >= 1.):
            p = 2. * Vec3(random.random(), random.random(), random.random()) - Vec3(1., 1., 1.)
        return p

    @staticmethod
    def random_in_unit_disk():
        p = 2. * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)
        while Vec3.dot(p, p) >= 1.:
            p = 2. * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)
        return p

    def reflect(ray_in, normal):
        return ray_in - 2 * Vec3.dot(ray_in, normal) * normal

    @staticmethod
    def refract(vec, normal, ni_over_nt):
        unit_v = vec.unit_vector()
        dt = Vec3.dot(unit_v, normal)
        discriminant = 1. - ni_over_nt ** 2 * (1 - dt ** 2)

        if discriminant > 0:
            refracted = ni_over_nt * (unit_v - normal * dt) - normal * math.sqrt(discriminant)
            return True, refracted
        return False, None

    def __str__(self):
        return 'Vec3: [%.3f, %.3f, %.3f]' % (self.vec[0], self.vec[1], self.vec[2])

    def __repr__(self):
        return 'Vec3: [%.3f, %.3f, %.3f]' % (self.vec[0], self.vec[1], self.vec[2])


def main():
    a = Vec3([1, 2, 3])
    b = Vec3([2, 4, 6])
    c = Vec3(1)
    print(c)
    print('a', a)
    print('b', b)
    print('add', a + b)
    print('sub', a - b)
    print('mul', a * b)
    print('div', a / b)
    print('constant mul', a * 2)
    print('reverse constant mul', 2 * a)
    print('neg', - b)
    print('pos', + b)
    print('unit length', a.length())

    print('dot', a.dot(b))
    print('cross', a.cross(b))

    a.make_unit_vector()
    print('unit ', a, a.length())

    print('iterate')
    for elem in a:
        print(elem)

    print([elem for elem in a])

    print('apply *2', a.apply(lambda x: x * 2))


if __name__ == '__main__':
    main()
