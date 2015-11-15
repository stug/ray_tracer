import numpy

from colors import BLACK
from util import normalize


class Scene(object):

    def __init__(
        self,
        position,
        direction,
        background_color=BLACK,
        shapes=None,
        light_sources=None
    ):
        self.position = position
        self.direction = direction
        self.background_color = background_color
        self.shapes = shapes or []
        self.light_sources = light_sources or []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def add_light_source(self, light_source):
        self.light_sources.append(light_source)

    # TODO: make a ray class to encapsulate pos + dir?
    # TODO: clean this up!
    def find_pixel_color_for_ray(self, ray, position, depth=3):
        intersection, shape = self.find_closest_intersection_and_shape(ray, position)
        if not shape:
            return self.background_color
        surface_normal = shape.build_surface_normal_at_point_for_ray(intersection, ray)

        # lambert reflection
        lambert_factor = 0
        for path in self.yield_paths_to_light_sources_from_point(intersection):
            dist_to_light = numpy.linalg.norm(path)
            dir_to_light = path/dist_to_light
            if not self.is_path_obstructed(intersection, path):
                lambert_contribution = numpy.dot(surface_normal, dir_to_light)
                if lambert_contribution > 0:
                    lambert_factor += lambert_contribution
        normalized_lambert_factor = min(lambert_factor, 1)

        shaded_color = shape.get_color_at_point(intersection) * normalized_lambert_factor

        # specular reflection
        if not shape.specular or depth == 0:
            specular_contribution = numpy.array([0,0,0])
        else:
            incident_ray_normal = normalize(ray)
            reflected_ray_normal = 2*surface_normal + incident_ray_normal
            specular_contribution = shape.specular * self.find_pixel_color_for_ray(
                reflected_ray_normal,
                intersection,
                depth-1
            )

        specularized_color = shaded_color + specular_contribution
        # TODO: fix this or at least factor out into a method
        for i, color_coord in enumerate(specularized_color):
            specularized_color[i] = min(255, round(specularized_color[i]))
        return specularized_color

    def is_path_obstructed(self, ray, position):
        """Determine if there are any objects along ray starting from position.
        Note that ray describes the entire path, not just the direction of the
        path, so the obstruction must occur along the length of the ray.
        """
        path_length = numpy.linalg.norm(ray)
        for obstruction_point, _ in self.yield_intersections_and_shapes(ray, position):
            dist_to_obstruction = numpy.linalg.norm(obstruction_point - position)
            if dist_to_obstruction <= path_length:
                return True
        return False

    def find_closest_intersection_and_shape(self, ray, position):
        best_distance_to_intersection = None
        # maybe should keep these two together in an object (namedtuple?)
        closest_intersection = None
        closest_shape = None
        for intersection, shape in self.yield_intersections_and_shapes(ray, position):
            distance_to_intersection = numpy.linalg.norm(intersection - position)
            if best_distance_to_intersection is None or distance_to_intersection < best_distance_to_intersection:
                best_distance_to_intersection = distance_to_intersection
                closest_intersection = intersection
                closest_shape = shape
        return closest_intersection, closest_shape

    def yield_intersections_and_shapes(self, ray, position):
        for shape in self.shapes:
            intersection = shape.find_intersection(position, ray)
            if intersection is not None:
                yield intersection, shape

    def yield_paths_to_light_sources_from_point(self, point):
        for light_source in self.light_sources:
            yield light_source.position - point
