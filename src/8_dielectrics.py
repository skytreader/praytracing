from random import SystemRandom
from src.camera import Camera
from src.hittable import HitRecord, Hittable, HittableList
from src.material import Dielectric, Lambertian, Metal, ReflectionRecord
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

def color(ray: Ray, world: HittableList, depth: int) -> Vec3:
    # Some reflected rays hit not at zero but at some near-zero value due to
    # floating point shennanigans. So we try to compensate for that.
    hit_attempt: Optional[HitRecord] = world.hit(ray, 0.001, sys.float_info.max)
    if hit_attempt is not None:
        scattering: ReflectionRecord = hit_attempt.material.scatter(ray, hit_attempt)
        # FIXME Is it really worthwhile to check if reflection is not None here?
        # All our Materials assume that a hit has been made, and therefore some
        # reflection should happen (unless it is Vanta).
        if depth < 50 and scattering is not None:
            # Compare this with the hard-coded reflection in 6_matterial.
            return scattering.attenuation * color(scattering.scattering, world, depth + 1)
        else:
            return Vec3(0, 0, 0)
    else:
        unit_direction: Vec3 = ray.direction.unit_vector()
        t: float = 0.5 * (unit_direction.y + 1)
        return ((1.0 - t) * UNIT_VEC3) + (t * Vec3(0.5, 0.7, 1.0))

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
        Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.8, 0.3, 0.3))),
        Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0))),
        Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), 0.3)),
        Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5))
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
                accumulator += color(r, world, 0)

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
