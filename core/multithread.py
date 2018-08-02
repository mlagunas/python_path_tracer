import numpy as np
from multiprocessing import Process, Pool, Value, Queue


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
        pool = Pool(processes=self.n_cores)  # create pool of threads
        results = [pool.apply_async(
            integrator,
            args=(*(self.rows_pool[core_idx],
                    self.cols_pool[core_idx],
                    self.camera.get_ray,
                    self.world)
                  ,)
        ) for core_idx in range(self.n_cores)]

        output = [p.get() for p in results]  # get results

        # map results to the resulting image
        for out in output:
            self.out_img[out[1], out[2], :] = out[0]
