import numpy

from colors import BLACK


# Used to avoid floating point errors in calculating distance to obstructions
# when determining when to render shadow.
THRESHOLD_SHADING_DISTANCE = 1


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
    def find_pixel_color_for_primary_ray(self, ray):
        intersection, shape = self.find_closest_intersection_and_shape(ray, self.position)
        if not shape:
            return self.background_color
        # import ipdb; ipdb.set_trace()
        for path in self.yield_paths_to_light_sources_from_point(intersection):
            dist_to_light = numpy.linalg.norm(path)
            unobstructed = True  # TODO: better way to do this?  pretty ugly.
            for obstruction, _ in self.yield_intersections_and_shapes(path, intersection):
                unobstructed = False
                dist_to_obstruction = numpy.linalg.norm(obstruction)
                if (
                    dist_to_light <= dist_to_obstruction
                    or dist_to_obstruction < THRESHOLD_SHADING_DISTANCE
                ):
                    return shape.color
            if unobstructed:
                return shape.color
        return BLACK  # eventually want shading


    def find_closest_intersection_and_shape(self, ray, position):
        best_distance_to_intersection = None
        # maybe should keep these two together in an object (namedtuple?)
        closest_intersection = None
        closest_shape = None
        for intersection, shape in self.yield_intersections_and_shapes(ray, position):
            distance_to_intersection = numpy.linalg.norm(intersection - self.position)
            if best_distance_to_intersection is None or distance_to_intersection < best_distance_to_intersection:
                best_distance_to_intersection = distance_to_intersection
                closest_intersection = intersection
                closest_shape = shape
        return closest_intersection, closest_shape

    def yield_intersections_and_shapes(self, ray, position):
        for shape in self.shapes:
            intersection = shape.find_intersection_and_normal(
                position,
                ray
            )
            if intersection is not None:
                yield intersection, shape

    def yield_paths_to_light_sources_from_point(self, point):
        for light_source in self.light_sources:
            yield light_source.position - point


class LightSource(object):

    def __init__(self, position):
        self.position = position
