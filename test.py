import numpy

import colors
from ray_tracer import RayTracer
from scene import LightSource
from scene import Scene
from shapes import Sphere

scene = Scene(
    position=numpy.array([0,0,0]),
    direction=numpy.array([1,0,0]),  # this is the only direction currently supported :-/
    background_color=colors.GREY_50,
    shapes=[
        Sphere(
            center=numpy.array([9,-1,0]),
            radius=2,
            color=colors.BLUE
        ),
        Sphere(
            center=numpy.array([10, 1, 0]),
            radius=3,
            color=colors.RED
        )
    ],
    light_sources=[LightSource(numpy.array([9,-7,3]))]
)

tracer = RayTracer(scene, 200, 200)
tracer.trace_scene()

print tracer.screen

tracer.dump_scene_to_png('test.png')
