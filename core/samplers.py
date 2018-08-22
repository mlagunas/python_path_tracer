import math
from bisect import bisect_left
from functools import reduce

import numpy as np

uniform = np.random.uniform

"""
utility functions
"""


def plotter(samples, title, grid=False):
    from matplotlib import pyplot as plt

    if grid:
        samples, grid = samples
        grid_i = grid[0]
        grid_j = grid[1]
        all_axis = np.zeros(samples.shape)
        all_axis[:, 1] = 1

    plt.scatter(samples[:, 0], samples[:, 1])
    plt.title(title)
    axes = plt.gca()
    axes.set_xlim([-0.1, 1.1])
    axes.set_ylim([-0.1, 1.1])
    axes.set_aspect('equal')
    if grid:
        for idx in range(len(grid_i)):
            plt.plot([grid_i[idx], grid_i[idx]], all_axis[idx], alpha=0.2, color='b', dashes=[6, 2])
        for idx in range(len(grid_j)):
            plt.plot(all_axis[idx], [grid_j[idx], grid_j[idx]], alpha=0.2, color='b', dashes=[6, 2])

        # add grid lines of the last elements of the square
        plt.plot([all_axis[1], all_axis[1]], all_axis[idx], alpha=0.2, color='b', dashes=[6, 2])
        plt.plot(all_axis[idx], [all_axis[1], all_axis[1]], alpha=0.2, color='b', dashes=[6, 2])

    plt.show()


def get_factors(n):
    # get factors and make it a set to remove duplicates
    # then make it a lit to sort in in increasing order
    factors = list(set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0))))
    factors.sort()

    # return all factors execept the original number (n)
    return factors[:-1]


def takeClosest(my_list, number):
    """
    Assumes my_list is sorted. Returns closest value to number.

    If two numbers are equally close, return the smallest number.
    """

    pos = bisect_left(my_list, number)
    if pos == 0:
        return my_list[0]
    if pos == len(my_list):
        return my_list[-1]
    before = my_list[pos - 1]
    after = my_list[pos]
    if after - number < number - before:
        return after
    else:
        return before


def two_factors_to_n(n):
    """
    n is an integer number

    The function returns two integers that multiplied together give n -> int1 * int2 = n
    """

    factors = get_factors(n)
    int1 = takeClosest(factors, math.sqrt(n))
    int2 = n // int1
    return int1, int2


"""
sampling functions
"""


def random_sampling(N, dim=2):
    return uniform(0, 1, (N, dim))


def regular_sampling(N, dim=2):
    samples = np.zeros((N, dim))

    if dim == 2:
        # split N into two factors in such a way N = nx * ny
        ny, nx = two_factors_to_n(N)

        # get all the combinations of nx and ny
        j, i = np.meshgrid(range(nx), range(ny))

        # get grid values
        grid_i = i[:, 0] / nx
        grid_j = j[0] / ny

        j, i = j.flatten(), i.flatten()

        # get samples
        samples[:, 0] = (i + 0.5) / nx
        samples[:, 1] = (j + 0.5) / ny

    return samples, [grid_i, grid_j]


def jittered_sampling(N, dim=2):
    samples = np.zeros((N, dim))

    if dim == 2:
        # split N into two factors in such a way N = nx * ny
        ny, nx = two_factors_to_n(N)

        # get all the combinations of nx and ny
        j, i = np.meshgrid(range(ny), range(nx))

        # get grid values
        grid_i = i[:, 0] / nx
        grid_j = j[0] / ny

        # flatten idxs to get samples
        j, i = j.flatten(), i.flatten()

        # get samples
        samples[:, 0] = uniform(i / nx, (i + 1) / nx)
        samples[:, 1] = uniform(j / ny, (j + 1) / ny)

    return samples, [grid_i, grid_j]


def half_jittered_sampling(N, dim=2):
    samples = np.zeros((N, dim))

    if dim == 2:
        # split N into two factors in such a way N = nx * ny
        ny, nx = two_factors_to_n(N)

        # get all the combinations of nx and ny
        j, i = np.meshgrid(range(ny), range(nx))

        # get grid values
        grid_i = i[:, 0] / nx
        grid_j = j[0] / ny

        # flatten idxs to get samples
        j, i = j.flatten(), i.flatten()

        # get samples
        samples[:, 0] = uniform((i + 0.25) / nx, (i + 0.75) / nx)
        samples[:, 1] = uniform((j + 0.25) / ny, (j + 0.75) / ny)

    return samples, [grid_i, grid_j]


def poisson_disk_sampling(N, d, dim=2):
    def get_mask(samples):
        j, i = np.meshgrid(range(N), range(N))
        j, i = j.flatten(), i.flatten()

        dist = ((samples[i, 0] - samples[j, 0]) ** 2 + (samples[i, 1] - samples[j, 1]) ** 2).reshape((N, N))

        upper_diag_idx = np.triu_indices(N)
        dist[upper_diag_idx] = float('inf')
        mask = np.any(dist < d ** 2, axis=1)
        return mask

    samples = uniform(0, 1, (N, dim))
    mask = get_mask(samples)

    while np.any(mask):
        samples[mask] = uniform(0, 1, (N, dim))[mask]
        mask = get_mask(samples)

    return samples


def n_rooks_sampling(N, dim=2):
    samples = np.zeros((N, dim))
    i = np.arange(0, N)
    samples_x = uniform(i / N, (i + 1) / N)
    samples_y = uniform(i / N, (i + 1) / N)

    # get grid values
    grid_i = grid_j = i / N

    # randomly shuffle samples over X
    np.random.shuffle(samples_x)
    samples[:, 0] = samples_x
    samples[:, 1] = samples_y

    return samples, [grid_i, grid_j]


"""
Test of the sampling functions
"""

plotter(random_sampling(36), 'random sampling')
plotter(regular_sampling(36), 'regular sampling', grid=True)
plotter(jittered_sampling(36), 'jitered sampling', grid=True)
plotter(half_jittered_sampling(36), 'half-jitered sampling', grid=True)
plotter(poisson_disk_sampling(36, d=0.1), 'poisson disk sampling')
plotter(n_rooks_sampling(36), 'n rooks sampling', grid=True)
