import numpy


def normalize(vector):
    """Given a vector, return its unit vector"""
    return vector/numpy.linalg.norm(vector)
