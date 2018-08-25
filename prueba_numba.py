import numba as nb
import numpy as np

spec = [
    ('min', nb.double[:]),
    ('max', nb.double[:]),
]


@nb.jitclass(spec)
class numpy_trial(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max


nptrial = numpy_trial(np.array([1, 2, 3]), np.array([4, 5, 6], dtype=np.double))
print(nptrial)
# import numpy as np
# from numba import int32, float32  # import the types
# from numba import jitclass  # import the decorator
#
# spec = [
#     ('value', int32),  # a simple scalar field
#     ('array', float32[:]),  # an array field
# ]
#
#
# @jitclass(spec)
# class Bag(object):
#     def __init__(self, value):
#         self.value = value
#         self.array = np.zeros(value, dtype=np.float32)
#
#     @property
#     def size(self):
#         return self.array.size
#
#     def increment(self, val):
#         for i in range(self.size):
#             self.array[i] = val
#         return self.array
#
#
# b = Bag(10)
# print (b.size)
