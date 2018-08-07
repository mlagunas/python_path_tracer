import numpy as np
from pathos.multiprocessing import Pool
import sys


class Multithread(object):

    def __init__(self, camera, world, n_cores):
        self.n_cores = n_cores
        self.camera = camera
        self.world = world

    def create_working_pool(self, width, height):
        self.out_img = np.zeros((height, width, 3))
        self.width, self.height = width, height

        matrix_pool = np.meshgrid(np.arange(width), np.arange(height))
        self.rows_pool = matrix_pool[0].reshape(self.n_cores, -1)
        self.cols_pool = matrix_pool[1].reshape(self.n_cores, -1)

    def run(self, integrator):
        if self.n_cores == 1:  # run single thread
            self.out_img = integrator.run(self.rows_pool[0],
                                          self.cols_pool[0],
                                          self.camera.get_ray,
                                          self.world)[0].reshape((self.height, self.width, 3))
        else:  # run multithread
            pool = Pool(processes=self.n_cores)  # create pool of threads
            results = [pool.apply_async(
                integrator.run,
                args=(self.rows_pool[core_idx],
                      self.cols_pool[core_idx],
                      self.camera.get_ray,
                      self.world)
            ) for core_idx in range(self.n_cores)]

            output = [p.get() for p in results]  # get results

            # map results to the resulting image
            for out in output:
                self.out_img[out[1], out[2], :] = out[0]
