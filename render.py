import random

import numpy as np
from matplotlib import pyplot as plt

from core import Camera, Multithread
from integrators import PathTracer
from scenes import moving_spheres

# set random seed for reproducibility
random.seed(123456)
rand = random.random

# set precision
dtype = np.double

n_cores = 1  # number of cores to use

out_name = 'pruebas_bvh'  # outfile image name

samples_per_pixel = 1  # number samples per pixel

# canvas properties
width = 120
height = 80


def main():
    # define camera
    lookfrom = np.array([13, 2, 3], dtype=np.double)
    lookat = np.array([0, 0, 0], dtype=np.double)
    vup = np.array([0, 1, 0], dtype=np.double)
    camera = Camera(lookfrom=lookfrom, lookat=lookat, vup=vup,  # set camera plane coordinates
                    vertical_fov=20, aspect_ratio=width / height,  # set canvas properties
                    aperture=0.05, focus_dist=10,  # set camera lense
                    time0=0, time1=1)  # set time of aperture

    # create scene
    # world = spheres()

    world = moving_spheres()

    # set integrator
    integrator = PathTracer(samples_per_pixel, width, height)
    # integrator = Depth(width, height)
    # integrator = SurfaceNormal(width, height)

    # start rendering process
    multithread = Multithread(camera, world, n_cores)  # create object to handle multithreading
    multithread.create_working_pool(width, height)  # create the pool of pixels for each thread
    multithread.run(integrator)

    # store output image
    # todo change this into a FILM class
    plt.figure()
    plt.axis('equal')
    plt.imshow(multithread.out_img, origin='lower')
    plt.axis('off')
    plt.show()
    plt.imsave('images/' + out_name + '.png', multithread.out_img, origin='lower')


if __name__ == '__main__':
    main()
