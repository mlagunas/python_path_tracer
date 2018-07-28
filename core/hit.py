class HitPoint(object):
    def __init__(self, point, normal, material, t):
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material
