import numpy


Z_UNIT_VECTOR = numpy.array([0,0,1])


def normalize(vector):
    """Given a vector, return its unit vector"""
    return vector/numpy.linalg.norm(vector)
