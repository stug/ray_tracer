import numpy

import colors
from ray_tracer import RayTracer
from scene import LightSource
from scene import Scene
from shapes import Sphere

scene = Scene(
    position=numpy.array([-5,0,0]),
    direction=numpy.array([1,0,0]),  # this is the only direction currently supported :-/
    background_color=colors.BLACK,
    shapes=[
        Sphere(
            center=numpy.array([9,-1,0]),
            radius=2,
            color=colors.BLUE,
            specular=1
        ),
        Sphere(
            center=numpy.array([10, 2, 0]),
            radius=3,
            color=colors.RED,
            specular=1
        ),
        Sphere(
            center=numpy.array([5,0,3]),
            radius=0.5,
            color=colors.GREEN,
            specular=1
        ),
        Sphere(
            center=numpy.array([5,-4,0]),
            radius=0.5,
            color=colors.MAGENTA,
            specular=1
        ),
        Sphere(
            center=numpy.array([8,0,-10]),
            radius=7,
            color=colors.YELLOW,
            specular=1
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,0,0]))
    ]
)


if __name__ == '__main__':
    tracer = RayTracer(scene, 900, 900)
    tracer.trace_scene()
    tracer.dump_scene_to_png('test.png')
