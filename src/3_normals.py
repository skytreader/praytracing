from src.ppm import PPM
from src.ray import Ray
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3

import math

"""
We have an abstract, static camera at (0, 0, 0).
"""

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)

def hit_sphere(center: Vec3, radius: float, ray: Ray) -> float:
    """
    Check if the given ray hits the sphere described by the center and the
    radius.

    More than just computing whether a ray hits the sphere, it also solves for
    the actual point of intersection. This can then be used to compute the
    normal vector _at that point_.
    """
    # The vector from the ray's origin to the center of the sphere
    oc: Vec3 = ray.origin - center
    a: float = ray.direction.dot(ray.direction)
    b: float = 2.0 * oc.dot(ray.direction)
    c: float = oc.dot(oc) - (radius ** 2)
    discriminant: float = (b ** 2) - (4 * a * c)

    if discriminant < 0:
        return -1.0
    else:
        # The quadratic equation has a conjugate pair for its numerator.
        # However, in here we only take the negative part of the conjugate pair.
        # This seems to be an arbitrary decision; try to change the negative to
        # positive and see some cool shit!
        return (-b - math.sqrt(discriminant)) / (2 * a)

def color(ray: Ray) -> Vec3:
    """
    Linear interpolation of color based on the y direction.

    As for hitting the sphere, note that the brightness of an object with
    respect to its light source is dependent on its normal vectors. The greater
    the angle between the normal and the light ray, the darker that spot is.
    Obvious implication: the sphere is brightest where the angle between the
    normal and the light ray is 0---that is, when the light ray is parallel to
    the normal.
    """
    t: float = hit_sphere(Vec3(0, 0, -1), 0.5, ray)
    if t > 0:
        normal: Vec3 = (ray.point_at_parameter(t) - Vec3(0, 0, -1)).unit_vector()
        # For all I can tell, what this does is to "scale" the normal such that
        # (a) there are no negatives and (b) it will not all devolve to just 0,
        # which leaves us with just a black circle. Multiplying by .5 ensures
        # that the resulting sphere isn't too dark or too light.
        #
        # - Without the scaling factor (0.5), the image is just too bright.
        # - Without the increments to each component of the normal, the
        #   resulting image will tend to have negative values, which are invalid
        #   in the PPM spec to begin with, and just plain doesn't make sense.
        return 0.5 * Vec3(normal.x + 1, normal.y + 1, normal.z + 1)

    unit_direction: Vec3 = ray.direction.unit_vector()
    # Note that t's definition was pulled up. I guess he was just saving on some
    # stack space.
    t = 0.5 * (unit_direction.y + 1)
    return (UNIT_VEC3 * (1.0 - t)) + (Vec3(0.5, 0.7, 1.0) * t)

if __name__ == "__main__":
    width = 400
    height = 200
    ppm: PPM = PPM(width, height)
    lower_left_corner: Vec3 = Vec3(-2, -1, -1)
    h_movement: Vec3 = Vec3(4, 0, 0)
    v_movement: Vec3 = Vec3(0, 2, 0)
    origin: Vec3 = Vec3(0, 0, 0)

    for j in range(height - 1, -1, -1):
        for i in range(width):
            # Get the ratio of how far are we from the "edges".
            u = i / width
            v = j / height
            # And use those ratios to "move" the ray away from the origin. Note:
            #  - (h_ * u) + (v_ * v) is scaled movement
            #  - the movement scales differently depending on dimension:
            #    horizontal movement is increasing towards the vector (4, 0, 0)
            #    while vertical movement is decreasing from the vector (0, 2, 0)
            r: Ray = Ray(origin, lower_left_corner + (h_movement * u) + (v_movement * v))
            _color: Vec3 = color(r)
            _color *= 255.9
            _color.map(int)

            # Note the translation for the row: we want the white part of the
            # gradient at the bottom so we do this.
            ppm.set_pixel((height - 1) - j, i, _color)

    ppm.write(_derive_ppm_filename())
