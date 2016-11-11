import sys

from ray_generator import RayGenerator
from ray_tracer import RayTracer
import test


class IndividualRayTester(object):
    """Traces the ray associated to a single pixel as a debugging aid"""

    def __init__(self, scene, screen_width, screen_height):
        self.ray_generator = RayGenerator(scene.direction, screen_width, screen_height)
        self.ray_tracer = RayTracer(scene)

    def get_color_for_pixel(self, pixel_x, pixel_y):
        world_y = self.ray_generator.num_vertical_steps - pixel_y - 1
        ray = self.ray_generator.create_ray_for_step_numbers(pixel_x, world_y)
        return self.ray_tracer.find_pixel_color_for_ray(ray, self.scene.position)


if __name__ == '__main__':
    tester = IndividualRayTester(test.plane_test, 300, 300)
    print tester.get_color_for_pixel(int(sys.argv[1]), int(sys.argv[2]))
