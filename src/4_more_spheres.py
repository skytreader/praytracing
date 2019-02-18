from src.hittable import HitRecord, Hittable, HittableList
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List, Optional

import sys

UNIT_VEC3: Vec3 = Vec3(1.0, 1.0, 1.0)

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
    ppm: PPM = PPM(width, height)
    lower_left_corner: Vec3 = Vec3(-2, -1, -1)
    h_movement: Vec3 = Vec3(4, 0, 0)
    v_movement: Vec3 = Vec3(0, 2, 0)
    origin: Vec3 = Vec3(0, 0, 0)

    hittables: List[Hittable] = [
        Sphere(Vec3(0, 0, -1), 0.5),
        Sphere(Vec3(0, -100.5, -1), 100)
    ]
    world: HittableList = HittableList(hittables)

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
            _color: Vec3 = color(r, world)
            _color *= 255.9
            _color.map(int)

            # Note the translation for the row: we want the white part of the
            # gradient at the bottom so we do this.
            ppm.set_pixel((height - 1) - j, i, _color)

    ppm.write(_derive_ppm_filename())
