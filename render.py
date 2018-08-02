from core import Camera, Multithread
from core.vec_utils import unit_vector
from geometries import Sphere, HitableList
from materials import Lambertian, Metal, Dielectric
from tqdm import tqdm
from matplotlib import pyplot as plt
from multiprocessing import Process, Pool, Value, Queue

import random
import numpy as np

# set random seed for reproducibility
random.seed(123456)
rand = random.random

n_cores = 8  # number of cores to use

out_name = 'test_final_image'  # outfile image name

samples_per_pixel = 32  # number samples per pixel

# canvas properties
width = 120
height = 80


def main():
    global pbar, pbar_update

    pbar_update = Value('d', 0)  # create a value to track progress

    # define camera
    lookfrom = np.array([13, 2, 3])
    lookat = np.array([0, 0, 0])
    vup = np.array([0, 1, 0])
    camera = Camera(lookfrom=lookfrom, lookat=lookat, vup=vup,  # set camera plane coordinates
                    vertical_fov=20, aspect_ratio=width / height,  # set canvas properties
                    aperture=.1, focus_dist=10)  # set camera lense

    # define geometries in the world
    # world = []
    # world.append(Sphere(center=[0, 0, -1], radius=0.5, material=Lambertian(Vec3(0.8, 0.3, 0.3))))
    # world.append(Sphere(center=[0, -100.5, -1], radius=100, material=Lambertian(Vec3(0.8, 0.8, 0.))))
    # world.append(Sphere(center=[1, 0, -1], radius=0.5, material=Metal(Vec3(0.8, 0.6, 0.2), fuzzy=0.3)))
    # world.append(Sphere(center=[-1, 0, -1], radius=0.5, material=Dielectric(1.5)))
    # world.append(Sphere(center=[-1, 0, -1], radius=-0.45, material=Dielectric(1.5)))
    # world = HitableList(world)

    world = create_world()

    multithread = Multithread(camera, world, n_cores)  # create object to handle multithreading
    multithread.create_working_pool(width, height)  # create the pool of pixels for each thread
    with tqdm(total=(width * height)) as pbar:  # start the processes
        multithread.run(path_trace)

    # store output image
    # todo change this into a FILM class
    plt.figure()
    plt.axis('equal')
    plt.imshow(multithread.out_img, origin='lower')
    plt.axis('off')
    plt.show()
    plt.imsave('images/' + out_name + '.png', multithread.out_img, origin='lower')


# todo change this into an integrators class
def path_trace(cols, rows, get_ray, world):
    global pbar, pbar_update

    color_values = np.zeros((*cols.shape, 3))

    for idx in range(cols.shape[0]):
        row, col = rows[idx], cols[idx]
        # initialize color to zero
        color = np.zeros(3)

        # antialiasing by sampling multiple times in the same pixel
        for s in range(samples_per_pixel):
            u = (col + rand()) / width
            v = (row + rand()) / height

            # trace ray
            ray = get_ray(u, v)

            # get color of the intersected objects
            color += get_color(ray, world, depth=0, max_depth=50)

        # normalize color for the number of samples and store it
        # out_img[row, col, :] = np.sqrt(color / samples_per_pixel)
        color_values[idx] = np.sqrt(color / samples_per_pixel)

        # update tqdm var
        with pbar_update.get_lock():
            pbar_update.value += 1
            pbar.n = pbar_update.value
            pbar.refresh()

    # queue.put(color_values, cols, cols)  # store the output
    return color_values, rows, cols


def get_color(ray, world, depth, max_depth=50):
    if world.hit(ray, 0.001, float("inf")):  # return normal of a hit with an item in the world
        hit_record = world.hit_record

        # check if the ray is absorvec or scattered
        is_scattered = hit_record.material.scatter(ray, hit_record)

        # if it is scattered and we have scattered less than max_depth times
        # get the scattered ray and obtain its color
        if depth < max_depth and is_scattered:
            scattered = hit_record.material.scattered
            attenuation = hit_record.material.attenuation

            return attenuation * get_color(scattered, world, depth + 1)
        else:  # if it did not scatter, return a black pixel
            return np.zeros(3)

    else:  # return background blue color
        t = 0.5 * (unit_vector(ray.direction)[1] + 1.)
        return (1. - t) * np.ones(3) + t * np.array([0.5, 0.7, 1.])


def create_world():
    world = []

    # add the world 'ground' as a big sphere
    world.append(
        Sphere(center=[0, -1000, 0],
               radius=1000,
               material=Lambertian([0.5, 0.5, 0.5])
               )
    )

    for a in range(-11, 11):
        for b in range(-11, 11):

            # get geometry center
            center = np.array([a + 0.9 * rand(), 0.2, b + 0.9 * rand()])

            # set a random to choose the material of the geometry
            material_chooser = rand()

            # set the material of the created geometries
            if material_chooser < 0.8:  # Diffuse
                world.append(
                    Sphere(center=center,
                           radius=0.2,
                           material=Lambertian((rand() ** 2, rand() ** 2, rand() ** 2))))

            elif material_chooser < 0.95:  # Metal
                world.append(
                    Sphere(center=center,
                           radius=0.2,
                           material=Metal(0.5 * np.array([1 + rand(), 1 + rand(), 1 + rand()]), 0.5 * rand())))

            else:  # Dielectric
                world.append(
                    Sphere(center=center,
                           radius=0.2,
                           material=Dielectric(1.5)))

    # Add last batch of bigger spheres
    world.append(
        Sphere(center=np.array([0, 1, 0]),
               radius=1,
               material=Dielectric(1.5)))
    world.append(
        Sphere(center=np.array([-4, 1, 0]),
               radius=1,
               material=Lambertian((0.4, 0.2, 0.1))))
    world.append(
        Sphere(center=np.array([4, 1, 0]),
               radius=1,
               material=Metal((0.4, 0.2, 0.15), 0)))

    return HitableList(world)


if __name__ == '__main__':
    main()
