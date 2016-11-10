import numpy

import colors
from util import normalize
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

    def build_surface_normal_at_point_for_ray(self, point, ray):
        # Surface normal should point in the opposite direction of the incoming
        # ray
        base_surface_normal = normalize(point - self.center)
        return -1*numpy.sign(numpy.dot(base_surface_normal, ray)) * base_surface_normal

    def ray_originates_inside(self, intersection_point, ray):
        # Note that in this case, the ray ENDS at intersection point
        return numpy.dot(intersection_point - self.center, ray) > 0


class ZPlane(Shape):

    # TODO: generalize this to allow any orientation
    def __init__(self, z_coord, color, checkered=False, specular=0, transparency=0, index_of_refraction=1):
        self.z_coord = z_coord
        self.color = color
        self.checkered=checkered
        self.specular = specular
        self.transparency = transparency
        self.index_of_refraction = index_of_refraction

    def find_intersection(self, ray_pos, ray_dir):
        """Intersection if ray_pos.z + d*ray_dir.z = z_coord"""
        # If the incoming ray has a z coordinate of 0, then either the ray
        # started within the plane, or it will never intersect it.
        if ray_dir[2] == 0:
            if ray_pos[2] == self.z_coord:
                return ray_pos
            else:
                return None
        d = (self.z_coord - ray_pos[2])/ray_dir[2]
        return ray_pos + d*ray_dir if d > THRESHOLD_INTERSECTION_DISTANCE else None

    def build_surface_normal_at_point_for_ray(self, point, ray):
        # Surface normal is the z unit vector pointing in the opposite direciton
        # of the incoming ray
        return -1*numpy.sign(numpy.dot(Z_UNIT_VECTOR, ray)) * Z_UNIT_VECTOR

    def get_color_at_point(self, point):
        # TODO: probably should implement a pattern class for this sort of thing?
        if not self.checkered:
            return self.color
        even_x_coord = numpy.floor(point[0]) % 2 == 0
        even_y_coord = numpy.floor(point[1]) % 2 == 0
        if even_x_coord == even_y_coord:
            return self.color
        else:
            return colors.BLACK

    def ray_originates_inside(self, ray):
        # plane is 2-dimensional and has no inside
        return False


class LightSource(object):

    def __init__(self, position):
        self.position = position
