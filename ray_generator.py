import math

import numpy

from util import normalize


Z_UNIT_VECTOR = numpy.array([0,0,1])


class RayGenerator(object):

    def __init__(
        self,
        direction,
        num_vertical_steps,
        num_horizontal_steps,
        horiz_fov_angle=math.pi/6.0,
        vert_fov_angle=math.pi/6.0
    ):
        self.num_vertical_steps = num_vertical_steps
        self.num_horizontal_steps = num_horizontal_steps

        vertical_step_size = 2*math.sin(vert_fov_angle/2)/self.num_vertical_steps
        horizontal_step_size = 2*math.sin(horiz_fov_angle/2)/self.num_horizontal_steps

        # make sure direction is a unit vector and then find right and up vectors
        direction = normalize(direction)
        right_vector, up_vector = self.find_right_and_up_vectors(direction)

        self.horizontal_increment = right_vector * horizontal_step_size
        self.vertical_increment = up_vector * vertical_step_size

        # TODO: support non-square screen (keep d as a unit vector and set
        # step size = 2*d*tan(fov_angle/2).  But unclear how strictly to tie
        # screen aspect ratio to fov angle ratio
        self.direction = direction * math.cos(vert_fov_angle)

    def find_right_and_up_vectors(self, direction_unit_vector):
        right_unit_vector = numpy.cross(direction_unit_vector, Z_UNIT_VECTOR)
        up_unit_vector = numpy.cross(right_unit_vector, direction_unit_vector)
        return right_unit_vector, up_unit_vector

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
