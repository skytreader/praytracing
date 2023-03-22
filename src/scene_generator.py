from src.camera import Camera, PositionableCamera
from src.hittable import HitRecord, Hittable, HittableList
from src.material import Dielectric, Lambertian, Metal, ReflectionRecord
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List, Optional

import math
import random
import sys

UNIT_VEC3: Vec3 = Vec3(1, 1, 1)

def random_scene(
    x_min: int, x_max: int, z_min: int, z_max: int
) -> List[Hittable]:
    # Start off the list with the "earth" sphere.
    world: List[Hittable] = [
        Sphere(Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5)))
    ]

    for x in range(x_min, x_max):
        if len(world) >= 100:
            break
        for z in range(z_min, z_max):
            if len(world) >= 100:
                break
            material_decider: float = random.random()
            # TODO Clarify what the 0.9 constant here is for.
            center: Vec3 = Vec3(
                x + 0.9 * random.random(),
                0.2,
                z + 0.9 * random.random()
            )

            # TODO What is Vec3(4, 0.2, 0) for?
            if (center - Vec3(4, 0.2, 0)).length() > 0.9:
                if material_decider < 0.8:
                    world.append(
                        Sphere(center, 0.2, Lambertian(Vec3(
                            random.random() * random.random(),
                            random.random() * random.random(),
                            random.random() * random.random()
                        )))
                    )
                elif material_decider < 0.95:
                    world.append(
                        Sphere(center, 0.2, Metal(
                            Vec3(
                                0.5 * (1 + random.random()),
                                0.5 * (1 + random.random()),
                                0.5 * (1 + random.random())
                            ),
                            0.5 * random.random()
                        ))
                    )
                else:
                    world.append(
                        Sphere(center, 0.2, Dielectric(1.5))
                    )

    world.extend([
        Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)),
        Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))),
        Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0))
    ])

    return world

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
    width: int = 1200
    height: int = 800
    sampling_size: int = 10
    ppm: PPM = PPM(width, height)
    spam: List[Hittable] = random_scene(-11, 11, -11, 11)
    world = HittableList(spam)
    print(spam)

    lookfrom: Vec3 = Vec3(13, 2, 3)
    lookat: Vec3 = Vec3(0, 0, 0)
    focus_distance: float = 10.0;
    aperture: float = 0.1

    camera: Camera = PositionableCamera(
        lookfrom, lookat, Vec3(0, 1, 0), 20, width / height, aperture,
        focus_distance
    )

    for j in range(height - 1, -1, -1):
        for i in range(width):
            print("Tracing on row %s, col %s" % (j, i))
            accumulator: Vec3 = Vec3(0, 0, 0)

            for sample in range(sampling_size):
                u: float = float(i + random.random()) / width
                v: float = float(j + random.random()) / height
                r: Ray = camera.get_ray(u, v)
                accumulator += color(r, world, 0)

            accumulator /= sampling_size
            accumulator.map(math.sqrt)
            accumulator *= 255.9
            accumulator.map(int)

            ppm.set_pixel((height - 1) - j, i, accumulator)

    ppm.write(_derive_ppm_filename())
