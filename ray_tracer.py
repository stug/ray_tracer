import numpy
import png

from ray_generator import RayGenerator
from screen import Screen
from shapes import Sphere


ARRAY_ELEMENTS_PER_PIXEL = 3  # because of r,g,b


class RayTracer(object):

    def __init__(self, scene, screen_width=100, screen_height=100):
        # eventually we should load a scene from a config file
        # although I guess the scene itself should handle that
        self.scene = scene
        self.ray_generator = RayGenerator(
            self.scene.direction,
            screen_width,
            screen_height
        )
        self.screen = Screen(screen_width, screen_height)

    def trace_scene(self):
        for (x, y), ray in self.ray_generator.yield_primary_rays():
            pixel_color = self.scene.find_pixel_color_for_ray(
                ray,
                self.scene.position
            )
            self.screen.write_pixel(x, y, pixel_color)

    def dump_scene_to_png(self, filename):
        self.screen.dump_to_png(filename)

