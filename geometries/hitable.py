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


from .aabb import sorrounding_box


class HitableList(Hitable):

    def __init__(self, hitable_array):

        self.hitable_array = hitable_array

    def hit(self, ray, t_min, t_max):
        hit_anything = False
        closest = t_max
        hit_record = None

        # hit every object in the array of objects
        for hitable in self.hitable_array:
            is_hit, new_hit_record = hitable.hit(ray, t_min, closest)
            if is_hit:
                hit_anything = True
                closest = new_hit_record.t
                hit_record = new_hit_record

        # return if something was hit
        return hit_anything, hit_record

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
            is_bbox, temp_bbox = self.hitable_array[i].bounding_box(t0, t1)
            if not is_bbox:
                return False, None
            bbox = sorrounding_box(bbox, temp_bbox)

        return True, bbox

    def __getitem__(self, index):
        return

    def __len__(self):
        return len(self.hitable_array)
