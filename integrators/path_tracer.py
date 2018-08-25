import random
from multiprocessing import Value

import numpy as np
from tqdm import tqdm

from core.vec_utils import unit_vector
from .integrator import Integrator

rand = random.random

global pbar, pbar_update

pbar_update = Value('i', 0)  # create a value to track progress


class PathTracer(Integrator):
    def __init__(self, samples_per_pixel, width, height):
        global pbar

        self.samples_per_pixel = samples_per_pixel
        self.height = height
        self.width = width
        pbar = tqdm(total=(width * height))

    def run(self, cols, rows, get_ray, world):
        global pbar, pbar_update
        color_values = np.zeros((*cols.shape, 3))

        for idx in range(cols.shape[0]):
            row, col = rows[idx], cols[idx]
            # initialize color to zero
            color = np.zeros(3)

            # antialiasing by sampling multiple times in the same pixel
            for s in range(self.samples_per_pixel):
                u = (col + rand()) / self.width
                v = (row + rand()) / self.height

                # trace ray
                ray = get_ray(u, v)

                # get color of the intersected objects
                color += self._get_color(ray, world, depth=0, max_depth=50)

            # normalize color for the number of samples and store it
            color_values[idx] = np.sqrt(color / self.samples_per_pixel)

            # update progress bar
            with pbar_update.get_lock():
                pbar_update.value += 1
                pbar.n = pbar_update.value
                pbar.refresh()

        return color_values, rows, cols

    def _get_color(self, ray, world, depth, max_depth=50):
        world_hit, hit_record = world.hit(ray, 0.001, float("inf"))  # intersect with the world

        if world_hit:  # run if there was a hit
            # check if the ray is absorved or scattered
            is_scattered = hit_record.material.scatter(ray, hit_record)

            # if it is scattered and we have scattered less than max_depth times
            # get the scattered ray and obtain its color
            if depth < max_depth and is_scattered:
                scattered = hit_record.material.scattered
                attenuation = hit_record.material.attenuation

                return attenuation * self._get_color(scattered, world, depth + 1, max_depth)
            else:
                return np.zeros(3)  # if it did not scatter, return a black pixel

        else:  # return background blue color
            t = 0.5 * (unit_vector(ray.direction)[1] + 1.)
            return (1. - t) * np.ones(3) + t * np.array([0.5, 0.7, 1.])
