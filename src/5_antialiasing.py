from random import SystemRandom
from src.camera import Camera
from src.hittable import HitRecord, Hittable, HittableList
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List, Optional

import sys

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)
random = SystemRandom()

def color(ray: Ray, world: HittableList) -> Vec3:
    hit_attempt: Optional[HitRecord] = world.hit(ray, 0.0, sys.float_info.max)
    if hit_attempt is not None:
        return 0.5 * Vec3(
            hit_attempt.normal.x + 1, hit_attempt.normal.y + 1,
            hit_attempt.normal.z + 1
        )
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
                u: float = (i + random.random()) / width
                v: float = (j + random.random()) / height
                r: Ray = cam.get_ray(u, v)
                # Huh? What's that 2.0 magic number here?
                p: Vec3 = r.point_at_parameter(2.0)
                accumulator += color(r, world)

            accumulator /= sampling_size
            print("done")
            _color: Vec3 = color(r, world)
            _color *= 255.9
            _color.map(int)

            # Note the translation for the row: we want the white part of the
            # gradient at the bottom so we do this.
            ppm.set_pixel((height - 1) - j, i, _color)

    ppm.write(_derive_ppm_filename())
