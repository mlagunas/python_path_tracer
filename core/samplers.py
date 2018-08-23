import math
from bisect import bisect_left
from functools import reduce

import numpy as np

uniform = np.random.uniform

"""
utility functions
"""


def print_discrepancy(discrepancy, title):
    print('%s\t%.4f\t%.4f\t%.4f' % (title, discrepancy.mean(), discrepancy.std(), discrepancy.max()))


def plotter(samples, title, grid=None):
    from matplotlib import pyplot as plt

    if grid is not None:
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
    if grid is not None:
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


def take_closest(my_list, number):
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
    int1 = take_closest(factors, math.sqrt(n))
    int2 = n // int1
    return int1, int2


"""
sampling functions
"""


class Sampler(object):
    def __init__(self, N, dim=2):
        self.N = N
        self.dim = dim

    def __call__(self, get_grid=False):
        raise NotImplementedError()


class RandomSampling(Sampler):
    def __call__(self, get_grid=False):
        return uniform(0, 1, (self.N, self.dim))


class RegularSampling(Sampler):
    def __call__(self, get_grid=False):
        samples = np.zeros((self.N, self.dim))

        if self.dim == 2:
            # split N into two factors in such a way N = nx * ny
            ny, nx = two_factors_to_n(self.N)

            # get all the combinations of nx and ny
            j, i = np.meshgrid(range(nx), range(ny))

            # get grid values
            grid_i = i[:, 0] / nx
            grid_j = j[0] / ny

            j, i = j.flatten(), i.flatten()

            # get samples
            samples[:, 0] = (i + 0.5) / nx
            samples[:, 1] = (j + 0.5) / ny

        if get_grid:
            return samples, [grid_i, grid_j]
        return samples


class JitteredSampling(Sampler):
    def __call__(self, get_grid=False):
        samples = np.zeros((self.N, self.dim))

        if self.dim == 2:
            # split N into two factors in such a way N = nx * ny
            ny, nx = two_factors_to_n(self.N)

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

        if get_grid:
            return samples, [grid_i, grid_j]
        return samples


class HalfJitteredSampling(Sampler):
    def __call__(self, get_grid=False):
        samples = np.zeros((self.N, self.dim))

        if self.dim == 2:
            # split N into two factors in such a way N = nx * ny
            ny, nx = two_factors_to_n(self.N)

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

        if get_grid:
            return samples, [grid_i, grid_j]
        return samples


class PoissonDiskSampling(Sampler):
    def __init__(self, d, *args, **kwargs):
        self.d = d
        super(PoissonDiskSampling, self).__init__(*args, **kwargs)

    def __call__(self, get_grid=False):
        def get_mask(samples):
            j, i = np.meshgrid(range(self.N), range(self.N))
            j, i = j.flatten(), i.flatten()

            dist = ((samples[i, 0] - samples[j, 0]) ** 2 + (samples[i, 1] - samples[j, 1]) ** 2).reshape(
                (self.N, self.N))

            upper_diag_idx = np.triu_indices(self.N)
            dist[upper_diag_idx] = float('inf')
            mask = np.any(dist < self.d ** 2, axis=1)
            return mask

        samples = uniform(0, 1, (self.N, self.dim))
        mask = get_mask(samples)

        while np.any(mask):
            samples[mask] = uniform(0, 1, (self.N, self.dim))[mask]
            mask = get_mask(samples)

        return samples


class NRooksSampling(Sampler):
    def __call__(self, get_grid=False):
        samples = np.zeros((self.N, self.dim))
        i = np.arange(0, self.N)
        samples_x = uniform(i / self.N, (i + 1) / self.N)
        samples_y = uniform(i / self.N, (i + 1) / self.N)

        # get grid values
        grid_i = grid_j = i / self.N

        # randomly shuffle samples over X
        np.random.shuffle(samples_x)
        samples[:, 0] = samples_x
        samples[:, 1] = samples_y

        if get_grid:
            return samples, [grid_i, grid_j]
        return samples


"""
Discrepancy measures

"""


def zeremba_discrepancy(sampling, iters):
    """


    samples: random samples inside a unit square (if 2D)


    This method returns the zeremba discrepancy which is defined as |n/N - ab|, where
    ab is the area of the small square, N is the total number of samples and n is the
    number of samples inside the small square defined with the (a,b) corner.

    x - represent the random samples
     _______________________
    |             x         |
    |     x             x   |
    |          x            |
    |____________x(a,b)     |
    |       x    |        x |
    |  x         |  x       |
    |            |     x    |
    |            |          |
    |       x    |   x      |
    |____________|__________|
    :param samples:
    :return:
    """

    discrepancy = np.zeros(iters)

    for i in range(iters):
        samples = sampling()  # call sampling method to obtain samples
        samples_i, samples_j = samples[:, 0], samples[:, 1]
        discrepancy_i = np.zeros(len(samples))
        for idx in range(len(samples)):
            a, b = samples[idx]  # get point (a,b)
            n = np.sum((samples_i < a) & (samples_j < b))  # find all the points inside the small square formed by (a,b)
            discrepancy_i[idx] = np.abs(n / len(samples) - a * b)  # get the discrepancy value

        discrepancy[i] = discrepancy_i.max()
    return discrepancy


