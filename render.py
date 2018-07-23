from core import Ray, Vec3, Camera
from geometries import Sphere, HitableList
from materials import Lambertian, Metal
from tqdm import tqdm
import random
import math

# set random seed for reproducibility
random.seed(123456)

# outfile image name
out_name = 'antialiasing_100_diffuse'

# canvas properties
WIDTH = 200
HEIGHT = 100

# color parameters
MAX_COLOR = 255.99

# number of antialiasing samples
antialiasing_samples = 4

# define camera
camera = Camera(low_left_corner=Vec3(-2., -1., -1.),
                origin=Vec3(0., 0., 0.),
                vertical=Vec3(0., 2., 0.),
                horizontal=Vec3(4., 0., 0.))

# define geometries in the world
world = []
world.append(Sphere(center=[0, 0, -1], radius=0.5, material=Lambertian(Vec3(0.8, 0.3, 0.3))))
world.append(Sphere(center=[0, -100.5, -1], radius=100, material=Lambertian(Vec3(0.8, 0.8, 0.))))
world.append(Sphere(center=[1, 0, -1], radius=0.5, material=Metal(Vec3(0.8, 0.6, 0.2))))
world.append(Sphere(center=[-1, 0, -1], radius=0.5, material=Metal(Vec3(0.8, 0.8, 0.8))))
world = HitableList(world)


# start the rendering process and save result into ppm file 
def main():
    header = 'P3\n%d %d\n%d\n' % (WIDTH, HEIGHT, 255)

    with open('images/' + out_name + '.ppm', 'w') as f:
        f.write(header)

        # Iterate over heigth and width
        for j in tqdm(range(HEIGHT - 1, 0, -1)):
            for i in range(WIDTH):

                # initialize color
                color = Vec3(0., 0., 0.)

                # antialiasing by sampling multiple times in the same pixel
                for s in range(antialiasing_samples):
                    u = (i + random.random()) / WIDTH
                    v = (j + random.random()) / HEIGHT

                    # trace ray
                    ray = camera.get_ray(u, v)

                    # get color of the intersected objects
                    color += get_color(ray, world, depth=0, max_depth=50)

                # normalize color for the number of samples and the color range
                color = Vec3.sqrt(color / antialiasing_samples) * MAX_COLOR
                pixel = '%d %d %d\n' % (color.x(), color.y(), color.z())
                f.write(pixel)


def get_color(ray, world, depth, max_depth=50):
    if world.hit(ray, 0.001, float("inf")):  # return normal of a hit with an item in the world
        hit_record = world.hit_record

        # check if the ray is absorvec or scattered
        is_scattered = hit_record['material'].scatter(ray, hit_record)

        # if it is scattered and we have scattered less than max_depth times
        # get the scattered ray and obtain its color
        if depth < max_depth and is_scattered:
            scattered = hit_record['material'].scattered
            attenuation = hit_record['material'].attenuation

            return attenuation * get_color(scattered, world, depth + 1)
        else:  # if it did not scatter, return a black pixel
            return Vec3(0., 0., 0.)

    else:  # return background blue color
        t = 0.5 * (ray.direction.unit_vector().y() + 1.)
        return (1. - t) * Vec3(1., 1., 1.) + t * Vec3(0.5, 0.7, 1.)


if __name__ == '__main__':
    main()
