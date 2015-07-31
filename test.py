from ray_tracer import RayTracer

tracer = RayTracer(10, 10)
tracer.trace_scene()

print tracer.screen

tracer.dump_scene_to_png('test.png')
