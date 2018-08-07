from .integrator import Integrator
import numpy as np
from core.vec_utils import unit_vector
import random
from tqdm import tqdm
from multiprocessing import Value

rand = random.random

global pbar, pbar_update

pbar_update = Value('i', 0)  # create a value to track progress


class SurfaceNormal(Integrator):
    def __init__(self, width, height):
        global pbar

        self.height = height
        self.width = width
        pbar = tqdm(total=(width * height))

    def run(self, cols, rows, get_ray, world):
        global pbar, pbar_update
        color_values = np.zeros((*cols.shape, 3))

        for idx in range(cols.shape[0]):
            row, col = rows[idx], cols[idx]

            u = col / self.width
            v = row / self.height

            # trace ray
            ray = get_ray(u, v)

            # get color of the intersected objects
            # color =

            # normalize color for the number of samples and store it
            color_values[idx] = self._get_color(ray, world, depth=0, max_depth=50)

            # update progress bar
            with pbar_update.get_lock():
                pbar_update.value += 1
                pbar.n = pbar_update.value
                pbar.refresh()

        return color_values, rows, cols

    def _get_color(self, ray, world, depth, max_depth=50):
        if world.hit(ray, 0.001, float("inf")):  # return normal of a hit with an item in the world
            # print(hit_record.normal)
            return world.hit_record.normal

        else:  # if there is no hit return white color
            return np.array([0, 0, 0])
