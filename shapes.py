import numpy

import colors
from util import change_basis
from util import normalize
from util import rotate
from util import BASE_BASIS
from util import X_UNIT_VECTOR
from util import Z_UNIT_VECTOR


# to avoid floating point errors
FLOATING_POINT_ERROR_THRESHOLD = 1e-10


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

    def ray_originates_inside(self, intersection_point, ray):
        raise NotImplementedError


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
                return intersection
        else:
            d1 = (-b + numpy.sqrt(discriminant))/(2*a)
            d2 = (-b - numpy.sqrt(discriminant))/(2*a)
            best_d = None
            for potential_d in (d1, d2):
                if potential_d < FLOATING_POINT_ERROR_THRESHOLD:
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

    # TODO: this is actually the same for all shapes: if dot(normal, ray) > 0 then
    # we're inside...
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
        return ray_pos + d*ray_dir if d > FLOATING_POINT_ERROR_THRESHOLD else None

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

    def ray_originates_inside(self, intersection_point, ray):
        # This is a 2-D object and has no inside
        return False


class Box(Shape):

    def __init__(
        self,
        center,
        size,
        color,
        rotation=numpy.array([0,0,0]),
        specular=0,
        transparency=0,
        index_of_refraction=1
    ):
        self.color = color
        self.specular = specular
        self.transparency = transparency
        self.index_of_refraction = index_of_refraction

        # create a rotated basis set and a representation of the base basis
        # vectors in the new basis
        self.basis = tuple(
            rotate(basis_vector, rotation) for basis_vector in BASE_BASIS
        )
        self.base_basis_in_rotated_basis = tuple(
            change_basis(basis_vector, self.basis)
            for basis_vector in BASE_BASIS
        )

        center = change_basis(center, self.basis)

        (x_extent, y_extent, z_extent) = size
        self.x_range = (center[0] - x_extent/2.0, center[0] + x_extent/2.0)
        self.y_range = (center[1] - y_extent/2.0, center[1] + y_extent/2.0)
        self.z_range = (center[2] - z_extent/2.0, center[2] + z_extent/2.0)


    def find_intersection(self, ray_pos, ray_dir):
        """Basic strategy here is to find where the ray intersects the PLANES
        of the faces of the box and then determine if the intersection is actually
        within the box.

        To find the intersections with these planes, we need to find values of d
        such that ray_pos[i] + d*ray_dir[i] = i_range[j], where i is any
        coordinate (x, y, z) and j is either 0 or 1 for the min or max value of
        coordinate i in the box.  Thus d = (i_range[j] - ray_pos[i])/ray_dir[i]
        """
        ray_pos = change_basis(ray_pos, self.basis)
        ray_dir = change_basis(ray_dir, self.basis)

        possible_ds = []

        if ray_dir[0] != 0:
            possible_ds.append((self.x_range[0] - ray_pos[0])/ray_dir[0])
            possible_ds.append((self.x_range[1] - ray_pos[0])/ray_dir[0])

        if ray_dir[1] != 0:
            possible_ds.append((self.y_range[0] - ray_pos[1])/ray_dir[1])
            possible_ds.append((self.y_range[1] - ray_pos[1])/ray_dir[1])

        if ray_dir[2] != 0:
            possible_ds.append((self.z_range[0] - ray_pos[2])/ray_dir[2])
            possible_ds.append((self.z_range[1] - ray_pos[2])/ray_dir[2])

        possible_intersections = [ray_pos + d*ray_dir for d in possible_ds]

        best_d = None
        for possible_d in possible_ds:
            if (
                possible_d > FLOATING_POINT_ERROR_THRESHOLD  # TODO: actually need this?
                and self._is_point_on_box(ray_pos + possible_d*ray_dir)
            ):
                if best_d is None:
                    best_d = possible_d
                else:
                    best_d = min(best_d, possible_d)

        if best_d is None:
            return None

        intersection = ray_pos + best_d*ray_dir
        return change_basis(intersection, self.base_basis_in_rotated_basis)

    # TODO: this is actually checking if the point is IN the box...
    def _is_point_on_box(self, point):
        return (
            self.x_range[0] - point[0] < FLOATING_POINT_ERROR_THRESHOLD
            and point[0] - self.x_range[1] < FLOATING_POINT_ERROR_THRESHOLD

            and self.y_range[0] - point[1] < FLOATING_POINT_ERROR_THRESHOLD
            and point[1] - self.y_range[1] < FLOATING_POINT_ERROR_THRESHOLD

            and self.z_range[0] - point[2] < FLOATING_POINT_ERROR_THRESHOLD
            and point[2] - self.z_range[1] < FLOATING_POINT_ERROR_THRESHOLD
        )

    def _build_surface_normal_at_point(self, point):
        point = change_basis(point, self.basis)
        normal = numpy.array([0,0,0])
        if numpy.abs(point[0] - self.x_range[0]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[0] = -1
        if numpy.abs(point[0] - self.x_range[1]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[0] = 1

        if numpy.abs(point[1] - self.y_range[0]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[1] = -1
        if numpy.abs(point[1] - self.y_range[1]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[1] = 1

        if numpy.abs(point[2] - self.z_range[0]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[2] = -1
        if numpy.abs(point[2] - self.z_range[1]) < FLOATING_POINT_ERROR_THRESHOLD:
            normal[2] = 1

        normal = normalize(normal)
        return change_basis(normal, self.base_basis_in_rotated_basis)

    def build_surface_normal_at_point_for_ray(self, point, ray):
        base_surface_normal = self._build_surface_normal_at_point(point)
        return -1*numpy.sign(numpy.dot(base_surface_normal, ray)) * base_surface_normal

    # TODO: find a way around recalculating the surface normal
    def ray_originates_inside(self, intersection_point, ray):
        base_surface_normal = self._build_surface_normal_at_point(intersection_point)
        return numpy.dot(base_surface_normal, ray) > 0


class LightSource(object):

    def __init__(self, position):
        self.position = position
