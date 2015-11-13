import numpy

from util import normalize

# to avoid floating point errors
THRESHOLD_INTERSECTION_DISTANCE = 1e-10


class Shape(object):

    def find_intersection(self, ray_pos, ray_dir):
        """Should return a tuple of (intersection point, surface normal)"""
        raise NotImplementedError

    def build_surface_normal_at_point(self, point):
        raise NotImplementedError


class Sphere(Shape):

    def __init__(self, center, radius, color, specular=0):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular

    def find_intersection(self, ray_pos, ray_dir):
        """There will be an intersection if norm(ray_pos + d*ray_dir - center) = r
        for some value of d -- i.e. if we can construct a ray that passes at
        some point exactly r from the center of the circle.

        Expanding that equation yields a quadratic in d with the components below.
        """
        a = numpy.linalg.norm(ray_dir)**2
        b = 2*numpy.dot(ray_dir, ray_pos - self.center)
        c = numpy.linalg.norm(ray_pos - self.center)**2 - self.radius**2

        # TODO: this really should by DRYed up.  Seems like we'd want a class
        # to handle building the intersection and the normal together and maybe
        # testing that d >= 0
        # Also seems like the cases where discriminant >= 0 could be combined.
        # TODO: Apparently there's a case where we'd want the surface normal to
        # point in the opposite direction (if ray_pos is within the sphere)
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

    def build_surface_normal_at_point(self, point):
        return normalize(point - self.center)
