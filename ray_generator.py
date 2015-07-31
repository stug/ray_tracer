import math

import numpy


class RayGenerator(object):

    def __init__(
        self,
        num_vertical_steps,
        num_horizontal_steps,
        horiz_fov_angle = math.pi/3.0,
        vert_fov_angle = math.pi/3.0
    ):
        self.num_vertical_steps = num_vertical_steps
        self.num_horizontal_steps = num_horizontal_steps

        self.vertical_step_size = 2*math.sin(vert_fov_angle)
        self.horizontal_step_size = 2*math.sin(horiz_fov_angle)

    def yield_primary_rays(self, position, direction):
        # TODO: actually implement this 
        position = numpy.array([0,0,0])
        direction = numpy.array([1,0,0])

        # make sure direction is a unit vector
        direction = direction/numpy.linalg.norm(direction)
        horizontal_increment = numpy.array([0,1,0]) / self.horizontal_step_size
        vertical_increment = numpy.array([0,0,1]) / self.vertical_step_size

        # this won't yield unit vectors -- problem?
        for i in xrange(self.num_vertical_steps):
            for j in xrange(self.num_horizontal_steps):
                horizontal_offset = horizontal_increment * (j - self.num_horizontal_steps/2)
                vertical_offset = vertical_increment * (i - self.num_vertical_steps/2)
                ray = direction + horizontal_offset + vertical_offset
                pixel_coords = (i, j)
                yield pixel_coords, ray
