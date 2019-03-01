from src.camera import Camera, PositionableCamera
from src.hittable import HitRecord, Hittable, HittableList
from src.material import Lambertian, ReflectionRecord
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List, Optional

import math
import random
import sys

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)

def color(ray: Ray, world: HittableList, depth: int) -> Vec3:
    # Some reflected rays hit not at zero but at some near-zero value due to
    # floating point shennanigans. So we try to compensate for that.
    hit_attempt: Optional[HitRecord] = world.hit(ray, 0.001, sys.float_info.max)
    if hit_attempt is not None:
        reflection: ReflectionRecord = hit_attempt.material.scatter(ray, hit_attempt)
        # FIXME Is it really worthwhile to check if reflection is not None here?
        # All our Materials assume that a hit has been made, and therefore some
        # reflection should happen (unless it is Vanta).
        if depth < 50 and reflection is not None:
            # Compare this with the hard-coded reflection in 6_matterial.
            return reflection.attenuation * color(reflection.scattering, world, depth + 1)
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
    camera_posn: Vec3 = Vec3(3, 3, 2)
    camera_aim: Vec3 = Vec3(0, 0, -1)
    cam: Camera = PositionableCamera(
        camera_posn, camera_aim, Vec3(0, 1, 0) ,90, width / height, 2,
        (camera_posn - camera_aim).length()
    )
    radius: float = math.cos(math.pi / 4)

    hittables: List[Hittable] = [
        Sphere(Vec3(-radius, 0, -1), radius, Lambertian(Vec3(0, 0, 1))),
        Sphere(Vec3(radius, 0, -1), radius, Lambertian(Vec3(1, 0, 0)))
    ]
    world: HittableList = HittableList(hittables)

    for j in range(height - 1, -1, -1):
        for i in range(width):
            print("Tracing on row %s, col %s" % (j, i))
            print("antialiasing...", end="")
            accumulator: Vec3 = Vec3(0, 0, 0)
            for sample in range(sampling_size):
                u: float = float(i + random.random()) / float(width)
                v: float = float(j + random.random()) / float(height)
                r: Ray = cam.get_ray(u, v)
                accumulator += color(r, world, 1)

            accumulator /= float(sampling_size)
            print("done")
            accumulator.map(math.sqrt)
            accumulator *= 255.9
            accumulator.map(int)

            ppm.set_pixel((height - 1) - j, i, accumulator)

    ppm.write(_derive_ppm_filename())
