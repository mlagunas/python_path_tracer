class Hitable(object):
    """
    Abstract class to define geometries that can be hit by a ray.

    It has the abstract method hit which has as input parameters the ray to intersect the given geometry,
    t_min and t_max as the bounds where the ray can be hit and hit_record which is a structure that keeps
    track of the objects that have been hit
    """

    def hit(self, ray, t_min, t_max):
        raise NotImplementedError()

    def bounding_box(self, t0, t1):
        raise NotImplementedError()


from .aabb import AABB


class HitableList(Hitable):

    def __init__(self, hitable_array):

        self.hitable_array = hitable_array

    def hit(self, ray, t_min, t_max):
        hit_anything = False
        closest = t_max

        # hit every object in the array of objects
        for hitable in self.hitable_array:
            if hitable.hit(ray, t_min, closest):
                hit_anything = True
                closest = hitable.hit_record.t
                self.hit_record = hitable.hit_record

        # return if something was hit
        return hit_anything

    def bounding_box(self, t0, t1):

        # there is nothing to hit
        if len(self.hitable_array < 1):
            return False

        # get bounding box of the first object
        is_bbox, bbox = self.hitable_array[0].bounding_box(t0, t1)
        if not is_bbox:
            return False, None

        # get subsequent sorrounding boxes for all the other objects in the array
        for i in range(1, len(self.hitable_array)):
            is_bbox, temp_bbox = self.hitable_array[0].bounding_box(t0, t1)
            if not is_bbox:
                return False, None
            bbox = AABB.sorrounding_box(bbox, temp_bbox)

        return True, bbox

    def __getitem__(self, index):
        return

    def __len__(self):
        return len(self.hitable_array)
