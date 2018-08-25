import numba as nb

spec = []


# @nb.jitclass(spec)
class Material(object):
    def __init__(self):
        pass

    def scatter(self, ray_in, hit_record):
        raise NotImplementedError()
