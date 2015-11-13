import numpy
import png

from ray_generator import RayGenerator
from shapes import Sphere


ARRAY_ELEMENTS_PER_PIXEL = 3  # because of r,g,b


class RayTracer(object):

    def __init__(self, scene, screen_width=100, screen_height=100):
        # eventually we should load a scene from a config file
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scene = scene
        self.ray_generator = RayGenerator(self.scene.direction, self.screen_width, self.screen_height)
        self.screen = numpy.empty(
            [self.screen_height, self.screen_width*ARRAY_ELEMENTS_PER_PIXEL],
            dtype=int
        )

    def trace_scene(self):
        for (x, y), ray in self.ray_generator.yield_primary_rays():
            pixel_color = self.scene.find_pixel_color_for_ray(
                ray,
                self.scene.position
            )

            # because computer graphics usually starts with increasing y moving
            # downward in the image, need to transform the world coordinates to
            # screen coordinates
            screen_y = self.screen_height - y - 1

            # each pixel is actually 3 array elements
            # TODO: clean this up and maybe make it its own method
            # TODO: or better, make a screen class that abstracts this away
            min_x = ARRAY_ELEMENTS_PER_PIXEL*x
            max_x = ARRAY_ELEMENTS_PER_PIXEL*(x+1)
            self.screen[screen_y][min_x:max_x] = pixel_color

    def dump_scene_to_png(self, filename):
        png_writer = png.Writer(self.screen_width, self.screen_height)
        with open(filename, 'wb') as png_file:
            png_writer.write(png_file, self.screen)

