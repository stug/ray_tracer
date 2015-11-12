import sys

from ray_generator import RayGenerator
from ray_tracer import RayTracer
from test import scene as test_scene


class IndividualRayTester(object):
    """Traces the ray associated to a single pixel as a debugging aid"""

    def __init__(self, scene, screen_width, screen_height):
        self.scene = scene
        self.ray_generator = RayGenerator(self.scene, screen_width, screen_height)

    def get_color_for_pixel(self, pixel_x, pixel_y):
        ray = self.ray_generator.create_ray_for_step_numbers(pixel_y, pixel_x)
        return self.scene.find_pixel_color_for_primary_ray(ray)


if __name__ == '__main__':
    tester = IndividualRayTester(test_scene, 200, 200)
    print tester.get_color_for_pixel(int(sys.argv[1]), int(sys.argv[2]))
