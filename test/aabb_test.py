from core import Camera, Multithread
from integrators import PathTracer, Depth, SurfaceNormal
from matplotlib import pyplot as plt
from scenes import spheres, moving_spheres
from geometries import MovingSphere, Sphere, HitableList
from materials import Lambertian, Dielectric, Metal

import random
import numpy as np

# set random seed for reproducibility
random.seed(123456)
rand = random.random

n_cores = 8  # number of cores to use

out_name = 'aabb test'  # outfile image name

samples_per_pixel = 32  # number samples per pixel

# canvas properties
width = 120
height = 80


def main():
    # define camera
    lookfrom = np.array([13, 2, 3])
    lookat = np.array([0, 0, 0])
    vup = np.array([0, 1, 0])
    camera = Camera(lookfrom=lookfrom, lookat=lookat, vup=vup,  # set camera plane coordinates
                    vertical_fov=20, aspect_ratio=width / height,  # set canvas properties
                    aperture=0.05, focus_dist=10,  # set camera lense
                    time0=0, time1=1)  # set time of aperture

    # create scene
    # world = spheres()

    world = Sphere(center=np.array([0, 0, 0]),
                   radius=1,
                   material=Lambertian((0.4, 0.2, 0.1)))

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
    # plt.imsave('images/' + out_name + '.png', multithread.out_img, origin='lower')

if __name__ == '__main__':
    main()
