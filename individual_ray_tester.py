import sys

from ray_generator import RayGenerator
from ray_tracer import RayTracer
import test


class IndividualRayTester(object):
    """Traces the ray associated to a single pixel as a debugging aid"""

    def __init__(self, scene, screen_width, screen_height):
        self.scene = scene
        self.ray_generator = RayGenerator(self.scene.direction, screen_width, screen_height)

    def get_color_for_pixel(self, pixel_x, pixel_y):
        world_y = self.ray_generator.num_vertical_steps - pixel_y - 1
        ray = self.ray_generator.create_ray_for_step_numbers(pixel_x, world_y)
        return self.scene.find_pixel_color_for_ray(ray, self.scene.position)


if __name__ == '__main__':
    tester = IndividualRayTester(test.transparency_test, 900, 900)
    print tester.get_color_for_pixel(int(sys.argv[1]), int(sys.argv[2]))
