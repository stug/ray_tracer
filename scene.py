import numpy

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

    def add_shape(self, shape):
        self.shapes.append(shape)

    def add_light_source(self, light_source):
        self.light_sources.append(light_source)

    # TODO: make a ray class to encapsulate pos + dir?
    # TODO: this should take a kwarg that tell us if we care about which shape
    # gets hit first and the color, etc
    def find_pixel_color_for_ray(self, ray):
        best_distance_to_intersection = None
        pixel_color = self.background_color

        for shape in self.shapes:
            intersection, normal =  shape.find_intersection_and_normal(
                self.position,
                ray
            )
            if intersection is not None:
                distance_to_intersection = numpy.linalg.norm(intersection - self.position)
                if best_distance_to_intersection is None or distance_to_intersection < best_distance_to_intersection:
                    best_distance_to_intersection = distance_to_intersection
                    pixel_color = shape.color
        return pixel_color
