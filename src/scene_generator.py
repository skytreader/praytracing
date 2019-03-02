from src.camera import Camera, PositionableCamera
from src.hittable import HitRecord, Hittable, HittableList
from src.material import Dielectric, Lambertian, Metal, ReflectionRecord
from src.ppm import PPM
from src.ray import Ray
from src.sphere import Sphere
from src.utils import _derive_ppm_filename
from src.vec3 import Vec3
from typing import List

import math
import sys

def random_scene(
    x_min: int, x_max: int, z_min: int, z_max: int
) -> List[Hittable]:
    # Start off the list with the "earth" sphere.
    world: List[Hittable] = [
        Sphere(Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5)))
    ]

    for x in range(x_min, x_max):
        for z in range(z_min, z_max):
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
                            random.random() * random.random()
                            random.random() * random.random()
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
                        )
                    )
                else:
                    world.append(
                        Sphere(center, 0.2, Dielectric(1.5))
                    )

    return world
