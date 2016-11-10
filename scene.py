from colors import BLACK


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

    def yield_intersections_and_shapes(self, ray, position):
        for shape in self.shapes:
            intersection = shape.find_intersection(position, ray)
            if intersection is not None:
                yield intersection, shape

    def yield_paths_to_light_sources_from_point(self, point):
        for light_source in self.light_sources:
            yield light_source.position - point
