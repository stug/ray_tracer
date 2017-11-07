import numpy

import colors
from main import RayTracerMain
from scene import Scene
from shapes import Box
from shapes import LightSource
from shapes import Plane
from shapes import Sphere


complex_scene = Scene(
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
            specular=0.2,
            transparency=1,
            index_of_refraction=1.5
        ),
        Sphere(
            center=numpy.array([5,0,3]),
            radius=0.5,
            color=colors.GREEN,
            specular=0.8
        ),
        Box(
            center=numpy.array([5,-4,0]),
            size=numpy.array([1,1,1]),
            color=colors.MAGENTA,
            specular=0.8,
            rotation=numpy.array([1,1,1])
        ),
        Sphere(
            center=numpy.array([8,0,-10]),
            radius=7,
            color=colors.YELLOW,
            specular=0.8
        ),
        Plane(
            center=numpy.array([0,0,-4]),
            normal=numpy.array([0,0,1]),
            color=colors.WHITE,
            specular=0.2,
            checkered=True
        ),
        Box(
            center=numpy.array([3,0,0]),
            size=numpy.array([2,2,2]),
            color=colors.CYAN,
            transparency=1,
            index_of_refraction=1.1,
            rotation=(numpy.pi/4.)*numpy.array([1,1,0]),
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,0,0])),
    ]
)


transparency_test = Scene(
    position=numpy.array([0,0,0]),
    direction=numpy.array([1,0,0]),
    background_color=colors.BLACK,
    shapes=[
        Sphere(
            center=numpy.array([15, 1, 0.5]),
            radius=1.5,
            color=colors.BLUE,
            transparency=0.8,
            index_of_refraction=1.5,
            specular=0.5
        ),
        Plane(
            center=numpy.array([0,0,-4]),
            normal=numpy.array([0,0,1]),
            color=colors.WHITE,
            checkered=True
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,0,0]))
    ]
)


plane_test = Scene(
    position=numpy.array([0,0,0]),
    direction=numpy.array([1,0,0]),
    background_color=colors.BLACK,
    shapes=[
        Sphere(
            center=numpy.array([15,1,0.5]),
            radius=2,
            color=colors.BLACK,
            specular=1,
        ),
        Plane(
            center=numpy.array([0,-2,0]),
            normal=numpy.array([0,1,0]),
            color=colors.BLUE,
            checkered=True
        )
    ],
    light_sources=[
        LightSource(numpy.array([15, 10, 0.5]))
    ]
)


rotate_box_test = Scene(
    position=numpy.array([-13,0,0]),
    direction=numpy.array([1,0,0]),
    background_color=colors.BLACK,
    shapes=[
        Box(
            center=numpy.array([5,-4,0]),
            size=numpy.array([1,1,1]),
            color=colors.MAGENTA,
            specular=0.8,
            rotation=2*numpy.pi*numpy.array([1,0,0])
        ),
        Plane(
            center=numpy.array([0,0,-4]),
            normal=numpy.array([0,0,1]),
            color=colors.WHITE,
            specular=0.2,
            checkered=True
        )
    ],
    light_sources=[
        LightSource(numpy.array([0,0,0])),
    ]
)


if __name__ == '__main__':
    program = RayTracerMain(complex_scene, 700, 700)
    program.trace_scene()
    program.export_png('test.png')
