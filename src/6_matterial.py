"""
Render a matte sphere.

From the text:

    Diffuse objects that don't emit light merely take on the color of their
    surroundings but they modulate that with their own intrinsic color. Light
    that reflects off a diffuse surface has its direction randomized. They might
    also be absorbed rather than reflected. The darker the surface, the more
    likely absorption is. Any algorithm that randomizes direction will produce
    surfaces that look matte.
"""
from random import SystemRandom
from src.camera import Camera
from src.hittable import HitRecord, Hittable, HittableList
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List, Optional

import math
import sys

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)
random = SystemRandom()

def color(ray: Ray, world: HittableList) -> Vec3:
    # Some reflected rays hit not at zero but at some near-zero value due to
    # floating point shennanigans. So we try to compensate for that.
    hit_attempt: Optional[HitRecord] = world.hit(ray, 0.001, sys.float_info.max)
    if hit_attempt is not None:
        target: Vec3 = hit_attempt.p + hit_attempt.normal + random_unit_sphere_point()
        # FIXME mmm recursion
        # reflector_rate * reflected_color
        # So in this case, the matterial is a 50% reflector.
        return 0.5 * color(Ray(hit_attempt.p, target - hit_attempt.p), world)
    else:
        unit_direction: Vec3 = ray.direction.unit_vector()
        t: float = 0.5 * (unit_direction.y + 1)
        return ((1.0 - t) * UNIT_VEC3) + (t * Vec3(0.5, 0.7, 1.0))

def random_unit_sphere_point() -> Vec3:
    """
    Pick a random point inside a unit sphere. To do this, we use a "rejection
    method":

    1. Pick a random point inside a cube with edges in the [-1, 1] range of all
    axes. Note that the unit sphere is inside this cube and this cube is "easy"
    to construct programmatically.
    2. Check whether the point is inside the unit sphere. If it is not, generate
    again. Do this until we get a point inside the unit sphere.

    The time complexity of this procedure is left as an exercise to the reader.
    """
    # Shirley uses the following formula to generate a random point in the
    # constraints specified:
    #   2 * rand_vector - unit_vector
    # Where rand_vector has components that range from [0, 1). While this is
    # understandable enough, I'm experimenting with random.uniform instead.
    rand_point: Vec3 = Vec3(
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )

    while rand_point.squared_length() >= 1:
        rand_point = Vec3(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

    return rand_point

if __name__ == "__main__":
    width = 400
    height = 200
    sampling_size = 200
    ppm: PPM = PPM(width, height)
    lower_left_corner: Vec3 = Vec3(-2, -1, -1)
    h_movement: Vec3 = Vec3(4, 0, 0)
    v_movement: Vec3 = Vec3(0, 2, 0)
    origin: Vec3 = Vec3(0, 0, 0)
    cam = Camera(lower_left_corner, h_movement, v_movement, origin)

    hittables: List[Hittable] = [
        Sphere(Vec3(0, 0, -1), 0.5, "gradient-sphere"),
        Sphere(Vec3(0, -100.5, -1), 100)
    ]
    world: HittableList = HittableList(hittables)

    for j in range(height - 1, -1, -1):
        for i in range(width):
            print("Tracing on row %s, col %s" % (j, i))
            print("antialiasing...", end="")
            accumulator: Vec3 = Vec3(0, 0, 0)
            for sample in range(sampling_size):
                # In this instance, instead of u and v being mere ratios to
                # our distance from the edges, they feature a random "jitter"
                # which we use to sample the pixels around our current pixel.
                # In this sense, the current pixel is a combination of its
                # surroundings.
                u: float = float(i + random.random()) / float(width)
                v: float = float(j + random.random()) / float(height)
                r: Ray = cam.get_ray(u, v)
                accumulator += color(r, world)

            accumulator /= float(sampling_size)
            print("done")
            # Apply gamma correction. Without this line, the spheres will be too
            # dark despite the fact that they are only 50% reflectors. This
            # happens because, according to Shirley, most image viewers assume
            # that the image is gamma-corrected and so display accordingly. We
            # just comply.
            accumulator.map(math.sqrt)
            accumulator *= 255.9
            accumulator.map(int)

            ppm.set_pixel((height - 1) - j, i, accumulator)

    ppm.write(_derive_ppm_filename())
