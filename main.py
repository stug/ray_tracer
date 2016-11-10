import numpy
import png

from ray_generator import RayGenerator
from ray_tracer import RayTracer


ARRAY_ELEMENTS_PER_PIXEL = 3  # because of r,g,b


class RayTracerMain(object):

    def __init__(self, scene, screen_width=100, screen_height=100):
        self.scene = scene
        self.ray_generator = RayGenerator(
            self.scene.direction,
            screen_width,
            screen_height
        )
        self.ray_tracer = RayTracer(scene)
        self.screen = Screen(screen_width, screen_height)

    def trace_scene(self):
        for (x, y), ray in self.ray_generator.yield_primary_rays():
            # TODO: create a ray class to encapsulate ray + position so this
            # class doesn't have to know about the scene
            pixel_color = self.ray_tracer.find_pixel_color_for_ray(
                ray,
                self.scene.position
            )
            self.screen.write_pixel(x, y, pixel_color)

    def export_png(self, filename):
        self.screen.dump_to_png(filename)


class Screen(object):

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.screen = numpy.empty(
            [self.height, self.width*ARRAY_ELEMENTS_PER_PIXEL],
            dtype=int
        )

    def write_pixel(self, x, y, color):
        # because computer graphics usually starts with increasing y moving
        # downward in the image, need to transform the world coordinates to
        # screen coordinates
        screen_y = self.height - y - 1

        min_x = ARRAY_ELEMENTS_PER_PIXEL * x
        max_x = ARRAY_ELEMENTS_PER_PIXEL * (x + 1)
        self.screen[screen_y][min_x:max_x] = color

    def dump_to_png(self, filename):
        png_writer = png.Writer(self.width, self.height)
        with open(filename, 'wb') as png_file:
            png_writer.write(png_file, self.screen)
