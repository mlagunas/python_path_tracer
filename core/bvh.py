from geometries import Hitable, AABB
import functools

import random

rint = random.randint


def compare_bbox(axis=0):
    def compare(hitable0, hitable1):
        # get boundoing boxes for both hitable items
        is_bbox0, bbox_0 = hitable0.bounding_box(0, 0)
        is_bbox1, bbox_1 = hitable1.bounding_box(0, 0)

        # check if they exist
        if not is_bbox0 or not is_bbox1:
            raise Exception('No bounding box in BVHnode constructor')

        # return -1 if the right is bigger than the left, 1 if the opposite and 0 if they are equal
        if bbox_0.min[axis] - bbox_1.min[axis] < 0:
            return -1
        elif bbox_0.min[axis] - bbox_1.min[axis]:
            return 1
        else:
            return 0

    return compare


class BVH_node(Hitable):
    def __init__(self, hitable_list, time0, time1):
        # self.hitable_list = hitable_list
        # self.time0 = time0
        # self.time1 = time1
        #
        # # tree structure
        # self.left = None
        # self.right = None
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

        self.bbox = AABB.sorrounding_box(left_bbox, right_bbox)

    def hit(self, ray, t_min, t_max):
        left_hit = self.left.hit(ray, t_min, t_max)
        right_hit = self.right.hit(ray, t_min, t_max)

        # if both branches have been hit then return the one that has been hit first
        if left_hit and right_hit:
            left_record, right_record = self.left.hit_record, self.right.hit_record
            self.hit_record = left_record if left_record.t < right_record.t else right_record
            return True

        if left_hit:
            self.hit_record = self.left.hit_record
            return True

        if right_hit:
            self.hit_record = self.right.hit_record
            return True

        # if nothing was hit
        return False

    def bounding_box(self, t0, t1):
        return True, self.bbox