def zeremba_rms_discrepancy(sampling, iters):
    """

    Instead of returning the lowest upper bound, this method computes
    the root mean square of the single discrepancy values

    :param samples:
    :return:
    """

    discrepancy = np.zeros(iters)

    for i in range(iters):
        samples = sampling()  # call sampling method to obtain samples
        samples_i, samples_j = samples[:, 0], samples[:, 1]
        discrepancy_i = np.zeros(len(samples))
        for idx in range(len(samples)):
            a, b = samples[idx]  # get point (a,b)
            n = np.sum((samples_i < a) & (samples_j < b))  # find all the points inside the small square formed by (a,b)
            discrepancy_i[idx] = np.abs(n / len(samples) - a * b)  # get the discrepancy value

        discrepancy[i] = np.sqrt((discrepancy_i ** 2).mean())
    return discrepancy


def strout_discrepancy(sampling, iters):
    discrepancy = np.zeros(iters)

    for i in range(iters):
        samples = sampling()  # call sampling method to obtain samples
        samples_i, samples_j = samples[:, 0], samples[:, 1]
        discrepancy_i = []
        for idx_ab in range(len(samples)):
            a, b = samples[idx_ab]  # get point (a,b)
            for idx_cd in range(idx_ab, len(samples)):
                c, d = samples[idx_cd]  # get point (c,d)

                # find all the points inside the small square formed by (a,b), (c,d)
                n = np.sum((samples_i < a) & (samples_j < b) & (samples_i > c) & (samples_j > d))
                discrepancy_i.append(np.abs(n / len(samples) - (a - c) * (b - d)))  # get the discrepancy value

        discrepancy[i] = np.array(discrepancy_i).max()
        # discrepancy[i] = np.sqrt((discrepancy_i ** 2).mean())
    return discrepancy


"""
Test of the sampling functions
"""
N = 16

rnd = RandomSampling(N=N)
reg = RegularSampling(N=N)
jit = JitteredSampling(N=N)
hjit = HalfJitteredSampling(N=N)
poisson = PoissonDiskSampling(N=N, d=0.2)
nrooks = NRooksSampling(N=N)

rnd_samples = rnd()
reg_samples, reg_grid = reg(get_grid=True)
jit_samples, jit_grid = jit(get_grid=True)
hjit_samples, hjit_grid = hjit(get_grid=True)
poisson_samples = poisson()
nrooks_samples, nrooks_grid = nrooks(get_grid=True)

plotter(rnd_samples, 'random sampling')
plotter(reg_samples, 'regular sampling', grid=reg_grid)
plotter(jit_samples, 'jitered sampling', grid=jit_grid)
plotter(hjit_samples, 'half-jitered sampling', grid=hjit_grid)
plotter(poisson_samples, 'poisson disk sampling')
plotter(nrooks_samples, 'n-rooks sampling', grid=nrooks_grid)

iters = 100
print_discrepancy(zeremba_discrepancy(rnd, iters), 'Zeremba disc. random sampling:')
print_discrepancy(zeremba_discrepancy(reg, iters), 'Zeremba disc. regular sampling:')
print_discrepancy(zeremba_discrepancy(jit, iters), 'Zeremba disc. jittered sampling:')
print_discrepancy(zeremba_discrepancy(hjit, iters), 'Zeremba disc. half-jittered sampling:')
print_discrepancy(zeremba_discrepancy(poisson, iters), 'Zeremba disc. poisson sampling:')
print_discrepancy(zeremba_discrepancy(nrooks, iters), 'Zeremba disc. n-rooks sampling:')
print()

iters = 100
print_discrepancy(zeremba_rms_discrepancy(rnd, iters), 'Zeremba RMS disc. random sampling:')
print_discrepancy(zeremba_rms_discrepancy(reg, iters), 'Zeremba RMS disc. regular sampling:')
print_discrepancy(zeremba_rms_discrepancy(jit, iters), 'Zeremba RMS disc. jittered sampling:')
print_discrepancy(zeremba_rms_discrepancy(hjit, iters), 'Zeremba RMS disc. half-jittered sampling:')
print_discrepancy(zeremba_rms_discrepancy(poisson, iters), 'Zeremba RMS disc. poisson sampling:')
print_discrepancy(zeremba_rms_discrepancy(nrooks, iters), 'Zeremba RMS disc. n-rooks sampling:')
print()

iters = 100
print_discrepancy(strout_discrepancy(rnd, iters), 'Strout disc. random sampling:')
print_discrepancy(strout_discrepancy(reg, iters), 'Strout disc. regular sampling:')
print_discrepancy(strout_discrepancy(jit, iters), 'Strout disc. jittered sampling:')
print_discrepancy(strout_discrepancy(hjit, iters), 'Strout disc. half-jittered sampling:')
print_discrepancy(strout_discrepancy(poisson, iters), 'Strout disc. poisson sampling:')
print_discrepancy(strout_discrepancy(nrooks, iters), 'Strout disc. n-rooks sampling:')
print()
