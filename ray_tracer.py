import numpy
import png

from util import normalize


class RayTracer(object):

    def __init__(self, scene):
        self.scene = scene

    def find_pixel_color_for_ray(self, ray, position, depth=3):
        intersection, shape = self.find_closest_intersection_and_shape(ray, position)
        if not shape:
            return self.scene.background_color

        surface_normal = shape.build_surface_normal_at_point_for_ray(intersection, ray)
        incident_ray_unit = normalize(ray)

        lambert_shaded_color = self.get_lambert_shaded_color(
            shape,
            intersection,
            surface_normal
        )
        specular_color = self.get_specular_color(
            shape,
            intersection,
            surface_normal,
            incident_ray_unit,
            depth
        )
        refraction_color = self.get_refraction_color(
            shape,
            intersection,
            surface_normal,
            incident_ray_unit,
            depth
        )

        # TODO: more physical way to combine these?
        pixel_color = lambert_shaded_color + specular_color + refraction_color

        # TODO: fix this or at least factor out into a method
        for i, color_coord in enumerate(pixel_color):
            pixel_color[i] = min(255, round(pixel_color[i]))
        return pixel_color

    def find_closest_intersection_and_shape(self, ray, position):
        best_distance_to_intersection = None
        # maybe should keep these two together in an object (namedtuple?)
        closest_intersection = None
        closest_shape = None
        for intersection, shape in self.scene.yield_intersections_and_shapes(ray, position):
            distance_to_intersection = numpy.linalg.norm(intersection - position)
            if (
                best_distance_to_intersection is None
                or distance_to_intersection < best_distance_to_intersection
            ):
                best_distance_to_intersection = distance_to_intersection
                closest_intersection = intersection
                closest_shape = shape
        return closest_intersection, closest_shape

    def get_lambert_shaded_color(self, shape, intersection, surface_normal):
        normalized_lambert_factor = self.generate_lambert_factor(
            intersection,
            surface_normal
        )
        shaded_color = (
            shape.get_color_at_point(intersection) *
            normalized_lambert_factor *
            (1 - shape.transparency)
        )
        return shaded_color

    def generate_lambert_factor(self, point, surface_normal):
        lambert_factor = 0
        for path in self.scene.yield_paths_to_light_sources_from_point(point):
            if not self.is_path_obstructed(point, path):
                path_normal = normalize(path)
                lambert_contribution = numpy.dot(surface_normal, path_normal)
                if lambert_contribution > 0:
                    lambert_factor += lambert_contribution
        return min(lambert_factor, 1)

    def get_specular_color(
        self,
        shape,
        intersection,
        surface_normal,
        incident_ray_unit,
        depth
    ):
        if not shape.specular or depth == 0:
            return numpy.array([0,0,0])

        specular_contribution = shape.specular * self.find_pixel_color_for_ray(
            self.generate_reflected_ray(incident_ray_unit, surface_normal),
            intersection,
            depth-1
        )
        return specular_contribution

    def generate_reflected_ray(self, incident_ray_unit, surface_normal):
        # to reflect a ray, we need to reverse the sign of the component
        # parallel to the surface normal
        component_to_reverse = numpy.dot(surface_normal, incident_ray_unit) * surface_normal
        # reflected_ray = incident_ray_unit - 2*numpy.dot(surface_normal, incident_ray_unit)*surface_normal
        reflected_ray = incident_ray_unit - 2*component_to_reverse
        return reflected_ray

    def get_refraction_color(
        self,
        shape,
        intersection,
        surface_normal,
        incident_ray_unit,
        depth
    ):
        if not shape.transparency or depth == 0:
            return numpy.array([0,0,0])

        if shape.ray_originates_inside(intersection, incident_ray_unit):
            n1 = shape.index_of_refraction
            n2 = 1  # for now only allowing refraction with air and shape
        else:
            n1 = 1
            n2 = shape.index_of_refraction
        refracted_ray_unit = self.generate_refracted_ray(
            incident_ray_unit,
            surface_normal,
            n1,
            n2
        )
        refraction_contribution = shape.transparency * self.find_pixel_color_for_ray(
            refracted_ray_unit,
            intersection,
            depth-1
        )
        return refraction_contribution

    def generate_refracted_ray(self, incident_ray_unit, surface_normal, n1, n2):
        # Snell's law says sin(incident_angle)/sin(refreacted_angle) =
        # (index_of_refraction1)/(index_of_refraction)
        cos_incident = -1*numpy.dot(incident_ray_unit, surface_normal)
        sin_incident = numpy.sqrt(1 - cos_incident**2)
        sin_refracted = n1*sin_incident/n2

        # total internal reflection
        if sin_refracted > 1:
            return self.generate_reflected_ray(
                incident_ray_unit,
                surface_normal
            )

        cos_refracted = numpy.sqrt(1 - sin_refracted**2)
        a = cos_incident - cos_refracted
        return normalize(a*surface_normal + incident_ray_unit)

    def is_path_obstructed(self, ray, position):
        """Determine if there are any objects along ray starting from position.
        Note that ray describes the entire path, not just the direction of the
        path, so the obstruction must occur along the length of the ray.
        """
        path_length = numpy.linalg.norm(ray)
        for obstruction_point, _ in self.scene.yield_intersections_and_shapes(ray, position):
            dist_to_obstruction = numpy.linalg.norm(obstruction_point - position)
            if dist_to_obstruction <= path_length:
                return True
        return False
