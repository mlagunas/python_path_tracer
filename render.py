from core import Ray, Vec3, Camera
from geometries import Sphere, HitableList
from materials import Lambertian, Metal, Dielectric
from tqdm import tqdm
import random
import numpy as np
from matplotlib import pyplot as plt
from multiprocessing.dummy import Pool as ThreadPool

# set random seed for reproducibility
random.seed(123456)
rand = random.random

# number of cores to use
n_cores = 8
pool = ThreadPool(4)

# outfile image name
out_name = 'test_final_image'

# canvas properties
width = 1200
height = 800

# number samples per pixel
samples_per_pixel = 10


# start the rendering process and save result into ppm file
def main():
    # define camera
    lookfrom = Vec3(13, 2, 3)
    lookat = Vec3(0, 0, 0)
    vup = Vec3(0, 1, 0)
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

    out_img = np.zeros((height, width, 3))

    # Iterate over heigth and width
    with tqdm(total=width * height) as pbar:
        for row in tqdm(range(height)):
            for col in range(width):
                path_trace(col, row, camera, world, out_img, pbar)

    # with tqdm(total=width * height) as pbar:
    #     thread_input = [(col, row, camera, world, out_img, pbar) for row in range(height) for col in range(width)]
    #     pool.starmap(path_trace, thread_input)

    plt.figure()
    plt.axis('equal')
    plt.imshow(out_img, origin='lower')
    plt.axis('off')
    plt.show()
    plt.imsave('images/' + out_name + '.png', out_img)


def path_trace(col, row, camera, world, out_img, pbar):
    # initialize color to zero
    color = Vec3(0)

    # antialiasing by sampling multiple times in the same pixel
    for s in range(samples_per_pixel):
        u = (col + rand()) / width
        v = (row + rand()) / height

        # trace ray
        ray = camera.get_ray(u, v)

        # get color of the intersected objects
        color += get_color(ray, world, depth=0, max_depth=50)

    # normalize color for the number of samples and store it
    out_img[row, col, :] = (Vec3.sqrt(color / samples_per_pixel)).vec

    # call tqdm
    pbar.update()


def create_world():
    world = []

    # add the world 'ground' as a big sphere
    world.append(
        Sphere(center=(0, -1000, 0),
               radius=1000,
               material=Lambertian(Vec3(0.5))))

    for a in range(-11, 11):
        for b in range(-11, 11):

            # get geometry center
            center = Vec3(a + 0.9 * rand(), 0.2, b + 0.9 * rand())

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
                           material=Metal(0.5 * Vec3(1 + rand(), 1 + rand(), 1 + rand()), 0.5 * rand())))

            else:  # Dielectric
                world.append(
                    Sphere(center=center,
                           radius=0.2,
                           material=Dielectric(1.5)))

    # Add last batch of bigger spheres
    world.append(
        Sphere(center=Vec3(0, 1, 0),
               radius=1,
               material=Dielectric(1.5)))
    world.append(
        Sphere(center=Vec3(-4, 1, 0),
               radius=1,
               material=Lambertian((0.4, 0.2, 0.1))))
    world.append(
        Sphere(center=Vec3(4, 1, 0),
               radius=1,
               material=Metal((0.4, 0.2, 0.15), 0)))

    return HitableList(world)


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
            return Vec3(0., 0., 0.)

    else:  # return background blue color
        t = 0.5 * (ray.direction.unit_vector().y() + 1.)
        return (1. - t) * Vec3(1., 1., 1.) + t * Vec3(0.5, 0.7, 1.)


if __name__ == '__main__':
    main()
