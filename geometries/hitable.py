class Hitable(object):
    """
    Abstract class to define geometries that can be hit by a ray.

    It has the abstract method hit which has as input parameters the ray to intersect the given geometry,
    t_min and t_max as the bounds where the ray can be hit and hit_record which is a structure that keeps
    track of the objects that have been hit
    """

    def hit(self, ray, t_min, t_max, hit_record):
        raise NotImplementedError()


class HitableList(Hitable):

    def __init__(self, hitable_array):
        self.hitable_array = hitable_array

    def hit(self, ray, t_min, t_max):
        hit_anything = False
        closest = t_max

        for hitable in self.hitable_array:
            if hitable.hit(ray, t_min, closest):
                hit_anything = True
                closest = hitable.hit_record['t']
                self.hit_record = hitable.hit_record

        return hit_anything
