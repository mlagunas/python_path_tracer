from core.vec3 import Vec3
from core.ray import Ray
from geometries.sphere import Sphere
from geometries.hitable import HitableList
from tqdm import tqdm

# canvas properties
width = 200
height = 100

# color parameters
color_max = 255.99

# position of the lower-left corner of the canvas
low_left_corner = Vec3(-2., -1., -1.)

# camera origin
origin = Vec3(0., 0., 0.)

# step to take on the horizontal and vertical direction
vertical = Vec3(0., 2., 0.)
horizontal = Vec3(4., 0., 0.)

# define geometries in the world
world = []
world.append(Sphere(center=[0, 0, -1], radius=0.5))
world.append(Sphere(center=[0, -100.5, -1], radius=100))
world = HitableList(world)


# start the rendering process and save result into ppm file 
def main():
    header = 'P3\n%d %d\n%d\n' % (width, height, 255)

    with open('images/hello_world.ppm', 'w') as f:
        f.write(header)

        # Iterate over heigth and width
        for j in tqdm(range(height - 1, 0, -1)):
            for i in range(width):
                u = i / width
                v = j / height

                ray = Ray(origin, low_left_corner + u * horizontal + v * vertical)
                color = get_color(ray, world).apply(lambda x: x * color_max)

                pixel = '%d %d %d\n' % (color.x(), color.y(), color.z())
                f.write(pixel)


def get_color(ray, world):
    if world.hit(ray, 0.0001, float("inf")):  # return normal of a hit with an item in the world
        hit_record = world.hit_record
        return 0.5 * hit_record['normal'].apply(lambda x: x + 1.)
    else:  # return background blue color
        t = 0.5 * (ray.direction.unit_vector().y() + 1.)
        return (1. - t) * Vec3(1., 1., 1.) + t * Vec3(0.5, 0.7, 1.)


if __name__ == '__main__':
    main()
