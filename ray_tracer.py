import numpy
import png

from ray_generator import RayGenerator


BACKGROUND_COLOR = numpy.array([0,0,0])  # black

ARRAY_ELEMENTS_PER_PIXEL = 3  # because of r,g,b


class RayTracer(object):

    def __init__(self, screen_width=50, screen_height=50):
        # eventually we should load a scene from a config file
        # maybe objects_in_scene should be stored in a scene class that handles
        # finding intersections
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.objects_in_scene = []
        self.ray_generator = RayGenerator(self.screen_width, self.screen_height)
        self.screen = numpy.empty(
            [self.screen_height, self.screen_width*ARRAY_ELEMENTS_PER_PIXEL],
            dtype=int
        )

    def trace_scene(self):
        for (y, x), ray in self.ray_generator.yield_primary_rays(None, None):  # TODO: implement
            pixel_color = self.find_pixel_color_for_ray(ray)

            # each pixel is actually 3 array elements
            # TODO: clean this up
            min_x = ARRAY_ELEMENTS_PER_PIXEL*x
            max_x = ARRAY_ELEMENTS_PER_PIXEL*(x+1)
            self.screen[y][min_x:max_x] = pixel_color

    def find_pixel_color_for_ray(self, ray):
        # as mentioned above, this should probably become its own class
        # also unclear that this is really the correct logic
        pixel_color = BACKGROUND_COLOR
        for object in self.objects_in_scene:
            pass

        return pixel_color

    def dump_scene_to_png(self, filename):
        png_writer = png.Writer(self.screen_width, self.screen_height)
        with open(filename, 'wb') as png_file:
            png_writer.write(png_file, self.screen)

