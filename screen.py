import numpy
import png


ARRAY_ELEMENTS_PER_PIXEL = 3  # because of r,g,b


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
