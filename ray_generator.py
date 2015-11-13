import math

import numpy


class RayGenerator(object):

    def __init__(
        self,
        direction,
        num_vertical_steps,
        num_horizontal_steps,
        horiz_fov_angle=math.pi/6.0,
        vert_fov_angle=math.pi/6.0
    ):
        # TODO: actually allow any direction
        direction = numpy.array([1,0,0])

        # make sure direction is a unit vector and then scale it so we get the
        # correct FOV angle
        # TODO: support non-square screen
        self.direction = direction/numpy.linalg.norm(direction) * math.cos(vert_fov_angle)
        self.num_vertical_steps = num_vertical_steps
        self.num_horizontal_steps = num_horizontal_steps

        vertical_step_size = 2*math.sin(vert_fov_angle)/self.num_vertical_steps
        horizontal_step_size = 2*math.sin(horiz_fov_angle)/self.num_horizontal_steps
        self.horizontal_increment = numpy.array([0,1,0]) * horizontal_step_size
        self.vertical_increment = numpy.array([0,0,1]) * vertical_step_size

    def yield_primary_rays(self):
        # Note that this does not return unit vectors
        for i in xrange(self.num_horizontal_steps):
            for j in xrange(self.num_vertical_steps):
                coords = (i, j)
                yield coords, self.create_ray_for_step_numbers(i, j)

    def create_ray_for_step_numbers(self, horizontal_step_number, vertical_step_number):
        horizontal_offset = self.horizontal_increment * (horizontal_step_number - self.num_horizontal_steps/2)
        vertical_offset = self.vertical_increment * (vertical_step_number - self.num_vertical_steps/2)
        return self.direction + horizontal_offset + vertical_offset
