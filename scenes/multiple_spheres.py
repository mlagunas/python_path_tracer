from geometries import MovingSphere, Sphere, HitableList
from materials import Lambertian, Dielectric, Metal
import numpy as np
import random

rand = random.random


def spheres():
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


def moving_spheres():
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
                    MovingSphere(center0=center,
                                 center1=center + np.array([0, 0.5 * rand(), 0]),
                                 time0=0,
                                 time1=1,
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
