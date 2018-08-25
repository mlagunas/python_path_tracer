import functools
import random

import numba as nb

from geometries import Hitable, sorrounding_box

rint = random.randint

nb.jit()


def compare_bbox(axis=0):
    def compare(hitable0, hitable1):
        # get boundoing boxes for both hitable items
        is_bbox0, bbox_0 = hitable0.bounding_box(0, 0)
        is_bbox1, bbox_1 = hitable1.bounding_box(0, 0)

        # check if they exist
        if not is_bbox0 or not is_bbox1:
            raise Exception('No bounding box in BVHnode constructor')

        # return -1 if the right is bigger than the left, 1 if the opposite and 0 if they are equal
        if (bbox_0.min[axis] - bbox_1.min[axis]) < 0:
            return -1
        elif (bbox_0.min[axis] - bbox_1.min)[axis] > 0:
            return 1
        else:
            return 0

    return compare


class BVH_node(Hitable):
    def __init__(self, hitable_list, time0, time1):

        n = len(hitable_list)
        axis = rint(0, 2)
        sorted(hitable_list, key=functools.cmp_to_key(compare_bbox(axis)))

        if n == 1:  # case of single item in the hitable list
            self.left = self.right = hitable_list[0]

        elif n == 2:  # case of two items in the hitable list
            self.left, self.right = hitable_list[0], hitable_list[1]

        else:
            self.left = BVH_node(hitable_list[:n // 2], time0, time1)
            self.right = BVH_node(hitable_list[n // 2:], time0, time1)

        is_left_bbox, left_bbox = self.left.bounding_box(time0, time1)
        is_right_bbox, right_bbox = self.right.bounding_box(time0, time1)

        if not is_left_bbox or not is_right_bbox:
            raise Exception('No bbox in BVH_node constructor')

        self.bbox = sorrounding_box(left_bbox, right_bbox)

    def hit(self, ray, t_min, t_max):
        if self.bbox.hit(ray, t_min, t_max):

            # hit the left branch
            left_hit, left_record = self.left.hit(ray, t_min, t_max)
            if left_hit:
                record = left_record  # set the record to the record of the item hit
                t_max = left_record.t  # update maximum hit distance

            # hit the right branch with the updated distance, if there is a hit, it means that
            # it occured before the left hit
            right_hit, right_record = self.right.hit(ray, t_min, t_max)
            if right_hit:
                record = right_record

            # if there was a hit, return it
            if left_hit or right_hit:
                return True, record

        # if nothing was hit
        return False, None

    def bounding_box(self, t0, t1):
        return True, self.bbox
