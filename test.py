import numpy

import colors
from ray_tracer import RayTracer
from scene import Scene
from shapes import LightSource
from shapes import Sphere
from shapes import ZPlane

scene1 = Scene(
    position=numpy.array([-13,0,0]),
    direction=numpy.array([1,0,0]),
    background_color=colors.BLACK,
    shapes=[
        Sphere(
            center=numpy.array([9,-1,0]),
            radius=2,
            color=colors.BLUE,
            specular=0.8
        ),
        Sphere(
            center=numpy.array([10, 2, 0]),
            radius=3,
            color=colors.RED,
            specular=0.8
        ),
        Sphere(
            center=numpy.array([5,0,3]),
            radius=0.5,
            color=colors.GREEN,
            specular=0.8
        ),
        Sphere(
            center=numpy.array([5,-4,0]),
            radius=0.5,
            color=colors.MAGENTA,
            specular=0.8
        ),
        Sphere(
            center=numpy.array([8,0,-10]),
            radius=7,
            color=colors.YELLOW,
            specular=0.8
        ),
        ZPlane(
            z_coord=-4,
            color=colors.WHITE,
            checkered=True,
            specular=0.8
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,0,0])),
    ]
)

scene2 = Scene(
    position=numpy.array([0,0,0]),
    direction=numpy.array([1,0,0]),
    background_color=colors.BLACK,
    shapes=[
        Sphere(
            center=numpy.array([0,0,0]),
            radius=10,
            color=colors.GREY_50,
            specular=0.9
        ),
        Sphere(
            center=numpy.array([4,1,1]),
            radius=0.5,
            color=colors.RED,
            specular=0.5
        ),
        ZPlane(
            z_coord=-2,
            color=colors.WHITE,
            checkered=True,
            specular=0
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,-7,0])),
    ]
)


if __name__ == '__main__':
    tracer = RayTracer(scene1, 900, 900)
    tracer.trace_scene()
    tracer.dump_scene_to_png('test.png')
