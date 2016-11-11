import numpy

import colors
from util import normalize
from util import X_UNIT_VECTOR
from util import Z_UNIT_VECTOR


# to avoid floating point errors
THRESHOLD_INTERSECTION_DISTANCE = 1e-10


# TODO: should standardize this interface more -- should guarantee that everything
# has color, specular, and transparency defined...

class Shape(object):

    def find_intersection(self, ray_pos, ray_dir):
        """Should return a tuple of (intersection point, surface normal)"""
        raise NotImplementedError

    def build_surface_normal_at_point_for_ray(self, point, ray):
        raise NotImplementedError

    def get_color_at_point(self, point):
        return self.color


class Sphere(Shape):

    def __init__(self, center, radius, color, specular=0, transparency=0, index_of_refraction=1):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.transparency = transparency
        self.index_of_refraction = index_of_refraction

    def find_intersection(self, ray_pos, ray_dir):
        """There will be an intersection if norm(ray_pos + d*ray_dir - center) = r
        for some value of d -- i.e. if we can construct a ray that passes at
        some point exactly r from the center of the circle.

        Expanding that equation yields a quadratic in d with the components below.
        """
        a = numpy.linalg.norm(ray_dir)**2
        b = 2*numpy.dot(ray_dir, ray_pos - self.center)
        c = numpy.linalg.norm(ray_pos - self.center)**2 - self.radius**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return None
        elif discriminant == 0:
            d = -b/a
            if d < 0:
                return None
            else:
                intersection = ray_pos + d*ray_dir
                return intersection, self.build_surface_normal(intersection)
        else:
            d1 = (-b + numpy.sqrt(discriminant))/(2*a)
            d2 = (-b - numpy.sqrt(discriminant))/(2*a)
            best_d = None
            for potential_d in (d1, d2):
                if potential_d < THRESHOLD_INTERSECTION_DISTANCE:
                    continue
                else:
                    best_d = potential_d if best_d is None else min(best_d, potential_d)
            if best_d is None:
                return None

            intersection = ray_pos + best_d*ray_dir
            return intersection

    def build_surface_normal_at_point_for_ray(self, point, ray):
        # Surface normal should point in the opposite direction of the incoming
        # ray
        base_surface_normal = normalize(point - self.center)
        return -1*numpy.sign(numpy.dot(base_surface_normal, ray)) * base_surface_normal

    def ray_originates_inside(self, intersection_point, ray):
        # Note that in this case, the ray ENDS at intersection point
        return numpy.dot(intersection_point - self.center, ray) > 0


class Plane(Shape):

    def __init__(self, center, normal, color, specular=0, transparency=0, checkered=False):
        self.center = center
        self.normal = normalize(normal)
        self.color = color
        self.specular = specular
        self.transparency = transparency
        self.checkered = checkered

        if checkered:
            self.basis_vector_1 = numpy.cross(self.normal, Z_UNIT_VECTOR)
            if numpy.linalg.norm(self.basis_vector_1) == 0:
                self.basis_vector_1 = numpy.cross(self.normal, X_UNIT_VECTOR)
            self.basis_vector_1 = normalize(self.basis_vector_1)
            self.basis_vector_2 = numpy.cross(self.normal, self.basis_vector_1)
        else:
            self.basis_vector_1 = None
            self.basis_vector_2 = None

    def find_intersection(self, ray_pos, ray_dir):
        """A plane is defined as all points p such that, for an arbitrary point
        p0 in the plane and a normal vector n, dot(p-p0, n) = 0.  In this case,
        p = ray_pos + d*ray_dir and so the intersection will occur when
        d = dot(p0 - ray_pos, n)/dot(ray_dir, n).  dot(ray_dir, n) = 0 implies
        that the ray and plane will never intersect.
        """
        denominator = numpy.dot(ray_dir, self.normal)
        if denominator == 0:
            return None

        numerator = numpy.dot(self.center - ray_pos, self.normal)
        d = numerator/denominator
        return ray_pos + d*ray_dir if d > THRESHOLD_INTERSECTION_DISTANCE else None

    def build_surface_normal_at_point_for_ray(self, point, ray):
        return -1*numpy.sign(numpy.dot(self.normal, ray)) * self.normal

    def get_color_at_point(self, point):
        # TODO: implement a class for textures
        if not self.checkered:
            return self.color

        vector_to_point = point - self.center

        vector_component_1 = numpy.dot(self.basis_vector_1, vector_to_point)
        vector_component_2 = numpy.dot(self.basis_vector_2, vector_to_point)
        coord_1_is_even = numpy.floor(vector_component_1) % 2 == 0
        coord_2_is_even = numpy.floor(vector_component_2) % 2 == 0

        if coord_1_is_even == coord_2_is_even:
            return self.color
        else:
            return colors.BLACK

    def ray_originates_inside(self, ray):
        # This is a 2-D object and has no inside
        return False


class LightSource(object):

    def __init__(self, position):
        self.position = position
