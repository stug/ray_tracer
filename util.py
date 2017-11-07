import numpy


X_UNIT_VECTOR = numpy.array([1,0,0])
Y_UNIT_VECTOR = numpy.array([0,1,0])
Z_UNIT_VECTOR = numpy.array([0,0,1])
BASE_BASIS = (X_UNIT_VECTOR, Y_UNIT_VECTOR, Z_UNIT_VECTOR)


def normalize(vector):
    """Given a vector, return its unit vector"""
    return vector/numpy.linalg.norm(vector)


def rotate(vector, rotation_vector):
    """Rotate provided vector around rotation_vector by rotation_vector's
    magnitude (radians).

    A vector (A, 0, x) when rotated by r radians around the z-axis will have
    the form (A*cos(r), A*sin(r), x).  Thus if we take the provided rotation
    vector as our z basis vector and the vector to be rotated's component
    perpendicular to the rotation vector as our x unit vector, we can use this
    to transform the vector to something like the above form and then easily
    rotate the vector
    """
    # TODO: make a rotation vector matrix
    v = vector
    radians = numpy.linalg.norm(rotation_vector)
    if not radians:
        return vector

    r_unit = rotation_vector/radians

    v_dot_r  = numpy.dot(v, r_unit)
    v_along_r  = v_dot_r * r_unit
    v_not_along_r = v - v_along_r

    return (
        numpy.cos(radians) * v_not_along_r
        + numpy.sin(radians) * numpy.cross(r_unit, v_not_along_r)
        + v_dot_r * r_unit
    )


def change_basis(vector, new_basis):
    """Given a vector and a new 3-vector basis set (represented using the
    vector's current basis), return a representation of the vector in the new
    basis.
    """
    return numpy.array([
        numpy.dot(vector, new_basis[0]),
        numpy.dot(vector, new_basis[1]),
        numpy.dot(vector, new_basis[2]),
    ])
